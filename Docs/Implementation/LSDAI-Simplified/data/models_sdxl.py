#!/usr/bin/env python3
"""
LSDAI Simplified - SDXL Model Definitions
Sample popular SDXL models for reference
"""

# Popular SDXL Base Models
SDXL_CHECKPOINTS = {
    "SDXL Base 1.0": {
        "url": "https://huggingface.co/stabilityai/stable-diffusion-xl-base-1.0/resolve/main/sd_xl_base_1.0.safetensors",
        "description": "Official SDXL 1.0 base model",
        "filename": "sd_xl_base_1.0.safetensors"
    },
    "SDXL Refiner 1.0": {
        "url": "https://huggingface.co/stabilityai/stable-diffusion-xl-refiner-1.0/resolve/main/sd_xl_refiner_1.0.safetensors",
        "description": "Official SDXL 1.0 refiner model",
        "filename": "sd_xl_refiner_1.0.safetensors"
    },
    "Juggernaut XL": {
        "url": "https://civitai.com/api/download/models/198639",
        "description": "Photorealistic SDXL model",
        "filename": "juggernautXL_version6Rundiffusion.safetensors"
    },
    "RealVis XL": {
        "url": "https://civitai.com/api/download/models/245431",
        "description": "Realistic photography SDXL model",
        "filename": "realvisxlV30.safetensors"
    },
    "DreamShaper XL": {
        "url": "https://civitai.com/api/download/models/293609",
        "description": "Artistic SDXL model",
        "filename": "dreamshaperXL_lightningDPMSDE.safetensors"
    },
    "Animagine XL": {
        "url": "https://civitai.com/api/download/models/293609",
        "description": "Anime style SDXL model",
        "filename": "animagineXLV3_v30.safetensors"
    }
}

# Popular SDXL LoRA Models
SDXL_LORAS = {
    "SDXL Illustration Helper": {
        "url": "https://civitai.com/api/download/models/139504",
        "description": "Illustration style helper for SDXL",
        "filename": "sdxl_illustration_helper.safetensors"
    },
    "Photography Helper": {
        "url": "https://civitai.com/api/download/models/245431",
        "description": "Photography enhancement for SDXL",
        "filename": "sdxl_photography_helper.safetensors"
    },
    "Anime Style Enhancer": {
        "url": "https://civitai.com/api/download/models/293609",
        "description": "Anime style enhancement for SDXL",
        "filename": "sdxl_anime_enhancer.safetensors"
    }
}

# Popular SDXL VAE Files
SDXL_VAES = {
    "SDXL VAE": {
        "url": "https://huggingface.co/stabilityai/sdxl-vae/resolve/main/sdxl_vae.safetensors",
        "description": "Official SDXL VAE",
        "filename": "sdxl_vae.safetensors"
    },
    "Custom SDXL VAE": {
        "url": "https://huggingface.co/madebyollin/sdxl-vae-fp16-fix/resolve/main/sdxl_vae.safetensors",
        "description": "Fixed FP16 SDXL VAE",
        "filename": "sdxl_vae_fp16_fix.safetensors"
    }
}

# Popular SDXL ControlNet Models
SDXL_CONTROLNET = {
    "Canny SDXL": {
        "url": "https://huggingface.co/diffusers/controlnet-canny-sdxl-1.0/resolve/main/diffusion_pytorch_model.safetensors",
        "description": "Canny edge detection for SDXL",
        "filename": "controlnet-canny-sdxl-1.0.safetensors"
    },
    "Depth SDXL": {
        "url": "https://huggingface.co/diffusers/controlnet-depth-sdxl-1.0/resolve/main/diffusion_pytorch_model.safetensors",
        "description": "Depth map control for SDXL",
        "filename": "controlnet-depth-sdxl-1.0.safetensors"
    },
    "Pose SDXL": {
        "url": "https://huggingface.co/diffusers/controlnet-openpose-sdxl-1.0/resolve/main/diffusion_pytorch_model.safetensors",
        "description": "Human pose estimation for SDXL",
        "filename": "controlnet-openpose-sdxl-1.0.safetensors"
    }
}

# Popular SDXL Textual Inversions/Embeddings
SDXL_EMBEDDINGS = {
    "SDXL Negative Prompt": {
        "url": "https://huggingface.co/guoyww/ambiguous/resolve/main/ambiguous.pt",
        "description": "Negative prompt embedding for SDXL",
        "filename": "sdxl_negative_prompt.pt"
    },
    "Quality Enhancer": {
        "url": "https://huggingface.co/ffs/quality-enhancer/resolve/main/quality_enhancer.pt",
        "description": "Quality enhancement embedding for SDXL",
        "filename": "quality_enhancer.pt"
    }
}

def get_sdxl_models():
    """Get all SDXL models"""
    return {
        'ckpt': SDXL_CHECKPOINTS,
        'lora': SDXL_LORAS,
        'vae': SDXL_VAES,
        'controlnet': SDXL_CONTROLNET,
        'embeddings': SDXL_EMBEDDINGS
    }

def get_sdxl_model_info(model_type, model_name):
    """Get specific SDXL model information"""
    models = get_sdxl_models()
    return models.get(model_type, {}).get(model_name)

if __name__ == "__main__":
    # Test the model definitions
    models = get_sdxl_models()
    print("SDXL Model Definitions:")
    for model_type, model_dict in models.items():
        print(f"\n{model_type.upper()}: {len(model_dict)} models")
        for name, info in list(model_dict.items())[:3]:  # Show first 3
            print(f"  - {name}: {info['description']}")