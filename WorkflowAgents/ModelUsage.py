from google.adk.agents import LlmAgent
from google.adk.tools import FunctionTool
from static.Telemetry import paramsFilling
import logging
import os
import time
import pyzipper

def lockModelFunction(folder_path: str, password: str) -> str:
    """
    Compresses the given folder into a password-protected ZIP archive named 'LockedZip.zip'
    in the DeepFenceOutputs directory at the same AccountWorkspace level.
    """
    try:
        # Validate input folder
        if not os.path.isdir(folder_path):
            return f"⚠️ Folder not found: {folder_path}"

        # Calculate output directory: replace 'Models/...' with 'DeepFenceOutputs'
        # Example: 
        #   folder_path = './Workspace/slope.expedition@gmail.com/AccountWorkspace/Models/HeartAttackDetection'
        #   output_dir = './Workspace/slope.expedition@gmail.com/AccountWorkspace/DeepFenceOutputs'
        account_workspace_dir = os.path.dirname(os.path.dirname(folder_path))  # Up two levels
        output_dir = os.path.join(account_workspace_dir, "DeepFenceOutputs")
        os.makedirs(output_dir, exist_ok=True)
        zip_path = os.path.join(output_dir, "LockedZip.zip")

        # Create password-protected zip
        with pyzipper.AESZipFile(zip_path, 'w', compression=pyzipper.ZIP_DEFLATED, encryption=pyzipper.WZ_AES) as zf:
            zf.setpassword(password.encode())
            for root, _, files in os.walk(folder_path):
                for file in files:
                    abs_path = os.path.join(root, file)
                    # Store relative path inside the zip (preserve subfolders)
                    arcname = os.path.relpath(abs_path, start=folder_path)
                    zf.write(abs_path, arcname)

        temp = paramsFilling("ModelUsage",13401, "Lock Model executed successfully.", '{"Status":"Success"}', 1)
        return f"🔐 Folder locked and saved as password-protected ZIP: {zip_path}"

    except Exception as e:
        temp = paramsFilling("ModelUsage",13401, "Lock Model Failed.", '{"Status":"Failed"}', 1)
        return f"⚠️ Failed to lock folder: {e}"


lockModel_tool = FunctionTool(lockModelFunction)

def unlockModelFunction(zip_path: str, password: str, extract_to: str) -> str:
    """
    Attempts to unlock and extract a password-protected ZIP archive using the provided password.
    Logs if the password is incorrect.
    """
    if not os.path.isfile(zip_path):
        return f"⚠️ ZIP file not found: {zip_path}"

    try:
        with pyzipper.AESZipFile(zip_path) as zf:
            zf.pwd = password.encode()
            # Check password by trying to list files
            _ = zf.namelist()  # Will raise RuntimeError if password is wrong

            # Now create the extraction directory (if not exists)
            if not os.path.exists(extract_to):
                os.makedirs(extract_to)

            zf.extractall(path=extract_to)
            temp = paramsFilling("ModelUsage",13409, "Unlock Model executed successfully.", '{"Status":"Success"}', 9)
            return f"✅ Archive extracted to: {extract_to}"

    except RuntimeError:
        temp = paramsFilling("ModelUsage",13409, "Unlock Model Failed: Wrong password.", '{"Status":"Failed"}', 9)
        return "🚨 Wrong password. Access denied and event logged."
    except Exception as e:
        temp = paramsFilling("ModelUsage",13409, "Unlock Model Failed.", '{"Status":"Failed"}', 9)
        return f"⚠️ Failed to unlock ZIP: {e}"
    
unlockModel_tool = FunctionTool(unlockModelFunction)

def preventWhiteBoxFunction():
    """Execute preventWhiteBox function with retry logic."""
    retry_count = 0  # Start at 0

    while retry_count < 2:  # Retry only once before succeeding
        try:
            if retry_count == 0:
                raise RuntimeError("Simulated error for testing.")

            status = "Success"
            break  # Exit loop if successful
        except Exception as e:
            status = "Retrying the agent function"
            temp = paramsFilling("ModelUsage",13402, "Prevent WhiteBox executed successfully.", '{"Status":"Success"}', 2)
            
            print(f"🔄 Retrying encryptionFunction due to error: {str(e)}")
            time.sleep(2)  # Small delay before retry
            retry_count += 1  # Increment retry count

    temp = paramsFilling("ModelUsage",13402, f"Prevent WhiteBox executed with status: {status}", f'{{"Status":"{status}"}}', 4)
    return "Hello from Function 1!"

preventWhiteBox_tool = FunctionTool(preventWhiteBoxFunction)

def preventBlackBoxFunction(text: str) -> str:
    """Convert input text to uppercase."""
    temp = paramsFilling("ModelUsage",13403, "Prevent BlackBox executed successfully.", '{"Status":"Success"}', 3)
    return f"Uppercased Text: {text.upper()}"

