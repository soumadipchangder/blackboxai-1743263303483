from typing import Dict, List
import pandas as pd
from datetime import datetime, timedelta

class ProjectTrackingAgent:
    def __init__(self):
        self.projects = {}  # Stores project state
        self.metric_weights = {
            'schedule_variance': 0.3,
            'budget_variance': 0.25,
            'resource_changes': 0.2,
            'quality_metrics': 0.15,
            'stakeholder_satisfaction': 0.1
        }

    def update_project_status(self, project_id: str, metrics: Dict) -> Dict:
        """Update and return current project status"""
        if project_id not in self.projects:
            self.projects[project_id] = {
                'history': [],
                'current_status': {}
            }
        
        # Calculate composite health score
        health_score = self._calculate_health_score(metrics)
        
        # Store update
        update = {
            'timestamp': datetime.now().isoformat(),
            'metrics': metrics,
            'health_score': health_score,
            'trend': self._calculate_trend(project_id, health_score)
        }
        
        self.projects[project_id]['history'].append(update)
        self.projects[project_id]['current_status'] = update
        
        return update

    def get_project_status(self, project_id: str) -> Dict:
        """Get current status of a project"""
        return self.projects.get(project_id, {}).get('current_status', {})

    def _calculate_health_score(self, metrics: Dict) -> float:
        """Calculate weighted health score from metrics"""
        score = 0.0
        for metric, weight in self.metric_weights.items():
            value = metrics.get(metric, 0)
            # Normalize values to 0-1 range where 1 is best
            if metric in ['schedule_variance', 'budget_variance']:
                value = 1 - min(abs(value), 1)  # Invert variance metrics
            score += value * weight
        return round(score, 2)

    def _calculate_trend(self, project_id: str, current_score: float) -> str:
        """Determine trend based on historical data"""
        history = self.projects.get(project_id, {}).get('history', [])
        if len(history) < 2:
            return 'neutral'
        
        # Get last 3 scores for trend analysis
        recent_scores = [h['health_score'] for h in history[-3:]]
        recent_scores.append(current_score)
        
        # Simple linear regression for trend
        x = range(len(recent_scores))
        y = recent_scores
        covariance = sum((xi - sum(x)/len(x)) * (yi - sum(y)/len(y)) for xi, yi in zip(x, y))
        variance = sum((xi - sum(x)/len(x))**2 for xi in x)
        
        if variance == 0:
            return 'neutral'
            
        slope = covariance / variance
        if slope > 0.05:
            return 'improving'
        elif slope < -0.05:
            return 'deteriorating'
        return 'stable'

    def detect_anomalies(self, project_id: str) -> List[Dict]:
        """Detect anomalies in project metrics"""
        status = self.get_project_status(project_id)
        anomalies = []
        
        # Example anomaly detection
        if status.get('metrics', {}).get('schedule_variance', 0) > 0.2:
            anomalies.append({
                'type': 'schedule',
                'severity': 'high',
                'message': 'Significant schedule variance detected'
            })
            
        if status.get('metrics', {}).get('resource_changes', 0) > 0.3:
            anomalies.append({
                'type': 'resources',
                'severity': 'medium',
                'message': 'High resource turnover detected'
            })
            
        return anomalies