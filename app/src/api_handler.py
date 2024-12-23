import requests
import json
from .config import load_config, save_config

class APIHandler:
    def __init__(self):
        self.config = load_config()

    def get_all_status(self):
        """Get status of all configured APIs"""
        apis = []
        for api in self.config.get('apis', []):
            try:
                status = self.test_connection(api['id'])
                apis.append({
                    'name': api['name'],
                    'status': 'active' if status else 'inactive'
                })
            except:
                apis.append({
                    'name': api['name'],
                    'status': 'inactive'
                })
        return apis

    def get_apis_by_type(self, api_type):
        """Get all APIs of a specific type"""
        return [api for api in self.config.get('apis', [])
                if api.get('type') == api_type]

    def save_config(self, data):
        """Save API configuration"""
        api_id = data.get('id')
        api_configs = self.config.get('apis', [])
        
        # Update existing or add new
        for api in api_configs:
            if api['id'] == api_id:
                api.update(data)
                break
        else:
            api_configs.append(data)
        
        self.config['apis'] = api_configs
        save_config(self.config)

    def test_connection(self, api_id):
        """Test API connection"""
        api = next((a for a in self.config.get('apis', [])
                   if a['id'] == api_id), None)
        if not api:
            raise ValueError(f"API {api_id} not found")
            
        try:
            response = requests.get(api['url'])
            return response.status_code == 200
        except:
            return False

    def get_video_types(self):
        """Get available video types"""
        return [
            {'id': 'trivia', 'name': 'Trivia Videos'},
            {'id': 'would_you_rather', 'name': 'Would You Rather'},
            # Add more video types as needed
        ]

    def get_accounts(self):
        """Get configured social media accounts"""
        return [
            {'id': acc['id'], 'name': acc['name']}
            for acc in self.config.get('accounts', [])
        ]

    def get_processing_steps(self):
        """Get available processing steps"""
        return [
            {'id': 'captions', 'name': 'Add Captions'},
            {'id': 'thumbnail', 'name': 'Generate Thumbnail'},
            # Add more processing steps as needed
        ]
