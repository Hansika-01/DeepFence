import hashlib
import os

def calculate_file_hash(filepath, hash_algorithm='sha256'):
    """Calculates the hash of a file."""
    hasher = hashlib.new(hash_algorithm)
    with open(filepath, 'rb') as f:
        while chunk := f.read(8192): # Read in chunks to handle large files
            hasher.update(chunk)
    return hasher.hexdigest()

def verify_file_integrity(filepath, expected_hash, hash_algorithm='sha256'):
    """Verifies the integrity of a file against an expected hash."""
    current_hash = calculate_file_hash(filepath, hash_algorithm)
    if current_hash == expected_hash:
        print(f"✅ File '{filepath}' integrity verified. Hash matches.")
        return True
    else:
        print(f"❌ File '{filepath}' integrity compromised!")
        print(f"   Expected: {expected_hash}")
        print(f"   Actual:   {current_hash}")
        return False

# --- Demonstration of Hashing ---
print("--- 1. Hashing for Data Integrity ---")

# Create a dummy data file
original_content = "This is some important data for machine learning."
file_name = "ml_data.txt"
with open(file_name, 'w') as f:
    f.write(original_content)
print(f"Created original file: '{file_name}'")

# Calculate its initial hash
initial_hash = calculate_file_hash(file_name, 'sha256')
print(f"Initial SHA256 hash of '{file_name}': {initial_hash}")

# Simulate a check immediately after creation
verify_file_integrity(file_name, initial_hash)

# Simulate data manipulation (e.g., accidental change or malicious tampering)
print(f"\nSimulating data manipulation in '{file_name}'...")
with open(file_name, 'a') as f: # Append some data
    f.write("\nMalicious injection!")

# Verify again
print(f"Verifying '{file_name}' after manipulation:")
verify_file_integrity(file_name, initial_hash)

# Clean up
os.remove(file_name)
print("\n--- Hashing demonstration complete ---")