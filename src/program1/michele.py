import time
import numpy as np
import pygfx as gfx
from scipy import interpolate
from wgpu.gui.auto import WgpuCanvas, run

gltf_path = model_dir / "Michelle.glb"
print("Loading", gltf_path)

canvas = WgpuCanvas(size=(640, 480), max_fps=-1, title="Skinnedmesh", vsync=False)

renderer = gfx.WgpuRenderer(canvas)
camera = gfx.PerspectiveCamera(75, 640 / 480, depth_range=(0.1, 1000))
camera.local.position = (0, 100, 200)
camera.look_at((0, 100, 0))
scene = gfx.Scene()

scene.add(gfx.AmbientLight(), gfx.DirectionalLight())


gltf = gfx.load_gltf(gltf_path, quiet=True)

# gfx.print_tree(gltf.scene) # Uncomment to see the tree structure

# Group[Scene]
# - WorldObject[Character]
# - - SkinnedMesh[Ch03]
# - - Bone[mixamorig:Hips]
# - - - ...

model_obj = gltf.scene.children[0]
model_obj.local.scale = (1, 1, 1)

action_clip = gltf.animations[0]

skeleton_helper = gfx.SkeletonHelper(model_obj)
scene.add(skeleton_helper)

scene.add(model_obj)

gfx.OrbitController(camera, register_events=renderer)


def update_track(track, time):
    target = track["target"]
    property = track["property"]
    values = track["values"]
    times = track["times"]
    interpolation = track["interpolation"]

    if time < times[0]:
        time = times[0]

    # TODO: Use scipy to interpolate now, will use our own implementation later
    if interpolation == "LINEAR":
        if property == "rotation":
            # TODO: should use spherical linear interpolation instead
            cs = interpolate.interp1d(times, values, kind="linear", axis=0)
            value = cs(time)
            value = value / np.linalg.norm(value)  # normalize quaternion
        else:
            cs = interpolate.interp1d(times, values, kind="linear", axis=0)
            value = cs(time)

    elif interpolation == "CUBICSPLINE":
        cs = interpolate.interp1d(times, values, kind="cubic", axis=0)
        value = cs(time)
    elif interpolation == "STEP":
        cs = interpolate.interp1d(times, values, kind="previous", axis=0)
        value = cs(time)
    else:
        print("unknown interpolation", interpolation)

    if property == "scale":
        target.local.scale = value
    elif property == "translation":
        target.local.position = value
    elif property == "rotation":
        target.local.rotation = value
    else:
        print("unknown property", property)


tracks = action_clip["tracks"]
gloabl_time = 0
last_time = time.perf_counter()

stats = gfx.Stats(viewport=renderer)


def animate():
    global gloabl_time, last_time
    now = time.perf_counter()
    dt = now - last_time
    last_time = now
    gloabl_time += dt
    if gloabl_time > action_clip["duration"]:
        gloabl_time = 0

    for track in tracks:
        update_track(track, gloabl_time)

    model_obj.children[0].skeleton.update()
    skeleton_helper.update()

    with stats:
        renderer.render(scene, camera, flush=False)
    stats.render()
    canvas.request_draw()


if __name__ == "__main__":
    renderer.request_draw(animate)
    run()