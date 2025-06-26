import asyncio
import uuid
from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService
from google.genai import types
from WorkflowAgents.DataSecurity import DataSecurity_agents_workflow
from WorkflowAgents.ModelDevelopment import ModelDevelopment_agents_workflow
from WorkflowAgents.ModelSecurity import ModelSecurity_agents_workflow
from WorkflowAgents.ModelUsage import ModelUsage_agents_workflow
from WorkflowAgents.ModelInfrastructure import ModelInfrastructure_agents_workflow
from WorkflowAgents.ModelMonitoring import ModelMonitoring_agents_workflow

APP_NAME = "Agent_Testing"
USER_ID = "surya_regalla"
SESSION_ID = str(uuid.uuid4())

# Combine all agents
all_agents = DataSecurity_agents_workflow + ModelSecurity_agents_workflow + ModelDevelopment_agents_workflow + ModelUsage_agents_workflow + ModelInfrastructure_agents_workflow + ModelMonitoring_agents_workflow
agent_map = {agent.name: agent for agent in all_agents}

# Define simple prompts matching dummy functions
agent_prompts = {
    # # Data Security agents
    "DetectDataPoisoning": "Validate dataset at './static/Files/sample_csv.csv'. using the provided using the provided tool",
    "EnableModelAccessControl": "Hide the folder './Workspace/slope.expedition@gmail.com/AccountWorkspace/Models/DataCoSupplyChain/DataCoSupplyChain.csv-Clustering-Dec06-23-14-29-57.pkl'. using the provided tool",
    # "EnableModelBackup": "Reverse the string 'OpenAI'. using the provided tool",
    "PreventDataInputManipulation": "Zip folder './static/Files/ZippingTest' using password 'Secure123' using the provided tool",
    "PreventDataLabelManipulation": "Execute the function tool that Encrypts dataset './static/Files/sample_csv.csv'.",
    # "PreventDataInjections": "Execute the function tool that reverses the string 'OpenAI'.",
    # "PreventLogicCorruption": "Execute the function tool that reverses the string 'OpenAIGPT'.",
    # "EnableDataMinimisation": "Extract essential columns ['UserID', 'Name', 'Age'] from the dataset './static/Files/sample_csv.csv'.",
    "EnableDataCataloguePolicy": "Verify if the required columns ['UserID', 'Name', 'Age', 'Email', 'PurchaseAmount'] exist in the dataset './static/Files/sample_csv.csv'.",

    # # Model Development agents
    "GradientMasking": "Please provide a friendly greeting.",
    "DefensiveDistillation": "Please provide a friendly greeting.",
    "Regularization": "Please provide a friendly greeting.",
    "FeatureSqueezing": "Please provide a friendly greeting.",
    # "Reformers": "Please provide a friendly greeting.",
    # "AdaptativeMisinformation": "Please provide a friendly greeting.",
    # "NeuralCleanse": "Please provide a friendly greeting.",
    # "ModelguidedAnonymization": "Please provide a friendly greeting.",
    "Anonymization": "Please provide a friendly greeting.",

    # # Model Infrastructure agents
    "NodeDeactivation": "Reverse the string 'OpenAI'.",
    "DeepContractiveNetwork": "Reverse the string 'OpenAI'.",
    "SecureMultipartyComputation": "Reverse the string 'OpenAI'.",
    "DefendModelDeployment": "Reverse the string 'OpenAI'.",
    # "SiemIntegration": "Reverse the string 'OpenAI'.",
    # "EnvCompliance": "Reverse the string 'OpenAI'.",
    # "ModelTheft": "Reverse the string 'OpenAI'.",
    # "CertificateSpoofing": "Reverse the string 'OpenAI'.",
    "NetworkHealthMonitor": "Ping the host '8.8.8.8' using count 3 to ensure the system is reachable.",

    # # Model Security agents
    "PreventWeightTempering": "Lock the model file at './Workspace/slope.expedition@gmail.com/AccountWorkspace/Models/DataCoSupplyChain/DataCoSupplyChain.csv-Clustering-Dec06-23-10-31-00.pkl' using the provided tool.",
    # "PreventModelManipulation": "Verify the integrity of the model file './static/Files/modelTest.pkl' by comparing its hash with the stored reference in './static/Files/Outputs/hash_log.txt'. If the hash differs, flag it as tampered.",
    "EnableDifferentialPrivacy": "Please provide a friendly greeting.",
    "Encryption": "Encrypt the JSON file './Workspace/slope.expedition@gmail.com/AccountWorkspace/Configurations/FilesConfig.json' using base64 and save at './Workspace/slope.expedition@gmail.com/AccountWorkspace/DeepFenceOutputs/'.",
    "DecryptJsonData": "Decrypt './Workspace/slope.expedition@gmail.com/AccountWorkspace/Configurations/FilesConfigEncrypted.json' and save at './Workspace/slope.expedition@gmail.com/AccountWorkspace/DeepFenceOutputs/'.",

    # "SetModelAccessPassword": "Please povide a casual greeting.",
    "AnonymizeCriticalPllFeatures": "Please provide a friendly greeting.",
    # "PreventModelDelete": "Apply deletion protection to './Workspace/slope.expedition@gmail.com/AccountWorkspace/Models/DataCoSupplyChain/DataCoSupplyChain.csv-Clustering-Dec05-23-16-24-58.pkl'.",

    # # Model Usage agents
    "LockModel": "Secure the model file './Workspace/slope.expedition@gmail.com/AccountWorkspace/Models/HeartAttackDetection' using password 'secure123' and store it in ./Workspace/slope.expedition@gmail.com/AccountWorkspace/DeepFenceOutputs/.",
    "UnlockModel": "Unlock the file ./Workspace/slope.expedition@gmail.com/AccountWorkspace/Models/LockedZip.zip using password secure123 and extract it to ./Workspace/slope.expedition@gmail.com/AccountWorkspace/DeepFenceOutputs/HeartAttackDetection_unlocked/.",

    # "PreventWhiteBoxAttack": "Please provide a friendly greeting.",
    # "PreventBlackBoxAttack": "Convert the text 'test' to uppercase.",
    # "PreventGreyBoxAttack": "Convert the text 'test' to uppercase.",
    # "PreventBadnets": "Convert the text 'test' to uppercase.",
    "EnableResponsibleAI": "Log execution details for AI task 'RiskPrediction_Model' using the provided tool.",
    "EnableLeastPrivilagePolicy": "Convert the text 'test' to uppercase.",
    "DetectAdversialInput": "Convert the text 'test' to uppercase.", 

    # # Model Monitoring agents
    # "ModelDriftAlerts": "Please provide a friendly greeting.",
    # "HealthCheckFrequency": "Please provide a simple greeting.",  
    
}

