from google.adk.agents import LlmAgent
from google.adk.tools import FunctionTool
from static.Telemetry import paramsFilling


### 🔹 **Function 1: Simple Greeting**
def modelDriftAlertsFunction() -> str:
    """Return a simple greeting message."""
    temp =  paramsFilling("ModelMonitoring",13501, "Model Drift Alerts executed successfully.", '{"Status":"Success"}', 1)
    return "Hello from Function 1!"

modelDriftAlerts_tool = FunctionTool(modelDriftAlertsFunction)

def healthCheckFrequencyFunction() -> str:
    """Return a casual greeting message."""
    temp =  paramsFilling("ModelMonitoring",13502, "Health Check Frequency executed successfully.", '{"Status":"Success"}', 2,True)
    return "Hello from Function 1!"

healthCheckFrequency_tool = FunctionTool(healthCheckFrequencyFunction)


### 🔹 **Defining 7 Dummy Agents with Clear Descriptions**
modelDriftAlerts = LlmAgent(
    name="ModelDriftAlerts",
    model="gemini-2.0-flash",
    tools=[modelDriftAlerts_tool],
    description="Provides a simple greeting message."
)
healthCheckFrequency = LlmAgent(
    name="HealthCheckFrequency",
    model="gemini-1.5-flash",
    tools=[healthCheckFrequency_tool],
    description="Provides a simple greeting message."
)


### **Exporting Agents for Main File**
ModelMonitoring_agents_workflow = [modelDriftAlerts, healthCheckFrequency]
