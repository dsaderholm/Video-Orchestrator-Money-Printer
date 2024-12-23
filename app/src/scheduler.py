from flask_apscheduler import APScheduler
from datetime import datetime
import json
from .config import load_config, save_config

class Scheduler:
    def __init__(self):
        self.scheduler = APScheduler()
        self.scheduler.start()
        self.config = load_config()
        self._init_schedules()

    def _init_schedules(self):
        """Initialize schedules from config"""
        for schedule in self.config.get('schedules', []):
            self._add_job(schedule)

    def _add_job(self, schedule):
        """Add a job to the scheduler"""
        job_id = f"schedule_{schedule['id']}"
        if schedule['frequency'] == 'daily':
            self.scheduler.add_job(
                id=job_id,
                func=self._execute_schedule,
                trigger='cron',
                hour=schedule.get('hour', 0),
                minute=schedule.get('minute', 0),
                args=[schedule['id']]
            )
        elif schedule['frequency'] == 'weekly':
            self.scheduler.add_job(
                id=job_id,
                func=self._execute_schedule,
                trigger='cron',
                day_of_week=schedule.get('day', 0),
                hour=schedule.get('hour', 0),
                minute=schedule.get('minute', 0),
                args=[schedule['id']]
            )
        elif schedule['frequency'] == 'custom':
            self.scheduler.add_job(
                id=job_id,
                func=self._execute_schedule,
                trigger='cron',
                **schedule['cron'],
                args=[schedule['id']]
            )

    def _execute_schedule(self, schedule_id):
        """Execute a scheduled job"""
        schedule = next((s for s in self.config.get('schedules', [])
                        if s['id'] == schedule_id), None)
        if not schedule:
            return

        # Log activity
        self._log_activity({
            'timestamp': datetime.now().isoformat(),
            'schedule_id': schedule_id,
            'status': 'started',
            'message': f"Started processing schedule {schedule['name']}"
        })

    def save_schedule(self, data):
        """Save a new or update existing schedule"""
        schedule_id = data.get('id', str(len(self.config.get('schedules', [])) + 1))
        schedules = self.config.get('schedules', [])
        
        # Update existing or add new
        for schedule in schedules:
            if schedule['id'] == schedule_id:
                schedule.update(data)
                break
        else:
            data['id'] = schedule_id
            schedules.append(data)
        
        self.config['schedules'] = schedules
        save_config(self.config)
        
        # Update scheduler
        self._add_job(data)

    def get_all_schedules(self):
        """Get all configured schedules"""
        return self.config.get('schedules', [])

    def get_recent_activities(self):
        """Get recent schedule activities"""
        activities = self.config.get('activities', [])
        return sorted(activities, 
                     key=lambda x: x['timestamp'],
                     reverse=True)[:10]

    def _log_activity(self, activity):
        """Log a schedule activity"""
        activities = self.config.get('activities', [])
        activities.append(activity)
        
        # Keep only last 100 activities
        self.config['activities'] = activities[-100:]
        save_config(self.config)