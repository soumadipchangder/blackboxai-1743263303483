import pytest
from datetime import datetime
from agents.risk_scoring import RiskScoringAgent

@pytest.fixture
def risk_agent():
    return RiskScoringAgent()

def test_risk_calculation(risk_agent):
    # Test with typical project data
    project_data = {
        'budget_variance': 0.15,
        'payment_delays': 1,
        'schedule_delay': 0.2,
        'missed_milestones': 0,
        'attrition_rate': 0.1,
        'skill_gaps': 0.05,
        'defect_rate': 0.08,
        'tech_debt': 0.1
    }
    
    result = risk_agent.calculate_project_risk(project_data)
    
    assert 'score' in result
    assert 'level' in result
    assert 'factors' in result
    assert isinstance(result['score'], float)
    assert result['level'] in ['low', 'medium', 'high', 'critical']
    
    # Verify all factors were calculated
    assert set(result['factors'].keys()) == {
        'financial', 'schedule', 'resources', 'technical'
    }

def test_risk_levels(risk_agent):
    # Test risk level thresholds
    test_cases = [
        (0.85, 'critical'),
        (0.75, 'high'),
        (0.55, 'medium'),
        (0.15, 'low')
    ]
    
    for score, expected_level in test_cases:
        project_data = {'budget_variance': score}  # Simplistic test data
        result = risk_agent.calculate_project_risk(project_data)
        assert result['level'] == expected_level

def test_timestamp_format(risk_agent):
    project_data = {'budget_variance': 0.1}
    result = risk_agent.calculate_project_risk(project_data)
    
    # Verify ISO format timestamp
    try:
        datetime.fromisoformat(result['timestamp'])
    except ValueError:
        pytest.fail("Timestamp is not in ISO format")

def test_factor_weights(risk_agent):
    # Verify weights sum to 1.0
    total_weight = sum(risk_agent.risk_factors.values())
    assert abs(total_weight - 1.0) < 0.0001  # Account for floating point precision