import torch
from diffusers import StableDiffusionPipeline


class StableDiffusion:
    def __init__(self) -> None:
        self._model = StableDiffusionPipeline.from_pretrained(
            'dreamlike-art/dreamlike-diffusion-1.0', torch_dtype=torch.float32
        )

    def get_response(self, message: str) -> str:
        self._model.to(torch.device('cuda'))
        images = self._model(prompt=message).images[0]
        return images
