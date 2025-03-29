from typing import Dict, List
from datetime import datetime
import json
from jinja2 import Template
import smtplib
from email.mime.text import MIMEText

class ReportingAgent:
    def __init__(self):
        self.templates = {
            'risk_report': """
            <html>
            <head><title>Risk Report for {{project_id}}</title></head>
            <body>
                <h1>Risk Assessment Report</h1>
                <p>Generated at: {{timestamp}}</p>
                
                <h2>Project: {{project_id}}</h2>
                <p>Overall Risk Score: <strong>{{risk_score}} ({{risk_level}})</strong></p>
                
                <h3>Risk Factors</h3>
                <ul>
                {% for factor, score in risk_factors.items() %}
                    <li>{{factor|title}}: {{score|round(2)}}</li>
                {% endfor %}
                </ul>
                
                <h3>Recommendations</h3>
                <ol>
                {% for rec in recommendations %}
                    <li>{{rec}}</li>
                {% endfor %}
                </ol>
            </body>
            </html>
            """,
            'alert': """
            [ALERT] Project {{project_id}} - {{risk_level}} risk detected!
            
            Risk Score: {{risk_score}}
            Key Factors:
            {% for factor, score in top_factors %}
            - {{factor}}: {{score}}
            {% endfor %}
            
            Immediate Actions Recommended:
            {% for action in actions %}
            * {{action}}
            {% endfor %}
            """
        }
        self.alert_rules = {
            'critical': {'email': True, 'sms': True},
            'high': {'email': True, 'sms': False},
            'medium': {'email': True, 'sms': False}
        }

    def generate_risk_report(self, project_id: str, risk_data: Dict) -> str:
        """Generate HTML risk report"""
        template = Template(self.templates['risk_report'])
        recommendations = self._generate_recommendations(risk_data)
        
        return template.render(
            project_id=project_id,
            timestamp=datetime.now().isoformat(),
            risk_score=risk_data['score'],
            risk_level=risk_data['level'],
            risk_factors=risk_data['factors'],
            recommendations=recommendations
        )

    def send_alert(self, project_id: str, risk_data: Dict) -> bool:
        """Send risk alert based on severity"""
        if risk_data['level'] not in self.alert_rules:
            return False
            
        rules = self.alert_rules[risk_data['level']]
        top_factors = sorted(
            risk_data['factors'].items(),
            key=lambda x: x[1],
            reverse=True
        )[:3]
        
        actions = self._generate_actions(risk_data)
        template = Template(self.templates['alert'])
        message = template.render(
            project_id=project_id,
            risk_level=risk_data['level'],
            risk_score=risk_data['score'],
            top_factors=top_factors,
            actions=actions
        )
        
        # Example email sending (would need SMTP config)
        if rules['email']:
            try:
                msg = MIMEText(message)
                msg['Subject'] = f"Risk Alert: {project_id} - {risk_data['level']}"
                msg['From'] = 'risk-system@company.com'
                msg['To'] = 'project-managers@company.com'
                
                # In production, would use actual SMTP server
                # with smtplib.SMTP('smtp.company.com') as server:
                #     server.send_message(msg)
                print(f"Would send email alert: {msg.as_string()}")
                return True
            except Exception as e:
                print(f"Failed to send alert: {str(e)}")
                return False
        return True

    def _generate_recommendations(self, risk_data: Dict) -> List[str]:
        """Generate risk mitigation recommendations"""
        recommendations = []
        level = risk_data['level']
        
        if level in ['critical', 'high']:
            recommendations.append(
                "Immediate executive review required"
            )
        
        if risk_data['factors']['financial'] > 0.5:
            recommendations.append(
                "Review project budget and payment terms"
            )
            
        if risk_data['factors']['schedule'] > 0.4:
            recommendations.append(
                "Re-evaluate project timeline and milestones"
            )
            
        if risk_data['factors']['resources'] > 0.3:
            recommendations.append(
                "Assess team composition and resource allocation"
            )
            
        if len(recommendations) == 0:
            recommendations.append(
                "Continue current risk mitigation strategies"
            )
            
        return recommendations

    def _generate_actions(self, risk_data: Dict) -> List[str]:
        """Generate immediate action items for alerts"""
        actions = []
        if risk_data['level'] == 'critical':
            actions.append("Escalate to senior leadership immediately")
            actions.append("Convene emergency risk mitigation meeting")
        elif risk_data['level'] == 'high':
            actions.append("Schedule risk review meeting within 24 hours")
        
        if risk_data['factors']['schedule'] > 0.6:
            actions.append("Identify critical path tasks for acceleration")
            
        if risk_data['factors']['financial'] > 0.7:
            actions.append("Freeze non-essential project expenditures")
            
        return actions

    def save_report(self, report: str, filename: str) -> bool:
        """Save report to file"""
        try:
            with open(filename, 'w') as f:
                f.write(report)
            return True
        except Exception as e:
            print(f"Failed to save report: {str(e)}")
            return False