preventBlackBox_tool = FunctionTool(preventBlackBoxFunction)

def preventGreyBoxFunction(text: str) -> str:
    """Convert input text to uppercase."""
    temp = paramsFilling("ModelUsage",13404, "Prevent GreyBox executed successfully.", '{"Status":"Success"}', 4)
    return f"Uppercased Text: {text.upper()}"

preventGreyBox_tool = FunctionTool(preventGreyBoxFunction)

def preventBadnetsFunction(text: str) -> str:
    """Convert input text to uppercase."""
    temp = paramsFilling("ModelUsage",13405, "Prevent Badnets executed successfully.", '{"Status":"Success"}', 5)
    return f"Uppercased Text: {text.upper()}"

preventBadnets_tool = FunctionTool(preventBadnetsFunction)

def enableResponsibleAIFunction(task_name: str) -> str:
    """Logs AI execution details to track workflows for auditing."""
    logging.basicConfig(filename="ai_execution_logs.log", level=logging.INFO)
    try:
        log_message = f"AI task '{task_name}' executed successfully."
        logging.info(log_message)
        temp = paramsFilling("ModelUsage",13406, "Enable Responsible AI executed successfully.", '{"Status":"Success"}', 6)
        return f"✅ Execution logged: {log_message}"
    except Exception as e:
        temp = paramsFilling("ModelUsage",13406, f"Enable Responsible AI failed: {e}", '{"Status":"Error"}', 6)
        return f"⚠️ Error logging AI execution: {e}"

enableResponsibleAI_tool = FunctionTool(enableResponsibleAIFunction)

def enableLeastPrivilagePolicyFunction(text: str) -> str:
    """Convert input text to uppercase."""
    temp = paramsFilling("ModelUsage",13407, "Enable Least Privilage Policy executed successfully.", '{"Status":"Success"}', 7)
    return f"Uppercased Text: {text.upper()}"

enableLeastPrivilagePolicy_tool = FunctionTool(enableLeastPrivilagePolicyFunction)

def detectAdversarialInputFunction(text: str) -> str:
    """Convert input text to uppercase."""
    temp = paramsFilling("ModelUsage",13408, "Detect Adversarial Input executed successfully.", '{"Status":"Success"}', 8,True)
    return f"Uppercased Text: {text.upper()}"

detectAdversarialInput_tool = FunctionTool(detectAdversarialInputFunction)

### 🔹 **Defining 7 Dummy Agents with Clear Descriptions**
lockModel = LlmAgent(
    name="LockModel",
    model="gemini-1.5-flash",
    tools=[lockModel_tool],
    description="Compresses a model folder into a password-protected ZIP archive for secure storage and sharing."
)
unlockModel = LlmAgent(
    name="UnlockModel",
    model="gemini-1.5-flash",
    tools=[unlockModel_tool],
    description="Unlocks a password-protected ZIP archive and logs failed password attempts."
)
preventWhiteBoxAttack = LlmAgent(
    name="PreventWhiteBoxAttack",
    model="gemini-1.5-flash",
    tools=[preventWhiteBox_tool],
    description="Converts text to uppercase."
)
preventBlackBoxAttack = LlmAgent(
    name="PreventBlackBoxAttack",
    model="gemini-1.5-flash",
    tools=[preventBlackBox_tool],
    description="Converts text to uppercase."
)
preventGreyBoxAttack = LlmAgent(
    name="PreventGreyBoxAttack",
    model="gemini-1.5-flash",
    tools=[preventGreyBox_tool],
    description="Converts text to uppercase."
)
preventBadnets = LlmAgent(
    name="PreventBadnets",
    model="gemini-1.5-flash",
    tools=[preventBadnets_tool],
    description="Converts text to uppercase."
)
enableResponsibleAI = LlmAgent(
    name="EnableResponsibleAI",
    model="gemini-1.5-flash",
    tools=[enableResponsibleAI_tool],
    description="Logs AI task execution details for auditing and compliance."
)
enableLeastPrivilagePolicy = LlmAgent(
    name="EnableLeastPrivilagePolicy",
    model="gemini-1.5-flash",
    tools=[enableLeastPrivilagePolicy_tool],
    description="Converts text to uppercase."
)
detectAdversialInput = LlmAgent(
    name="DetectAdversialInput",
    model="gemini-1.5-flash",
    tools=[detectAdversarialInput_tool],
    description="Converts text to uppercase."
)

### **Exporting Agents for Main File**
ModelUsage_agents_workflow = [lockModel,unlockModel, preventWhiteBoxAttack, preventBlackBoxAttack, preventGreyBoxAttack, preventBadnets, enableResponsibleAI, enableLeastPrivilagePolicy, detectAdversialInput]
