from fastapi import APIRouter, HTTPException
from fastapi.responses import HTMLResponse, JSONResponse
from datetime import datetime
import random
from agents.risk_scoring import RiskScoringAgent
from agents.project_tracking import ProjectTrackingAgent
from agents.reporting import ReportingAgent

router = APIRouter()
risk_agent = RiskScoringAgent()
project_agent = ProjectTrackingAgent()
reporting_agent = ReportingAgent()

# Sample project data
sample_projects = {
    "project-001": {
        "name": "E-Commerce Platform",
        "description": "New online shopping platform development",
        "team_size": 12,
        "start_date": "2023-01-15",
        "end_date": "2023-09-30"
    },
    "project-002": {
        "name": "Mobile Banking App",
        "description": "Cross-platform mobile banking application",
        "team_size": 8,
        "start_date": "2023-03-01",
        "end_date": "2023-11-15"
    }
}

@router.get("/project/{project_id}/risk", response_class=JSONResponse)
async def get_project_risk(project_id: str):
    """Get current risk assessment for a project"""
    if project_id not in sample_projects:
        raise HTTPException(status_code=404, detail="Project not found")
    
    # Generate sample metrics (in real app would come from database)
    metrics = {
        "budget_variance": random.uniform(0, 0.3),
        "payment_delays": random.randint(0, 3),
        "schedule_delay": random.uniform(0, 0.4),
        "missed_milestones": random.randint(0, 2),
        "attrition_rate": random.uniform(0, 0.2),
        "skill_gaps": random.uniform(0, 0.15),
        "defect_rate": random.uniform(0, 0.25),
        "tech_debt": random.uniform(0, 0.2)
    }
    
    # Update project status with these metrics
    project_agent.update_project_status(project_id, metrics)
    
    # Calculate risk score
    risk_data = risk_agent.calculate_project_risk(metrics)
    
    # Generate report (not used in this endpoint but available)
    report = reporting_agent.generate_risk_report(project_id, risk_data)
    
    # Check if we need to send alerts
    if risk_data['level'] in ['critical', 'high']:
        reporting_agent.send_alert(project_id, risk_data)
    
    return {
        "project": sample_projects[project_id],
        "metrics": metrics,
        "risk": risk_data,
        "timestamp": datetime.now().isoformat()
    }

@router.get("/project/{project_id}/alerts", response_class=JSONResponse)
async def get_project_alerts(project_id: str):
    """Get recent alerts for a project"""
    if project_id not in sample_projects:
        raise HTTPException(status_code=404, detail="Project not found")
    
    # Generate sample alerts
    alerts = []
    for i in range(3):
        alerts.append({
            "id": f"alert-{i}",
            "project_id": project_id,
            "title": f"Sample Alert {i+1}",
            "message": f"This is a sample alert message about potential risks in {sample_projects[project_id]['name']}",
            "severity": random.choice(["low", "medium", "high", "critical"]),
            "timestamp": datetime.now().isoformat()
        })
    
    return {"alerts": alerts}

@router.get("/project/{project_id}/report", response_class=HTMLResponse)
async def get_project_report(project_id: str):
    """Generate HTML risk report for a project"""
    if project_id not in sample_projects:
        raise HTTPException(status_code=404, detail="Project not found")
    
    # Generate sample risk data
    risk_data = {
        "score": random.uniform(0.1, 0.9),
        "level": random.choice(["low", "medium", "high", "critical"]),
        "factors": {
            "financial": random.uniform(0.1, 0.9),
            "schedule": random.uniform(0.1, 0.9),
            "resources": random.uniform(0.1, 0.9),
            "technical": random.uniform(0.1, 0.9)
        }
    }
    
    return reporting_agent.generate_risk_report(project_id, risk_data)

@router.post("/chat")
async def handle_chat_message(message: dict):
    """Handle chat messages and return AI response"""
    user_message = message.get("text", "")
    
    # Simple response logic (in real app would use NLP)
    if "risk" in user_message.lower():
        return {"response": "The current risk level is medium. The main factors are schedule delay (45%) and budget variance (30%)."}
    elif "schedule" in user_message.lower():
        return {"response": "The project is currently 2 weeks behind schedule. The risk factor is 0.45 (medium)."}
    elif "budget" in user_message.lower():
        return {"response": "Current budget utilization is at 65%. The risk factor is 0.30 (low)."}
    else:
        return {"response": "I can provide information about project risks, schedule, and budget. What would you like to know?"}