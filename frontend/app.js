// Global variables
let currentProjectId = 'project-001';
let riskData = {};
let alertHistory = [];

// Initialize the dashboard
document.addEventListener('DOMContentLoaded', function() {
    // Initialize charts
    initRiskGauge();
    initRiskFactorsChart();
    
    // Load initial data
    fetchProjectData();
    fetchAlerts();
    
    // Set up chat interface
    document.getElementById('sendButton').addEventListener('click', sendChatMessage);
    document.getElementById('chatInput').addEventListener('keypress', function(e) {
        if (e.key === 'Enter') sendChatMessage();
    });
});

// Initialize risk gauge chart
function initRiskGauge() {
    const ctx = document.getElementById('riskGauge').getContext('2d');
    window.riskGauge = new Chart(ctx, {
        type: 'doughnut',
        data: {
            datasets: [{
                data: [0, 100],
                backgroundColor: ['#10B981', '#E5E7EB'],
                borderWidth: 0
            }]
        },
        options: {
            circumference: 180,
            rotation: 270,
            cutout: '80%',
            plugins: {
                legend: { display: false },
                tooltip: { enabled: false }
            }
        }
    });
}

// Initialize risk factors chart
function initRiskFactorsChart() {
    const ctx = document.getElementById('riskFactorsChart').getContext('2d');
    window.riskFactorsChart = new Chart(ctx, {
        type: 'bar',
        data: {
            labels: ['Financial', 'Schedule', 'Resources', 'Technical'],
            datasets: [{
                label: 'Risk Score',
                data: [0, 0, 0, 0],
                backgroundColor: [
                    '#EF4444',
                    '#F59E0B',
                    '#3B82F6',
                    '#8B5CF6'
                ],
                borderWidth: 1
            }]
        },
        options: {
            scales: {
                y: {
                    beginAtZero: true,
                    max: 1
                }
            }
        }
    });
}

// Fetch project data from API
async function fetchProjectData() {
    try {
        const response = await fetch(`/api/project/${currentProjectId}/risk`);
        if (!response.ok) throw new Error('Network response was not ok');
        
        riskData = await response.json();
        updateDashboard(riskData);
    } catch (error) {
        console.error('Error fetching project data:', error);
        showAlert('Failed to load project data', 'error');
    }
}

// Update dashboard with new data
function updateDashboard(data) {
    // Update risk score and level
    document.getElementById('riskScore').textContent = data.score.toFixed(2);
    const riskLevelElement = document.getElementById('riskLevel');
    riskLevelElement.textContent = data.level.toUpperCase();
    
    // Set risk level color
    riskLevelElement.className = `ml-2 px-3 py-1 rounded-full text-sm font-medium ${
        data.level === 'critical' ? 'bg-red-100 text-red-800' :
        data.level === 'high' ? 'bg-orange-100 text-orange-800' :
        data.level === 'medium' ? 'bg-yellow-100 text-yellow-800' :
        'bg-green-100 text-green-800'
    }`;
    
    // Update risk gauge
    const riskPercentage = data.score * 100;
    window.riskGauge.data.datasets[0].data = [riskPercentage, 100 - riskPercentage];
    window.riskGauge.data.datasets[0].backgroundColor = [
        getRiskColor(data.score),
        '#E5E7EB'
    ];
    window.riskGauge.update();
    
    // Update risk factors chart
    window.riskFactorsChart.data.datasets[0].data = [
        data.factors.financial,
        data.factors.schedule,
        data.factors.resources,
        data.factors.technical
    ];
    window.riskFactorsChart.update();
    
    // Update progress bars
    updateProgressBar('schedule', data.factors.schedule);
    updateProgressBar('budget', data.factors.financial);
    updateProgressBar('resource', data.factors.resources);
}

// Update progress bar display
function updateProgressBar(type, value) {
    const percentage = Math.round(value * 100);
    document.getElementById(`${type}Bar`).style.width = `${percentage}%`;
    document.getElementById(`${type}Value`).textContent = `${percentage}%`;
    
    // Set color based on value
    const element = document.getElementById(`${type}Bar`);
    element.className = `h-2.5 rounded-full ${
        value > 0.7 ? 'bg-red-500' :
        value > 0.4 ? 'bg-yellow-500' :
        'bg-green-500'
    }`;
}

// Get color based on risk score
function getRiskColor(score) {
    return score > 0.8 ? '#EF4444' :  // red
           score > 0.6 ? '#F59E0B' :  // orange
           score > 0.4 ? '#FCD34D' :  // yellow
           '#10B981';                 // green
}

