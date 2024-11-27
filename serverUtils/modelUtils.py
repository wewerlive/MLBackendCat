import argparse
import os
from datetime import datetime

import numpy as np
import torch
from diffusers.image_processor import VaeImageProcessor
from huggingface_hub import snapshot_download

from modelBackbone.model.cloth_masker import AutoMasker, vis_mask
from modelBackbone.model.pipeline import CatVTONPipeline
from modelBackbone.utils import init_weight_dtype, resize_and_crop, resize_and_padding

from serverUtils.imageUtils import imageFromBase64, imageToBase64


from DeepCache import DeepCacheSDHelper


# Load the model
repo_path = snapshot_download(repo_id='zhengchong/CatVTON')

# Pipeline
pipeline = CatVTONPipeline(
        base_ckpt="booksforcharlie/stable-diffusion-inpainting",
        attn_ckpt=repo_path,
        attn_ckpt_version="mix",
        weight_dtype=init_weight_dtype("bf16"),
        use_tf32=True,
        device='cuda'
)


helper = DeepCacheSDHelper(pipe=pipeline)
helper.set_params(cache_interval=3, cache_branch_id=0)
helper.enable()

# pipeline.unet.to(memory_format=torch.channels_last)
# pipeline.vae.to(memory_format=torch.channels_last)



# AutoMasker
mask_processor = VaeImageProcessor(vae_scale_factor=8, do_normalize=False, do_binarize=True, do_convert_grayscale=True)

automasker = AutoMasker(
    densepose_ckpt=os.path.join(repo_path, "DensePose"),
    schp_ckpt=os.path.join(repo_path, "SCHP"),
    device='cuda', 
)

imageWidth = 768
imageHeight = 1024

def predictTryOn(personImage,clothImage,cloth_type,num_inference_steps=10,seed=-1,guidance_scale=2.5):
    # person_image = Image.open(BytesIO(base64.b64decode(personImage64.split(",")[1]))).resize((768, 1024))
    # cloth_image = Image.open(BytesIO(base64.b64decode(clothImage64.split(",")[1]))).resize((768, 1024))
    person_image = personImage.resize((imageWidth, imageHeight))
    cloth_image = clothImage.resize((imageWidth, imageHeight))
    person_image.save("person.jpg")
    cloth_image.save("cloth.jpg")
    mask = automasker(
            person_image,
            cloth_type
        )['mask']
    mask = mask_processor.blur(mask, blur_factor=9)
    generator = None
    if seed != -1:
        generator = torch.Generator(device='cuda').manual_seed(seed)
    # Inference
    # try:
    result_image = pipeline(
        image=person_image,
        condition_image=cloth_image,
        mask=mask,
        num_inference_steps=num_inference_steps,
        guidance_scale=guidance_scale,
        generator=generator
    )[0]
    print(result_image)
#     imFile = BytesIO()
#     result_image.save(imFile, format="JPEG")
#     imFile = imFile.getvalue()
#     imFile = base64.b64encode(imFile)

#     result_image.save("result.jpg")

# #     person_image = person_image = resize_and_crop(person_image, (imageWidth, imageHeight))
# #     cloth_image = resize_and_padding(cloth_image, (imageWidth, imageHeight))
#     return str(imFile)
    return result_image

