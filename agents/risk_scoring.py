from typing import Dict, List
import numpy as np
from datetime import datetime

class RiskScoringAgent:
    def __init__(self):
        self.risk_factors = {
            'financial': 0.4,
            'schedule': 0.3,
            'resources': 0.2,
            'technical': 0.1
        }
        self.thresholds = {
            'critical': 0.8,
            'high': 0.6,
            'medium': 0.4,
            'low': 0.2
        }

    def calculate_project_risk(self, project_data: Dict) -> Dict:
        """Calculate comprehensive risk score for a project"""
        scores = {
            'financial': self._assess_financial_risk(project_data),
            'schedule': self._assess_schedule_risk(project_data),
            'resources': self._assess_resource_risk(project_data),
            'technical': self._assess_technical_risk(project_data)
        }

        # Calculate weighted risk score
        total_score = sum(
            score * self.risk_factors[factor]
            for factor, score in scores.items()
        )

        # Determine risk level
        risk_level = self._determine_risk_level(total_score)

        return {
            'score': round(total_score, 2),
            'level': risk_level,
            'factors': scores,
            'timestamp': datetime.now().isoformat()
        }

    def _assess_financial_risk(self, data: Dict) -> float:
        """Assess financial risk factors"""
        budget_variance = data.get('budget_variance', 0)
        payment_delays = data.get('payment_delays', 0)
        return min(1.0, (abs(budget_variance) * 0.5 + payment_delays * 0.5))

    def _assess_schedule_risk(self, data: Dict) -> float:
        """Assess schedule risk factors"""
        delay_percentage = data.get('schedule_delay', 0)
        milestone_misses = data.get('missed_milestones', 0)
        return min(1.0, (delay_percentage * 0.7 + milestone_misses * 0.3))

    def _assess_resource_risk(self, data: Dict) -> float:
        """Assess resource risk factors"""
        attrition_rate = data.get('attrition_rate', 0)
        skill_gaps = data.get('skill_gaps', 0)
        return min(1.0, (attrition_rate * 0.6 + skill_gaps * 0.4))

    def _assess_technical_risk(self, data: Dict) -> float:
        """Assess technical risk factors"""
        defect_rate = data.get('defect_rate', 0)
        tech_debt = data.get('tech_debt', 0)
        return min(1.0, (defect_rate * 0.5 + tech_debt * 0.5))

    def _determine_risk_level(self, score: float) -> str:
        """Determine risk level based on score"""
        if score >= self.thresholds['critical']:
            return 'critical'
        elif score >= self.thresholds['high']:
            return 'high'
        elif score >= self.thresholds['medium']:
            return 'medium'
        return 'low'