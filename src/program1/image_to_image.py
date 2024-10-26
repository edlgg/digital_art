import torch
from diffusers import AutoPipelineForImage2Image
from diffusers.utils import load_image, make_image_grid

from consts import DATA_DIR

file_path = DATA_DIR / "meadow_cube.jpg"

pipeline = AutoPipelineForImage2Image.from_pretrained(
    "kandinsky-community/kandinsky-2-2-decoder", torch_dtype=torch.float16, use_safetensors=True
)
pipeline.enable_model_cpu_offload()
# remove following line if xFormers is not installed or you have PyTorch 2.0 or higher installed
pipeline.enable_xformers_memory_efficient_attention()

init_image = load_image(file_path)

prompt = "magical land"
image = pipeline(prompt, image=init_image).images[0]
final_image = make_image_grid([init_image, image], rows=1, cols=2)
final_image.show()

