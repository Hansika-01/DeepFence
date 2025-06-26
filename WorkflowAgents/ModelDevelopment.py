from google.adk.agents import LlmAgent
from google.adk.tools import FunctionTool

from static.Telemetry import paramsFilling

### 🔹 **Function 1: Simple Greeting**
def gradientMaskingFunction() -> str:
    """Return a simple greeting message."""

    temp =  paramsFilling("ModelDevelopment",13101, "Gradient Masking executed successfully.", '{"Status":"Success"}', 1)

    return "Hello from Function 1!"

gradientMasking_tool = FunctionTool(gradientMaskingFunction)

def defensiveDistillationFunction() -> str:
    """Return a simple greeting message."""
    temp =  paramsFilling("ModelDevelopment",13102, "Defensive Distillation executed successfully.", '{"Status":"Success"}', 2)
    return "Hello from Function 1!"

defensiveDistillation_tool = FunctionTool(defensiveDistillationFunction)

def regularizationFunction() -> str:
    """Return a simple greeting message."""
    temp =  paramsFilling("ModelDevelopment",13103, "Regularization executed successfully.", '{"Status":"Success"}', 3)
    return "Hello from Function 1!"

regularization_tool = FunctionTool(regularizationFunction)

def featureSqueezingFunction() -> str:
    """Return a simple greeting message."""
    temp =  paramsFilling("ModelDevelopment",13104, "Feature SqueezingF executed successfully.", '{"Status":"Success"}', 4)
    return "Hello from Function 1!"

featureSqueezing_tool = FunctionTool(featureSqueezingFunction)

def reformersFunction() -> str:
    """Return a simple greeting message."""
    temp =  paramsFilling("ModelDevelopment",13105, "Reformers executed successfully.", '{"Status":"Success"}', 5)
    return "Hello from Function 1!"

reformers_tool = FunctionTool(reformersFunction)

def adaptativeMisinformationFunction() -> str:
    """Return a simple greeting message."""
    temp =  paramsFilling("ModelDevelopment",13106, "Adaptative Misinformation executed successfully.", '{"Status":"Success"}', 6)
    return "Hello from Function 1!"

adaptativeMisinformation_tool = FunctionTool(adaptativeMisinformationFunction)

def neuralCleanseFunction() -> str:
    """Return a simple greeting message."""
    temp =  paramsFilling("ModelDevelopment",13107, "Neural Cleanse executed successfully.", '{"Status":"Success"}', 7)
    return "Hello from Function 1!"

neuralCleanse_tool = FunctionTool(neuralCleanseFunction)

def modelguidedAnonymizationFunction() -> str:
    """Return a simple greeting message."""
    temp =  paramsFilling("ModelDevelopment",13108, "Model guided Anonymization executed successfully.", '{"Status":"Success"}', 8)
    return "Hello from Function 1!"

modelguidedAnonymization_tool = FunctionTool(modelguidedAnonymizationFunction)

def anonymizationFunction() -> str:
    """Return a simple greeting message."""
    temp =  paramsFilling("ModelDevelopment",13109, "Anonymization executed successfully.", '{"Status":"Success"}', 9,True)
    return "Hello from Function 1!"

anonymization_tool = FunctionTool(anonymizationFunction)



### 🔹 **Defining 7 Dummy Agents with Clear Descriptions**
gradientMasking = LlmAgent(
    name="GradientMasking",
    model="gemini-2.0-flash",
    tools=[gradientMasking_tool],
    description="Provides a simple greeting message."
)
defensiveDistillation = LlmAgent(
    name="DefensiveDistillation",
    model="gemini-1.5-flash",
    tools=[defensiveDistillation_tool],
    description="Provides a simple greeting message."
)
regularization = LlmAgent(
    name="Regularization",
    model="gemini-1.5-flash",
    tools=[regularization_tool],
    description="Provides a simple greeting message."
)
featureSqueezing = LlmAgent(
    name="FeatureSqueezing",
    model="gemini-1.5-flash",
    tools=[featureSqueezing_tool],
    description="Provides a simple greeting message."
)
reformers = LlmAgent(
    name="Reformers",
    model="gemini-1.5-flash",
    tools=[reformers_tool],
    description="Provides a simple greeting message."
)
adaptativeMisinformation = LlmAgent(
    name="AdaptativeMisinformation",
    model="gemini-1.5-flash",
    tools=[adaptativeMisinformation_tool],
    description="Provides a simple greeting message."
)
neuralCleanse = LlmAgent(
    name="NeuralCleanse",
    model="gemini-1.5-flash",
    tools=[neuralCleanse_tool],
    description="Provides a simple greeting message."
)

modelguidedAnonymization = LlmAgent(
    name="ModelguidedAnonymization",
    model="gemini-1.5-flash",
    tools=[modelguidedAnonymization_tool],
    description="Provides a simple greeting message."
)
anonymization = LlmAgent(
    name="Anonymization",
    model="gemini-1.5-flash",
    tools=[anonymization_tool],
    description="Provides a simple greeting message."
)

### **Exporting Agents for Main File**
ModelDevelopment_agents_workflow = [gradientMasking, defensiveDistillation, regularization, featureSqueezing, reformers, adaptativeMisinformation, neuralCleanse, modelguidedAnonymization, anonymization]
