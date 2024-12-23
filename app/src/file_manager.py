import os
import shutil
from datetime import datetime

class FileManager:
    def __init__(self):
        self.temp_dir = os.getenv('UPLOAD_FOLDER', 'temp')
        os.makedirs(self.temp_dir, exist_ok=True)

    def create_temp_directory(self):
        """Create a new temporary directory for processing"""
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        temp_path = os.path.join(self.temp_dir, f'process_{timestamp}')
        os.makedirs(temp_path, exist_ok=True)
        return temp_path

    def clean_temp_files(self, directory):
        """Clean up temporary files after processing"""
        try:
            shutil.rmtree(directory)
        except Exception as e:
            print(f"Error cleaning temporary files: {e}")

    def save_upload(self, file, directory):
        """Save uploaded file to temporary directory"""
        if file and self._allowed_file(file.filename):
            filename = os.path.join(directory, file.filename)
            file.save(filename)
            return filename
        return None

    def _allowed_file(self, filename):
        """Check if file type is allowed"""
        return '.' in filename and \
               filename.rsplit('.', 1)[1].lower() in {'mp4', 'mov', 'avi'}
