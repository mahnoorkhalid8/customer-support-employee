"""
Metrics Service - Track statistics for dashboard
In-memory storage for email and WhatsApp metrics
"""
from datetime import datetime, timedelta
from typing import Dict, List
from collections import defaultdict
import threading

class MetricsService:
    _instance = None
    _lock = threading.Lock()

    def __new__(cls):
        if cls._instance is None:
            with cls._lock:
                if cls._instance is None:
                    cls._instance = super().__new__(cls)
                    cls._instance._initialize()
        return cls._instance

    def _initialize(self):
        """Initialize metrics storage"""
        self.email_stats = {
            'total': 0,
            'success': 0,
            'failed': 0,
            'activity': []  # List of {timestamp, count}
        }

        self.whatsapp_stats = {
            'total': 0,
            'success': 0,
            'failed': 0,
            'activity': []  # List of {timestamp, count}
        }

        # Hourly activity counters
        self.email_hourly = defaultdict(int)
        self.whatsapp_hourly = defaultdict(int)

    def record_email_processed(self, success: bool = True):
        """Record an email being processed"""
        with self._lock:
            self.email_stats['total'] += 1
            if success:
                self.email_stats['success'] += 1
            else:
                self.email_stats['failed'] += 1

            # Record hourly activity
            hour_key = datetime.now().strftime('%Y-%m-%d %H:00')
            self.email_hourly[hour_key] += 1

    def record_whatsapp_processed(self, success: bool = True):
        """Record a WhatsApp message being processed"""
        with self._lock:
            self.whatsapp_stats['total'] += 1
            if success:
                self.whatsapp_stats['success'] += 1
            else:
                self.whatsapp_stats['failed'] += 1

            # Record hourly activity
            hour_key = datetime.now().strftime('%Y-%m-%d %H:00')
            self.whatsapp_hourly[hour_key] += 1

    def get_email_stats(self) -> Dict:
        """Get email statistics"""
        with self._lock:
            total = self.email_stats['total']
            success = self.email_stats['success']
            failed = self.email_stats['failed']

            success_rate = round((success / total * 100) if total > 0 else 0, 1)

            return {
                'total': total,
                'success': success,
                'failed': failed,
                'success_rate': success_rate
            }

    def get_whatsapp_stats(self) -> Dict:
        """Get WhatsApp statistics"""
        with self._lock:
            total = self.whatsapp_stats['total']
            success = self.whatsapp_stats['success']
            failed = self.whatsapp_stats['failed']

            success_rate = round((success / total * 100) if total > 0 else 0, 1)

            return {
                'total': total,
                'success': success,
                'failed': failed,
                'success_rate': success_rate
            }

    def get_email_activity(self, hours: int = 24) -> List[Dict]:
        """Get email activity for the last N hours"""
        with self._lock:
            now = datetime.now()
            activity = []

            for i in range(hours):
                hour = now - timedelta(hours=hours-i-1)
                hour_key = hour.strftime('%Y-%m-%d %H:00')
                count = self.email_hourly.get(hour_key, 0)

                activity.append({
                    'time': hour.strftime('%I %p').lstrip('0'),
                    'emails': count
                })

            return activity

    def get_whatsapp_activity(self, hours: int = 24) -> List[Dict]:
        """Get WhatsApp activity for the last N hours"""
        with self._lock:
            now = datetime.now()
            activity = []

            for i in range(hours):
                hour = now - timedelta(hours=hours-i-1)
                hour_key = hour.strftime('%Y-%m-%d %H:00')
                count = self.whatsapp_hourly.get(hour_key, 0)

                activity.append({
                    'time': hour.strftime('%I %p').lstrip('0'),
                    'messages': count
                })

            return activity

    def reset_stats(self):
        """Reset all statistics (for testing)"""
        with self._lock:
            self._initialize()


# Singleton instance
metrics_service = MetricsService()
