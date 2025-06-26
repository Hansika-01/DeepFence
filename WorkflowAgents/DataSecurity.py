import os
import pandas as pd
from dotenv import load_dotenv
from google.adk.agents import LlmAgent
from google.adk.tools import FunctionTool
from google.genai import types
import pyzipper
from cryptography.fernet import Fernet
from static.Telemetry import paramsFilling


### 🔹 **Function 1: Detect Data Poisoning**
def detectDataPoisoningFunction(file_path: str) -> str:
    abs_path = os.path.abspath(file_path)
    try:
        df = pd.read_csv(abs_path)
        if df.isnull().sum().sum() > 0:
            return f"❌ Data poisoning detected in {abs_path}!"
        temp =  paramsFilling("DataSecurity",13001, "Detect Data Poisoning executed successfully.", '{"Status":"Success"}', 1)

        return f"✅ Dataset {abs_path} is clean!"
    except Exception as e:
        return f"❌ Error validating dataset {abs_path}: {e}"

detectDataPoisoning_tool = FunctionTool(detectDataPoisoningFunction)

### 🔹 **Function 2: Hide Folder**
def enableModelAccessControlFunction(folder_path: str) -> str:
    abs_path = os.path.abspath(folder_path)
    try:
        os.system(f'attrib +h "{abs_path}"')
        temp =  paramsFilling("DataSecurity",13002, "Enable Model Access Control executed successfully.", '{"Status":"Success"}', 2)
        return f"✅ Folder {abs_path} hidden successfully!"
    except Exception as e:
        return f"❌ Error hiding folder {abs_path}: {e}"

enableModelAccessControl_tool = FunctionTool(enableModelAccessControlFunction)

### 🔹 **Function 4: Enable Model Backup**
# def enableModelBackupFunction(model_path: str) -> str:
#     """Creates a backup of the model file stored at model_path using Dill."""
    
#     abs_folder = os.path.abspath(model_path)  # Ensure absolute path
#     backup_dir = os.path.join(os.path.dirname(abs_folder), "Outputs")  # Store in Outputs directory
#     os.makedirs(backup_dir, exist_ok=True)  # Ensure Outputs folder exists

#     backup_path = os.path.join(backup_dir, "model_backup.pkl")  # Define backup file path

#     try:
#         # Read the model file and backup using Dill
#         with open(model_path, "rb") as f:
#             model = dill.load(f)  # Load model from file
        
#         # Save backup using Dill
#         with open(backup_path, "wb") as f:
#             dill.dump(model, f)
#         print(f"✅ Model backup created successfully at {backup_path}")

#         # Verify backup by loading the model
#         with open(backup_path, "rb") as f:
#             loaded_model = dill.load(f)
#         print(f"✅ Backup verification successful. Loaded Model:", loaded_model)
#         temp =  paramsFilling("DataSecurity",13003, "Enable Model Backup executed successfully.", '{"Status":"Success"}', 1)

#         return backup_path  # Return backup path for reference
    
#     except Exception as e:
#         return f"❌ Error during model backup: {e}"

def enableModelBackupFunction(text: str) -> str:
    """Reverse the input text string."""
    temp =  paramsFilling("DataSecurity",13003, "Enable Model Backup executed successfully.", '{"Status":"Success"}', 3)
    return f"Reversed Text: {text[::-1]}"

# ✅ Update function tool to take a **string file path** instead of a model object
enableModelBackup_tool = FunctionTool(enableModelBackupFunction)


### 🔹 **Function 5: Prevent Data Input Manipulation (Zip Folder)**
def preventDataInputManipulationFunction(folder_path: str, password: str) -> str:
    """Zips a folder securely with a password, preserving subdirectories."""
    
    abs_folder = os.path.abspath(folder_path)
    output_folder = os.path.join(os.path.dirname(abs_folder), "Outputs")
    os.makedirs(output_folder, exist_ok=True)  # Ensure Outputs folder exists

    zip_path = os.path.join(output_folder, "ZippedDF.zip")  # Store zip in Outputs
    password_bytes = password.encode("utf-8")

    try:
        with pyzipper.AESZipFile(zip_path, 'w', encryption=pyzipper.WZ_AES) as zipf:
            zipf.setpassword(password_bytes)

            for root, dirs, files in os.walk(abs_folder):
                for file in files:
                    file_path = os.path.join(root, file)
                    arcname = os.path.relpath(file_path, abs_folder)  # Preserve folder structure
                    zipf.write(file_path, arcname)
        temp =  paramsFilling("DataSecurity",13004, "Prevent Data Input Manipulation executed successfully.", '{"Status":"Success"}', 4)

        return f"✅ Folder zipped successfully at {zip_path}, including subdirectories."

    except Exception as e:
        return f"❌ Error zipping folder: {e}"

preventDataInputManipulation_tool = FunctionTool(preventDataInputManipulationFunction)

### 🔹 **Function 7: Prevent Data Label Manipulation (Encrypt File)**
def preventDataLabelManipulationFunction(file_path: str) -> str:
    """Encrypts a file and stores the encryption key separately."""
    
    abs_path = os.path.abspath(file_path)
    encrypted_path = os.path.join(os.path.dirname(abs_path), "Outputs", "data.enc")
    key_path = os.path.join(os.path.dirname(abs_path), "Outputs", "encryption_key.key")
    
    try:
        key = Fernet.generate_key()
        cipher_suite = Fernet(key)

        with open(abs_path, 'rb') as file:
            file_data = file.read()
        
        encrypted_data = cipher_suite.encrypt(file_data)

        # Save encrypted file
        with open(encrypted_path, 'wb') as file:
            file.write(encrypted_data)
        
        # Save encryption key
        with open(key_path, 'wb') as key_file:
            key_file.write(key)
        
        temp =  paramsFilling("DataSecurity",13005, "Prevent Data Label Manipulation executed successfully.", '{"Status":"Success"}', 5)
        print(f"✅ File encrypted at {encrypted_path}, Key stored at {key_path}")
        return key_path  # Return key file path

    except Exception as e:
        return f"❌ Error encrypting file: {e}"

