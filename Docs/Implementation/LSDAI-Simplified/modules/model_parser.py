#!/usr/bin/env python3
"""
LSDAI Simplified Model Parser
Text-based model shopping cart system
"""

import re
from typing import Dict, List, Any, Optional
from urllib.parse import urlparse

class ModelTextParser:
    """Simple text-based model parser for shopping cart system"""
    
    def __init__(self):
        self.categories = ['$ckpt', '$lora', '$vae', '$controlnet', '$embeddings']
        self.supported_hosts = [
            'civitai.com', 'huggingface.co', 'github.com', 
            'drive.google.com', 'mega.nz'
        ]
    
    def parse_text_input(self, text: str) -> Dict[str, Dict[str, List[Dict[str, str]]]]:
        """Parse text input and categorize models"""
        models = {
            'sd15': {'ckpt': [], 'lora': [], 'vae': [], 'controlnet': [], 'embeddings': []},
            'sdxl': {'ckpt': [], 'lora': [], 'vae': [], 'controlnet': [], 'embeddings': []}
        }
        
        current_category = None
        lines = text.strip().split('\n')
        
        for line in lines:
            line = line.strip()
            if not line:
                continue
            
            # Check for category markers
            if line in self.categories:
                current_category = line[1:]  # Remove $ prefix
                continue
            
            # Parse model URLs
            if current_category and self._is_valid_url(line):
                # Extract model info from URL
                model_info = self._extract_model_info(line)
                if model_info:
                    # Categorize as SD1.5 or SDXL
                    category = self._categorize_model(line, model_info)
                    if category in models and current_category in models[category]:
                        models[category][current_category].append(model_info)
        
        return models
    
    def _is_valid_url(self, text: str) -> bool:
        """Check if text is a valid URL"""
        try:
            result = urlparse(text)
            return all([result.scheme, result.netloc])
        except:
            return False
    
    def _extract_model_info(self, url: str) -> Optional[Dict[str, str]]:
        """Extract model information from URL"""
        # Handle URLs with custom names [Model Name]
        if '[' in url and ']' in url:
            name_start = url.find('[') + 1
            name_end = url.find(']')
            name = url[name_start:name_end].strip()
            clean_url = url.split('[')[0].strip()
        else:
            # Extract name from URL
            parsed = urlparse(url)
            name = parsed.path.split('/')[-1]
            clean_url = url
        
        # Clean up name
        name = self._clean_filename(name)
        
        # Determine file extension
        extension = self._get_file_extension(url)
        if not extension:
            extension = '.safetensors'  # Default extension
        
        return {
            'url': clean_url,
            'name': name,
            'filename': f"{name}{extension}",
            'extension': extension,
            'host': self._get_host_name(clean_url)
        }
    
    def _clean_filename(self, filename: str) -> str:
        """Clean filename for safe file system usage"""
        # Remove common file extensions
        filename = re.sub(r'\.(safetensors|ckpt|pt|bin|pth|vae)$', '', filename, flags=re.IGNORECASE)
        
        # Remove special characters and spaces
        filename = re.sub(r'[^\w\s-]', '', filename)
        filename = re.sub(r'[-\s]+', '-', filename)
        
        # Remove leading/trailing hyphens
        filename = filename.strip('-')
        
        return filename if filename else 'model'
    
    def _get_file_extension(self, url: str) -> str:
        """Determine file extension from URL or context"""
        # Check for explicit extensions in URL
        if '.safetensors' in url.lower():
            return '.safetensors'
        elif '.ckpt' in url.lower():
            return '.ckpt'
        elif '.pt' in url.lower():
            return '.pt'
        elif '.bin' in url.lower():
            return '.bin'
        elif '.pth' in url.lower():
            return '.pth'
        elif '.vae' in url.lower():
            return '.vae'
        
        return ''
    
    def _get_host_name(self, url: str) -> str:
        """Extract host name from URL"""
        try:
            parsed = urlparse(url)
            return parsed.netloc
        except:
            return 'unknown'
    
    def _categorize_model(self, url: str, model_info: Dict[str, str]) -> str:
        """Categorize model as SD1.5 or SDXL"""
        url_lower = url.lower()
        name_lower = model_info['name'].lower()
        
        # Check for SDXL indicators
        sdxl_indicators = [
            'sdxl', 'xl', 'sd xl', 'stablediffusion xl',
            'sd_xl', 'stable-xl', 'stablediffusion-xl'
        ]
        
        # Check for SD1.5 indicators
        sd15_indicators = [
            'sd1.5', 'sd 1.5', 'sd15', 'stable-diffusion-1.5',
            'sd_1_5', 'stable-diffusion-1-5'
        ]
        
        # Check URL and name for indicators
        text_to_check = f"{url_lower} {name_lower}"
        
        for indicator in sdxl_indicators:
            if indicator in text_to_check:
                return 'sdxl'
        
        for indicator in sd15_indicators:
            if indicator in text_to_check:
                return 'sd15'
        
        # Default to SD1.5 if no clear indicators
        return 'sd15'
    
    def validate_models(self, models: Dict[str, Dict[str, List[Dict[str, str]]]]) -> Dict[str, Any]:
        """Validate parsed models and return validation results"""
        validation = {
            'valid': True,
            'warnings': [],
            'errors': [],
            'total_models': 0,
            'by_category': {}
        }
        
        for sd_type, categories in models.items():
            validation['by_category'][sd_type] = {}
            for category, model_list in categories.items():
                validation['by_category'][sd_type][category] = len(model_list)
                validation['total_models'] += len(model_list)
                
                for model in model_list:
                    # Validate URL
                    if not self._is_valid_url(model['url']):
                        validation['errors'].append(f"Invalid URL: {model['url']}")
                        validation['valid'] = False
                    
                    # Check for supported hosts
                    if model['host'] not in self.supported_hosts:
                        validation['warnings'].append(
                            f"Unsupported host '{model['host']}' for model: {model['name']}"
                        )
                    
                    # Check filename length
                    if len(model['filename']) > 255:
                        validation['warnings'].append(
                            f"Very long filename: {model['filename']}"
                        )
        
        return validation
    
    def format_models_summary(self, models: Dict[str, Dict[str, List[Dict[str, str]]]]) -> str:
        """Format models summary for display"""
        summary = []
        summary.append("📋 Model Summary")
        summary.append("=" * 30)
        
        total_models = 0
        for sd_type, categories in models.items():
            sd_total = sum(len(model_list) for model_list in categories.values())
            total_models += sd_total
            
            if sd_total > 0:
                summary.append(f"\n{sd_type.upper()} Models ({sd_total}):")
                for category, model_list in categories.items():
                    if model_list:
                        summary.append(f"  {category}: {len(model_list)} models")
                        for model in model_list[:3]:  # Show first 3 models
                            summary.append(f"    - {model['name']}")
                        if len(model_list) > 3:
                            summary.append(f"    ... and {len(model_list) - 3} more")
        
        if total_models == 0:
            summary.append("No models found")
        
        return '\n'.join(summary)
    
    def get_download_list(self, models: Dict[str, Dict[str, List[Dict[str, str]]]]) -> List[Dict[str, Any]]:
        """Get flat list of models for downloading"""
        download_list = []
        
        for sd_type, categories in models.items():
            for category, model_list in categories.items():
                for model in model_list:
                    download_item = {
                        'url': model['url'],
                        'name': model['name'],
                        'filename': model['filename'],
                        'category': category,
                        'sd_type': sd_type,
                        'target_path': f"shared_models/{self._get_category_path(category)}/{model['filename']}"
                    }
                    download_list.append(download_item)
        
        return download_list
    
    def _get_category_path(self, category: str) -> str:
        """Get file system path for a category"""
        category_paths = {
            'ckpt': 'Stable-diffusion',
            'lora': 'Lora',
            'vae': 'VAE',
            'controlnet': 'ControlNet',
            'embeddings': 'embeddings'
        }
        return category_paths.get(category, 'Other')

# Global model parser instance
_model_parser = None

def get_model_parser():
    """Get global model parser instance"""
    global _model_parser
    if _model_parser is None:
        _model_parser = ModelTextParser()
    return _model_parser