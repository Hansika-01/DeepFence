import pickle
from cryptography.fernet import Fernet
import os

# --- 1. Model Creation (for demonstration purposes) ---
# Let's create a simple dummy model object to pickle
class DummyModel:
    def __init__(self, name="MyMLModel", version="1.0"):
        self.name = name
        self.version = version
        self.parameters = {"learning_rate": 0.01, "epochs": 100}

    def predict(self, data):
        print(f"Model {self.name} v{self.version} predicting on: {data}")
        return len(data) * self.parameters["learning_rate"] # A dummy prediction

    def __str__(self):
        return f"Dummy Model: {self.name} (v{self.version})"

# Instantiate our dummy model
my_model = DummyModel()
print(f"Original Model: {my_model}")
print(f"Model Parameters: {my_model.parameters}")

# --- 2. Key Generation and Management ---
# THIS IS CRUCIAL: Generate a strong encryption key.
# In a real application, you would load this key securely, not generate it every time.
# Store this key securely!
key = Fernet.generate_key()
print(f"\nGenerated Encryption Key (STORE THIS SECURELY!): {key.decode()}")

# For demonstration, we'll save the key to a file.
# In production, use environment variables or a KMS.
key_file = 'secret.key'
with open(key_file, 'wb') as f:
    f.write(key)
print(f"Encryption key saved to '{key_file}' (for demonstration purposes).")

# --- 3. Encryption Function ---
def encrypt_pickle_file(model_object, output_filepath, encryption_key):
    """
    Serializes a model object using pickle, encrypts it, and saves it to a file.

    Args:
        model_object: The Python object (your model) to be pickled and encrypted.
        output_filepath (str): The path where the encrypted file will be saved.
        encryption_key (bytes): The encryption key (Fernet key).
    """
    f = Fernet(encryption_key)

    # Pickle the model object
    pickled_data = pickle.dumps(model_object)

    # Encrypt the pickled data
    encrypted_data = f.encrypt(pickled_data)

    # Write the encrypted data to a file
    with open(output_filepath, 'wb') as file:
        file.write(encrypted_data)

    print(f"\nModel encrypted and saved to '{output_filepath}'")

# --- 4. Decryption Function ---
def decrypt_pickle_file(encrypted_filepath, encryption_key):
    """
    Reads an encrypted file, decrypts it, and deserializes the model object.

    Args:
        encrypted_filepath (str): The path to the encrypted model file.
        encryption_key (bytes): The encryption key (Fernet key).

    Returns:
        The decrypted and unpickled model object.
    """
    f = Fernet(encryption_key)

    # Read the encrypted data from the file
    with open(encrypted_filepath, 'rb') as file:
        encrypted_data = file.read()

    # Decrypt the data
    decrypted_data = f.decrypt(encrypted_data)

    # Unpickle the model object
    model_object = pickle.loads(decrypted_data)

    return model_object

# --- 5. Demonstrate Encryption and Decryption ---

encrypted_model_file = 'encrypted_model.pickle'

# Encrypt the model
encrypt_pickle_file(my_model, encrypted_model_file, key)

# --- Now, simulate loading and decrypting the model ---
print(f"\n--- Loading and Decrypting Model from '{encrypted_model_file}' ---")

# In a real scenario, you would load the key from your secure storage here
# For demonstration, we'll load it from the file we just saved
with open(key_file, 'rb') as f:
    loaded_key = f.read()

# Decrypt and load the model
loaded_model = decrypt_pickle_file(encrypted_model_file, loaded_key)

print(f"Decrypted Model: {loaded_model}")
print(f"Decrypted Model Parameters: {loaded_model.parameters}")

# Test the loaded model
dummy_input = [10, 20, 30]
result = loaded_model.predict(dummy_input)
print(f"Prediction result: {result}")

# --- 6. Cleanup (Optional) ---
# Remove the generated files
os.remove(encrypted_model_file)
os.remove(key_file)
print("\nCleaned up generated files.")