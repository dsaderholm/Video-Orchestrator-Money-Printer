# src/main.py
from flask import Flask, render_template, request, jsonify
from .config import load_config
from .api_handler import APIHandler
from .scheduler import Scheduler
from .file_manager import FileManager
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'default-secret-key')

# Initialize components
api_handler = APIHandler()
scheduler = Scheduler()
file_manager = FileManager()

@app.route('/')
def index():
    apis = api_handler.get_all_status()
    activities = scheduler.get_recent_activities()
    return render_template('index.html', apis=apis, activities=activities)

@app.route('/api_config')
def api_config():
    creator_apis = api_handler.get_apis_by_type('creator')
    utility_apis = api_handler.get_apis_by_type('utility')
    uploader_apis = api_handler.get_apis_by_type('uploader')
    return render_template('api_config.html', 
                         creator_apis=creator_apis,
                         utility_apis=utility_apis,
                         uploader_apis=uploader_apis)

@app.route('/schedule')
def schedule():
    video_types = api_handler.get_video_types()
    accounts = api_handler.get_accounts()
    processing_steps = api_handler.get_processing_steps()
    schedules = scheduler.get_all_schedules()
    return render_template('schedule.html',
                         video_types=video_types,
                         accounts=accounts,
                         processing_steps=processing_steps,
                         schedules=schedules)

@app.route('/api/config/save', methods=['POST'])
def save_api_config():
    try:
        data = request.form.to_dict()
        api_handler.save_config(data)
        return jsonify({'success': True, 'message': 'Configuration saved successfully'})
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)})

@app.route('/api/schedule/save', methods=['POST'])
def save_schedule():
    try:
        data = request.form.to_dict()
        scheduler.save_schedule(data)
        return jsonify({'success': True, 'message': 'Schedule saved successfully'})
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)})

@app.route('/api/test/<api_id>', methods=['GET'])
def test_api(api_id):
    try:
        result = api_handler.test_connection(api_id)
        return jsonify({'success': True, 'message': 'API test successful'})
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)