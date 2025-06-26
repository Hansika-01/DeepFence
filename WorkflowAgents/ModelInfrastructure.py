from google.adk.agents import LlmAgent
from google.adk.tools import FunctionTool
from static.Telemetry import paramsFilling
import subprocess

### 🔹 **Function 5: Reverse Text**
def nodeDeactivationFunction(text: str) -> str:
    """Reverse the input text string."""
    temp =  paramsFilling("ModelInfrastructure",13201, "Node Deactivation executed successfully.", '{"Status":"Success"}', 1)
    return f"Reversed Text: {text[::-1]}"

nodeDeactivation_tool = FunctionTool(nodeDeactivationFunction)

def deepContractiveNetworkFunction(text: str) -> str:
    """Reverse the input text string."""
    temp =  paramsFilling("ModelInfrastructure",13202, "Deep Contractive Network executed successfully.", '{"Status":"Success"}', 2)
    return f"Reversed Text: {text[::-1]}"

deepContractiveNetwork_tool = FunctionTool(deepContractiveNetworkFunction)

def secureMultipartyComputationFunction(text: str) -> str:
    """Reverse the input text string."""
    temp =  paramsFilling("ModelInfrastructure",13203, "Secure Multiparty Computation executed successfully.", '{"Status":"Success"}', 3)
    return f"Reversed Text: {text[::-1]}"

secureMultipartyComputation_tool = FunctionTool(secureMultipartyComputationFunction)

def defendModelDeploymentFunction(text: str) -> str:
    """Reverse the input text string."""
    temp =  paramsFilling("ModelInfrastructure",13204, "Defend Model Deployment executed successfully.", '{"Status":"Success"}', 4)
    return f"Reversed Text: {text[::-1]}"

defendModelDeployment_tool = FunctionTool(defendModelDeploymentFunction)

def siemIntegrationFunction(text: str) -> str:
    """Reverse the input text string."""
    temp =  paramsFilling("ModelInfrastructure",13205, "Siem Integration executed successfully.", '{"Status":"Success"}', 5)
    return f"Reversed Text: {text[::-1]}"

siemIntegration_tool = FunctionTool(siemIntegrationFunction)

def envComplianceFunction(text: str) -> str:
    """Reverse the input text string."""
    temp =  paramsFilling("ModelInfrastructure",13206, "Env Compliance executed successfully.", '{"Status":"Success"}', 6)
    return f"Reversed Text: {text[::-1]}"

envCompliance_tool = FunctionTool(envComplianceFunction)

def modelTheftFunction(text: str) -> str:
    """Reverse the input text string."""
    temp =  paramsFilling("ModelInfrastructure",13207, "Model Theft executed successfully.", '{"Status":"Success"}', 7)
    return f"Reversed Text: {text[::-1]}"

modelTheft_tool = FunctionTool(modelTheftFunction)

def certificateSpoofingFunction(text: str) -> str:
    """Reverse the input text string."""
    temp =  paramsFilling("ModelInfrastructure",13208, "Certificate Spoofing executed successfully.", '{"Status":"Success"}', 8)
    return f"Reversed Text: {text[::-1]}"

certificateSpoofing_tool = FunctionTool(certificateSpoofingFunction)

def pingNetworkFunction(host: str, count: int) -> str:
    """Pings a network host and returns reachability information."""
    try:
        result = subprocess.run(["ping", host, "-n", str(count)], capture_output=True, text=True)
        temp = paramsFilling("ModelInfrastructure",13209, "Ping Network executed successfully.", '{"Status":"Success"}', 3,True)
        if result.returncode == 0:
            return f"✅ Host '{host}' is reachable:\n\n{result.stdout}"
        else:
            return f"⚠️ Host '{host}' is unreachable:\n\n{result.stdout}"
    except Exception as e:
        temp = paramsFilling("ModelInfrastructure",13209, "Ping Network failed.", '{"Status":"Failed"}', 3,True)
        return f"⚠️ Network ping failed: {e}"

ping_tool = FunctionTool(pingNetworkFunction)


### 🔹 **Defining 7 Dummy Agents with Clear Descriptions**
nodeDeactivation = LlmAgent(
    name="NodeDeactivation",#agent -15
    model="gemini-1.5-flash",
    tools=[nodeDeactivation_tool],
    description="Reverses the provided text."
)
deepContractiveNetwork = LlmAgent(
    name="DeepContractiveNetwork",
    model="gemini-1.5-flash",
    tools=[deepContractiveNetwork_tool],
    description="Reverses the provided text."
)
secureMultipartyComputation = LlmAgent(
    name="SecureMultipartyComputation",
    model="gemini-1.5-flash",
    tools=[secureMultipartyComputation_tool],
    description="Reverses the provided text."
)
defendModelDeployment = LlmAgent(
    name="DefendModelDeployment",
    model="gemini-1.5-flash",
    tools=[defendModelDeployment_tool],
    description="Reverses the provided text."
)
siemIntegration = LlmAgent(
    name="SiemIntegration",
    model="gemini-1.5-flash",
    tools=[siemIntegration_tool],
    description="Reverses the provided text."
)
envCompliance = LlmAgent(
    name="EnvCompliance",
    model="gemini-1.5-flash",
    tools=[envCompliance_tool],
    description="Reverses the provided text."
)
modelTheft = LlmAgent(
    name="ModelTheft",
    model="gemini-1.5-flash",
    tools=[modelTheft_tool],
    description="Reverses the provided text."
)
certificateSpoofing = LlmAgent(
    name="CertificateSpoofing",
    model="gemini-1.5-flash",
    tools=[certificateSpoofing_tool],
    description="Reverses the provided text."
)
networkHealthMonitor = LlmAgent(
    name="NetworkHealthMonitor",
    model="gemini-1.5-flash",
    tools=[ping_tool],
    description="Monitors infrastructure availability by pinging a given host and reporting status."
)

### **Exporting Agents for Main File**
ModelInfrastructure_agents_workflow = [nodeDeactivation, deepContractiveNetwork, secureMultipartyComputation, defendModelDeployment, siemIntegration, envCompliance, modelTheft, certificateSpoofing, networkHealthMonitor]
