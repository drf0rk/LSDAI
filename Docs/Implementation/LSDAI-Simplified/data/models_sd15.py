#!/usr/bin/env python3
"""
LSDAI Simplified - SD1.5 Model Definitions
Sample popular SD1.5 models for reference
"""

# Popular SD1.5 Checkpoint Models
SD15_CHECKPOINTS = {
    "Realistic Vision": {
        "url": "https://civitai.com/api/download/models/130072",
        "description": "Photorealistic SD1.5 model",
        "filename": "realisticVisionV51_v51VAE.safetensors"
    },
    "Deliberate": {
        "url": "https://civitai.com/api/download/models/152368", 
        "description": "Artistic and realistic model",
        "filename": "deliberate_v3.safetensors"
    },
    "DreamShaper": {
        "url": "https://civitai.com/api/download/models/128713",
        "description": "Versatile artistic model",
        "filename": "dreamshaper_8.safetensors"
    },
    "Realistic Stock Photo": {
        "url": "https://civitai.com/api/download/models/137883",
        "description": "Stock photo style model",
        "filename": "realisticStockPhoto_v20.safetensors"
    },
    "Epic Realism": {
        "url": "https://civitai.com/api/download/models/134060",
        "description": "Highly realistic model",
        "filename": "epicRealism.safetensors"
    }
}

# Popular SD1.5 LoRA Models
SD15_LORAS = {
    "Detail Tweaker": {
        "url": "https://civitai.com/api/download/models/62833",
        "description": "Enhance image details",
        "filename": "detail_tweaker.safetensors"
    },
    "Epic Realism Helper": {
        "url": "https://civitai.com/api/download/models/139504",
        "description": "Helper for Epic Realism model",
        "filename": "epic_realism_helper.safetensors"
    },
    "SDXL Illustration Helper": {
        "url": "https://civitai.com/api/download/models/139504",
        "description": "Illustration style helper",
        "filename": "illustration_helper.safetensors"
    }
}

# Popular SD1.5 VAE Files
SD15_VAES = {
    "VAE vae-ft-mse-840000-ema-pruned": {
        "url": "https://huggingface.co/stabilityai/sd-vae-ft-mse-original/resolve/main/vae-ft-mse-840000-ema-pruned.safetensors",
        "description": "Standard SD1.5 VAE",
        "filename": "vae-ft-mse-840000-ema-pruned.safetensors"
    },
    "VAE vae-ft-mse-original": {
        "url": "https://huggingface.co/stabilityai/sd-vae-ft-mse-original/resolve/main/vae-ft-mse-original.safetensors", 
        "description": "Original MSE VAE",
        "filename": "vae-ft-mse-original.safetensors"
    }
}

# Popular SD1.5 ControlNet Models
SD15_CONTROLNET = {
    "Canny": {
        "url": "https://huggingface.co/lllyasviel/ControlNet-v1-1/resolve/main/control_v11p_sd15_canny.pth",
        "description": "Canny edge detection",
        "filename": "control_v11p_sd15_canny.pth"
    },
    "Depth": {
        "url": "https://huggingface.co/lllyasviel/ControlNet-v1-1/resolve/main/control_v11f1p_sd15_depth.pth",
        "description": "Depth map control",
        "filename": "control_v11f1p_sd15_depth.pth"
    },
    "Pose": {
        "url": "https://huggingface.co/lllyasviel/ControlNet-v1-1/resolve/main/control_v11p_sd15_openpose.pth",
        "description": "Human pose estimation",
        "filename": "control_v11p_sd15_openpose.pth"
    },
    "Scribble": {
        "url": "https://huggingface.co/lllyasviel/ControlNet-v1-1/resolve/main/control_v11p_sd15_scribble.pth", 
        "description": "Scribble to image",
        "filename": "control_v11p_sd15_scribble.pth"
    }
}

# Popular SD1.5 Textual Inversions/Embeddings
SD15_EMBEDDINGS = {
    "Bad Artist": {
        "url": "https://huggingface.co/datasets/Nerfgun3/bad_artist/resolve/main/bad_artist.pt",
        "description": "Negative embedding for art quality",
        "filename": "bad_artist.pt"
    },
    "Bad Hands": {
        "url": "https://huggingface.co/yesyeahvh/bad-hands-5/resolve/main/bad-hands-5.pt",
        "description": "Fix bad hand generation",
        "filename": "bad-hands-5.pt"
    },
    "Easy Negative": {
        "url": "https://huggingface.co/datasets/Nerfgun3/bad_prompt/resolve/main/bad_prompt_version2.pt",
        "description": "Negative prompt embedding",
        "filename": "bad_prompt_version2.pt"
    }
}

def get_sd15_models():
    """Get all SD1.5 models"""
    return {
        'ckpt': SD15_CHECKPOINTS,
        'lora': SD15_LORAS,
        'vae': SD15_VAES,
        'controlnet': SD15_CONTROLNET,
        'embeddings': SD15_EMBEDDINGS
    }

def get_sd15_model_info(model_type, model_name):
    """Get specific SD1.5 model information"""
    models = get_sd15_models()
    return models.get(model_type, {}).get(model_name)

if __name__ == "__main__":
    # Test the model definitions
    models = get_sd15_models()
    print("SD1.5 Model Definitions:")
    for model_type, model_dict in models.items():
        print(f"\n{model_type.upper()}: {len(model_dict)} models")
        for name, info in list(model_dict.items())[:3]:  # Show first 3
            print(f"  - {name}: {info['description']}")