# async def run_agents():
#     workflow_results = []
#     valid_agents = [name for name in agent_prompts if name in agent_map]

#     for agent_name in valid_agents:
#         agent = agent_map[agent_name]
#         prompt = agent_prompts[agent_name]
#         print(f"🔹 Executing {agent_name} with prompt: {prompt}")

#         await asyncio.sleep(5)  # Base delay before execution

#         runner = Runner(agent=agent, app_name=APP_NAME, session_service=session_service)
#         new_message = types.Content(role="user", parts=[types.Part(text=prompt)])

#         response = None
#         async for event in runner.run_async(user_id=USER_ID, session_id=SESSION_ID, new_message=new_message):
#             if event.is_final_response():
#                 response = event.content.parts[0].text if event.content and event.content.parts else f"⚠️ No valid response from {agent_name}."

#         print(f"✅ {agent_name} completed. Response: {response}")
#         workflow_results.append({"agent": agent_name, "response": response.strip()})

#     print("🚀 All agents completed.")
#     return workflow_results

async def run_agents():
    workflow_results = []

    for agent_name in [name for name in agent_prompts if name in agent_map]:
        # Generate a fresh session ID for each agent run
        session_id = str(uuid.uuid4())
        session_service = InMemorySessionService()
        initial_state = {
            "user_name": "Surya",
            "task": "Executing simplified dummy workflows",
        }
        await session_service.create_session(
            app_name=APP_NAME,
            user_id=USER_ID,
            session_id=session_id,
            state=initial_state,
        )

        agent = agent_map[agent_name]
        prompt = agent_prompts[agent_name]
        print(f"🔹 Executing {agent_name} with prompt: {prompt}")

        runner = Runner(agent=agent, app_name=APP_NAME, session_service=session_service)
        new_message = types.Content(role="user", parts=[types.Part(text=prompt)])

        await asyncio.sleep(7)  # Small delay to avoid race conditions

        response = None
        async for event in runner.run_async(user_id=USER_ID, session_id=session_id, new_message=new_message):
            if event.is_final_response():
                response = event.content.parts[0].text if event.content and event.content.parts else f"⚠️ No valid response from {agent_name}."

        print(f"✅ {agent_name} completed. Response: {response}")
        workflow_results.append({"agent": agent_name, "response": response.strip()})

    print("🚀 All agents completed.")
    return workflow_results