// Fetch alerts from API
async function fetchAlerts() {
    try {
        const response = await fetch(`/api/project/${currentProjectId}/alerts`);
        if (!response.ok) throw new Error('Network response was not ok');
        
        alertHistory = await response.json();
        renderAlerts();
    } catch (error) {
        console.error('Error fetching alerts:', error);
    }
}

// Render alerts to the UI
function renderAlerts() {
    const container = document.getElementById('alertsContainer');
    container.innerHTML = '';
    
    alertHistory.slice(0, 5).forEach(alert => {
        const alertElement = document.createElement('div');
        alertElement.className = `p-3 rounded-lg border-l-4 ${
            alert.severity === 'critical' ? 'bg-red-50 border-red-500' :
            alert.severity === 'high' ? 'bg-orange-50 border-orange-500' :
            'bg-yellow-50 border-yellow-500'
        }`;
        
        alertElement.innerHTML = `
            <div class="flex justify-between items-start">
                <div>
                    <h3 class="font-medium">${alert.title}</h3>
                    <p class="text-sm text-gray-600">${alert.message}</p>
                </div>
                <span class="text-xs text-gray-500">${new Date(alert.timestamp).toLocaleString()}</span>
            </div>
        `;
        
        container.appendChild(alertElement);
    });
}

// Handle chat messages
function sendChatMessage() {
    const input = document.getElementById('chatInput');
    const message = input.value.trim();
    if (!message) return;
    
    addChatMessage('user', message);
    input.value = '';
    
    // Simulate AI response
    setTimeout(() => {
        const response = generateChatResponse(message);
        addChatMessage('ai', response);
    }, 1000);
}

// Add message to chat UI
function addChatMessage(sender, text) {
    const container = document.getElementById('chatMessages');
    const messageElement = document.createElement('div');
    messageElement.className = `mb-3 ${sender === 'user' ? 'text-right' : 'text-left'}`;
    
    messageElement.innerHTML = `
        <div class="inline-block max-w-xs md:max-w-md lg:max-w-lg px-4 py-2 rounded-lg ${
            sender === 'user' ? 'bg-blue-100 text-blue-900' : 'bg-gray-200 text-gray-900'
        }">
            ${text}
        </div>
    `;
    
    container.appendChild(messageElement);
    container.scrollTop = container.scrollHeight;
}

// Generate simple AI response
function generateChatResponse(message) {
    const lowerMessage = message.toLowerCase();
    
    if (lowerMessage.includes('risk') || lowerMessage.includes('score')) {
        return `The current risk score is ${riskData.score.toFixed(2)} (${riskData.level} level). ` +
               `The main contributing factors are: ${getTopRiskFactors()}.`;
    }
    else if (lowerMessage.includes('schedule') || lowerMessage.includes('timeline')) {
        return `Schedule risk factor is currently ${(riskData.factors.schedule * 100).toFixed(0)}%. ` +
               `This is considered ${getRiskDescription(riskData.factors.schedule)}.`;
    }
    else if (lowerMessage.includes('budget') || lowerMessage.includes('financial')) {
        return `Financial risk factor is currently ${(riskData.factors.financial * 100).toFixed(0)}%. ` +
               `This is considered ${getRiskDescription(riskData.factors.financial)}.`;
    }
    else {
        return "I can provide information about project risks, schedule, budget, and resource factors. " +
               "What would you like to know specifically?";
    }
}

// Get top risk factors
function getTopRiskFactors() {
    const factors = Object.entries(riskData.factors)
        .sort((a, b) => b[1] - a[1])
        .slice(0, 2)
        .map(([factor, score]) => `${factor} (${(score * 100).toFixed(0)}%)`);
    
    return factors.join(' and ');
}

// Get risk description
function getRiskDescription(score) {
    return score > 0.7 ? 'very high' :
           score > 0.5 ? 'high' :
           score > 0.3 ? 'moderate' :
           'low';
}

// Show temporary alert message
function showAlert(message, type = 'info') {
    const alert = document.createElement('div');
    alert.className = `fixed top-4 right-4 px-4 py-2 rounded-md shadow-md ${
        type === 'error' ? 'bg-red-100 text-red-800' :
        type === 'success' ? 'bg-green-100 text-green-800' :
        'bg-blue-100 text-blue-800'
    }`;
    alert.textContent = message;
    document.body.appendChild(alert);
    
    setTimeout(() => {
        alert.remove();
    }, 5000);
}