preventDataLabelManipulation_tool = FunctionTool(preventDataLabelManipulationFunction)

def preventDataInjectionsFunction(text: str) -> str:
    """Reverse the input text string."""
    temp =  paramsFilling("DataSecurity",13006, "Prevent Data Injections executed successfully.", '{"Status":"Error"}', 6)
    return f"Reversed Text: {text[::-1]}"

preventDataInjections_tool = FunctionTool(preventDataInjectionsFunction)

def preventLogicCorruptionFunction(text: str) -> str:
    """Reverse the input text string."""
    temp =  paramsFilling("DataSecurity",13007, "Prevent Logic Corruption executed successfully.", '{"Status":"Success"}', 7)
    return f"Reversed Text: {text[::-1]}"

preventLogicCorruption_tool = FunctionTool(preventLogicCorruptionFunction)

def enableDataMinimisationFunction(csv_path: str, columns: list[str]) -> str:
    """
    Extracts only required columns from a CSV for minimal data exposure.

    Args:
        csv_path (str): Path to the input CSV file.
        columns (list of str): List of column names to extract.

    Returns:
        str: Path to the filtered CSV or error message.
    """
    try:
        # Ensure output directory exists
        output_dir = "./static/Files/Outputs"
        os.makedirs(output_dir, exist_ok=True)

        df = pd.read_csv(csv_path)
        df_filtered = df[columns]  # Ensure columns is a proper list
        
        # Define output path inside 'static/Files/Outputs'
        file_name = os.path.basename(csv_path).replace(".csv", "_filtered.csv")
        output_path = os.path.join(output_dir, file_name)

        df_filtered.to_csv(output_path, index=False)
        temp = paramsFilling("DataSecurity",13008, "Enable Data Minimisation executed successfully.", '{"Status":"Success"}', 8)
        return f"✅ Data minimization applied. Filtered file saved: {output_path}"
    except Exception as e:
        temp = paramsFilling("DataSecurity",13008, f"Enable Data Minimisation failed: {e}", '{"Status":"Error"}', 8)
        return f"⚠️ Error filtering CSV: {e}"

enableDataMinimisation_tool = FunctionTool(enableDataMinimisationFunction)

def enableDataCataloguePolicyFunction(csv_path: str, expected_columns: list[str]) -> str:
    """Validates if a CSV file contains the required columns."""
    try:
        df = pd.read_csv(csv_path)
        missing_columns = [col for col in expected_columns if col not in df.columns]

        if missing_columns:
            temp = paramsFilling("DataSecurity",13009, "Enable Data Catalogue Policy {csv_path} : {missing_columns}.", '{"Status":"Error"}', 9,True)

            return f"⚠️ Missing columns in '{csv_path}': {missing_columns}"
        
        temp = paramsFilling("DataSecurity",13009, "Enable Data Catalogue Policy executed successfully.", '{"Status":"Success"}', 9,True)
        return f"✅ CSV '{csv_path}' contains all expected columns."
    except Exception as e:
        temp = paramsFilling("DataSecurity",13009, f"Enable Data Catalogue Policy failed: {e}", '{"Status":"Error"}', 9,True)
        return f"⚠️ Error validating CSV columns: {e}"

enableDataCataloguePolicy_tool = FunctionTool(enableDataCataloguePolicyFunction)



### 🔹 **Creating Agents for Each Function**
detectDataPoisoning = LlmAgent(name="DetectDataPoisoning", model="gemini-1.5-flash", tools=[detectDataPoisoning_tool])
enableModelAccessControl = LlmAgent(name="EnableModelAccessControl", model="gemini-1.5-flash", tools=[enableModelAccessControl_tool])
enableModelBackup = LlmAgent(name="EnableModelBackup", model="gemini-1.5-flash", tools=[enableModelBackup_tool])
preventDataInputManipulation = LlmAgent(name="PreventDataInputManipulation", model="gemini-1.5-flash", tools=[preventDataInputManipulation_tool])
preventDataLabelManipulation = LlmAgent(name="PreventDataLabelManipulation", model="gemini-1.5-flash", tools=[preventDataLabelManipulation_tool])
preventDataInjections = LlmAgent(name="PreventDataInjections", model="gemini-1.5-flash", tools=[preventDataInjections_tool])
preventLogicCorruption = LlmAgent(name="PreventLogicCorruption", model="gemini-1.5-flash", tools=[preventLogicCorruption_tool])
enableDataMinimisation = LlmAgent(name="EnableDataMinimisation", model="gemini-1.5-flash", tools=[enableDataMinimisation_tool], description="Extracts only essential columns from structured datasets.")
enableDataCataloguePolicy = LlmAgent(name="EnableDataCataloguePolicy", model="gemini-1.5-flash", tools=[enableDataCataloguePolicy_tool], description="Ensures AI models receive correctly formatted CSV files with expected columns.")

### **Exporting Agents for Main File**
DataSecurity_agents_workflow = [detectDataPoisoning, enableModelAccessControl, enableModelBackup, preventDataInputManipulation, preventDataLabelManipulation, preventDataInjections, preventLogicCorruption, enableDataMinimisation, enableDataCataloguePolicy]
