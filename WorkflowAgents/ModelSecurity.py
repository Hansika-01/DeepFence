from google.adk.agents import LlmAgent
from google.adk.tools import FunctionTool
from static.Telemetry import paramsFilling
import asyncio
import base64
# import hashlib
import os



def preventWeightTamperingFunction(file_path: str) -> str:
    """Locks a model file by setting it to read-only mode."""
    try:
        os.chmod(file_path, 0o444)  # Read-only permissions
        temp = paramsFilling("ModelSecurity",13301, "Prevent Weight Tampering executed successfully.", '{"Status":"Success"}', 1)
        return f"✅ Model file '{file_path}' locked successfully."
    except Exception as e:
        temp = paramsFilling("ModelSecurity",13301, f"Prevent Weight Tampering failed: {e}", '{"Status":"Error"}', 1)
        return f"⚠️ Error locking model file '{file_path}': {e}"

preventWeightTempering_tool = FunctionTool(preventWeightTamperingFunction)

def preventModelManipulationFunction(file_path: str, log_file: str) -> str:
    """Return a simple greeting message."""
    temp = paramsFilling("ModelSecurity",13302, "Set Model Manipulation executed successfully.", '{"Status":"Success"}', 2)
    return "Hello from Function 1!"

preventModelManipulation_tool = FunctionTool(preventModelManipulationFunction)

async def enableDifferentialPrivacyFunction() -> str:
    """Return a simple greeting message."""
    try:
        # Simulate a timeout by making the function wait longer than allowed
        await asyncio.wait_for(asyncio.sleep(6), timeout=5)  # Timeout set to 5 seconds

        status = "Success"
    except asyncio.TimeoutError:
        status = "Timeout"
    temp = paramsFilling("ModelSecurity",13303, "Enable Differential Privacy executed successfully.", f'{{"Status":"{status}"}}', 3)
    return "Hello from Function 1!"

enableDifferentialPrivacy_tool = FunctionTool(enableDifferentialPrivacyFunction)

def preventModelDeletionFunction(file_path: str) -> str:
    """Applies system and read-only attributes to prevent accidental deletion (Windows only)."""
    try:
        os.system(f'icacls "{file_path}" /deny Everyone:(D)')
        temp = paramsFilling("ModelSecurity",13307, "Prevent Model Deletion executed successfully.", '{"Status":"Success"}', 7)
        return f"🛡️ Deletion prevention (deny delete) applied to: {file_path}"
    except Exception as e:
        return f"⚠️ Failed to apply delete protection: {e}"

prevent_delete_tool = FunctionTool(preventModelDeletionFunction)

def encryptionFunction(json_path: str, encrypted_path: str) -> str:
    """Simulates encryption by base64 encoding a JSON file and saving to the encrypted path."""
    try:
        # Ensure the output directory exists
        os.makedirs(encrypted_path, exist_ok=True)

        # Define full path to the encrypted file
        encrypted_path = os.path.join(encrypted_path, "FilesConfigEncrypted.json")

        # Read and encode the JSON
        with open(json_path, "rb") as f:
            content = f.read()
        with open(encrypted_path, "wb") as out:
            out.write(base64.b64encode(content))

        temp = paramsFilling("ModelSecurity",13304, "Encryption executed successfully.", '{"Status":"Success"}', 4)
        return f"🔐 JSON file encoded and saved to: {encrypted_path}"
    except Exception as e:
        return f"⚠️ Error encoding JSON file: {e}"

encryption_tool = FunctionTool(encryptionFunction)

def decryptJsonFile(encrypted_path: str, output_path: str) -> str:
    """Simulates decryption by base64 decoding the JSON file."""
    try:

        # Ensure the output directory exists
        os.makedirs(output_path, exist_ok=True)

        # Define full path to the encrypted file
        output_path = os.path.join(output_path, "FilesConfigDecrypted.json")
        with open(encrypted_path, "rb") as f:
            encoded = f.read()
        with open(output_path, "wb") as out:
            out.write(base64.b64decode(encoded))
        
        temp = paramsFilling("ModelSecurity",13307, "Decryption executed successfully.", '{"Status":"Success"}', 7)
        return f"✅ JSON file decoded and restored to: {output_path}"
    except Exception as e:
        return f"⚠️ Error decoding JSON file: {e}"

decrypt_json_tool = FunctionTool(decryptJsonFile)

def setModelAccessPasswordFunction() -> str:
    """Return a simple greeting message."""
    temp = paramsFilling("ModelSecurity",13305, "Set Model Access Password executed successfully.", '{"Status":"Success"}', 5)
    return "Hello from Function 1!"

setModelAccessPassword_tool = FunctionTool(setModelAccessPasswordFunction)

def anonymizeCriticalPllFeaturesFunction() -> str:
    """Return a simple greeting message."""
    try:
        # Simulate an intentional error for testing
        raise RuntimeError("Simulated error for testing.")

        # If no error occurs, it returns success
        status = "Success"
    except Exception as e:
        # If an error occurs, the status is updated to 'Error' with the exception message
        status = f"Error: {str(e)}"
    temp = paramsFilling("ModelSecurity",13306, "Anonymize Critical Pll Features executed successfully.", f'{{"Status":"{status}"}}', 1,True)
    return "Hello from Function 1!"

anonymizeCriticalPllFeatures_tool = FunctionTool(anonymizeCriticalPllFeaturesFunction)

### 🔹 **Defining 7 Dummy Agents with Clear Descriptions**
preventWeightTempering = LlmAgent(
    name="PreventWeightTempering",
    model="gemini-2.0-flash",
    tools=[preventWeightTempering_tool],
    description="Locks model files to prevent unauthorized modifications."
)
preventModelManipulation = LlmAgent(
    name="PreventModelManipulation",
    model="gemini-1.5-flash",
    tools=[preventModelManipulation_tool],
    description="Verifies model file integrity by computing and comparing stored hashes."
)
enableDifferentialPrivacy = LlmAgent(
    name="EnableDifferentialPrivacy",
    model="gemini-1.5-flash", 
    tools=[enableDifferentialPrivacy_tool],
    description="Provides a simple greeting message."
)
encryption = LlmAgent(
    name="Encryption",
    model="gemini-1.5-flash",
    tools=[encryption_tool],
    description="Simulates JSON encryption by encoding it with base64 and saving to outputs."
)

decryptJsonData = LlmAgent(
    name="DecryptJsonData",
    model="gemini-1.5-flash",
    tools=[decrypt_json_tool],
    description="Simulates decryption by decoding a base64-encoded JSON file."
)
setModelAccessPassword = LlmAgent(
    name="SetModelAccessPassword",
    model="gemini-1.5-flash",
    tools=[setModelAccessPassword_tool],
    description="Provides a simple greeting message."
)
anonymizeCriticalPllFeatures = LlmAgent(
    name="AnonymizeCriticalPllFeatures",
    model="gemini-1.5-flash",
    tools=[anonymizeCriticalPllFeatures_tool],
    description="Provides a simple greeting message."
)

preventModelDelete = LlmAgent(
    name="PreventModelDelete",
    model="gemini-1.5-flash",
    tools=[prevent_delete_tool],
    description="Protects model files from accidental deletion by applying system attributes."
)

### **Exporting Agents for Main File**
ModelSecurity_agents_workflow = [preventWeightTempering, preventModelManipulation, enableDifferentialPrivacy,preventModelDelete, encryption, decryptJsonData, setModelAccessPassword, anonymizeCriticalPllFeatures]
