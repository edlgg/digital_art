import bpy

def clear_scene():
    bpy.ops.object.select_all(action='SELECT')
    bpy.ops.object.delete()


def create_white_frame(size=6, thickness=0.05):
    bpy.ops.mesh.primitive_cube_add(size=size)
    frame = bpy.context.object
    frame.name = "WhiteFrame"
    bpy.ops.object.modifier_add(type='WIREFRAME')
    frame.modifiers["Wireframe"].thickness = thickness

    mat = bpy.data.materials.new(name="WhiteMat")
    mat.use_nodes = True
    bsdf = mat.node_tree.nodes["Principled BSDF"]
    bsdf.inputs["Base Color"].default_value = (1, 1, 1, 1)
    bsdf.inputs["Roughness"].default_value = 0.3
    frame.data.materials.append(mat)

    return frame


def add_camera(location=(10, -10, 6), rotation=(1.1, 0, 0.78)):
    bpy.ops.object.camera_add(location=location, rotation=rotation)
    bpy.context.scene.camera = bpy.context.object
    return bpy.context.object


def add_light(location=(5, -5, 5), energy=2000):
    bpy.ops.object.light_add(type='AREA', location=location)
    light = bpy.context.object
    light.data.energy = energy
    return light


def add_base_sphere(radius=1, location=(0, 0, 0)):
    bpy.ops.mesh.primitive_uv_sphere_add(radius=radius, location=location)
    sphere = bpy.context.object
    sphere.name = "BaseSphere"
    return sphere


def setup_scene():
    clear_scene()
    create_white_frame()
    add_camera()
    add_light()
    add_base_sphere()


if __name__ == "__main__":
    setup_scene()
