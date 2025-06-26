import pandas as pd
import numpy as np

def detect_corrupted_data(file_path):
    """
    Detects various types of corrupted data in a CSV file.

    Args:
        file_path (str): The path to the CSV file.

    Returns:
        None: Prints out the detected issues.
    """
    print(f"\n--- Analyzing file: {file_path} ---")

    try:
        # 1. Attempt to load the CSV: Malformed rows/columns can cause errors
        # Set 'header=None' initially to catch issues with headers or rows
        # 'error_bad_lines=False' is deprecated, so we'll catch parsing errors
        # using 'on_bad_lines' (in pandas 1.3.0+ use 'on_bad_lines='warn'' or 'skip')
        # For older pandas versions, use 'error_bad_lines=False'
        try:
            df = pd.read_csv(file_path, header=0) # Try with header first
        except pd.errors.ParserError as e:
            print(f"**Issue: Parser Error during initial load!** This often indicates malformed rows (e.g., too many/few columns). Error: {e}")
            print("Attempting to load again with 'on_bad_lines='skip'' to identify problematic rows.")
            df = pd.read_csv(file_path, header=0, on_bad_lines='skip') # Skip bad lines to proceed with analysis

        print(f"\nDataFrame loaded successfully with {len(df)} rows and {len(df.columns)} columns.")
        print("Initial DataFrame head:")
        print(df.head())

        # 2. Check for missing values (NaN, None, empty strings, etc.)
        print("\n--- 2. Missing Values ---")
        missing_values = df.isnull().sum()
        missing_percentage = (missing_values / len(df)) * 100
        missing_df = pd.DataFrame({'Missing Count': missing_values, 'Percentage': missing_percentage})
        if missing_df['Missing Count'].sum() > 0:
            print("Detected missing values:")
            print(missing_df[missing_df['Missing Count'] > 0])
        else:
            print("No missing values detected using isnull().")

        # 3. Check for incorrect data types
        print("\n--- 3. Incorrect Data Types ---")
        for column in df.columns:
            # Attempt to convert to a more appropriate type if possible
            original_dtype = df[column].dtype
            try:
                # Try converting to numeric, then to datetime, otherwise keep as object
                if original_dtype == 'object':
                    # Check if all values can be numeric
                    if pd.to_numeric(df[column], errors='coerce').notna().all():
                        print(f"Column '{column}': Can be converted to numeric (currently object). Potential data type issue.")
                    elif pd.to_datetime(df[column], errors='coerce').notna().all():
                        print(f"Column '{column}': Can be converted to datetime (currently object). Potential data type issue.")
                    else:
                        print(f"Column '{column}': Is object type, contains non-numeric/non-datetime entries. Example: {df[column].iloc[df[column].apply(lambda x: not isinstance(x, (int, float, complex, np.number, pd.Timestamp)), axis=1)].head().tolist()}")
                else:
                    print(f"Column '{column}': Type is {original_dtype}.")
            except Exception as e:
                print(f"Error checking type for column '{column}': {e}")
                print(f"Column '{column}' current type: {original_dtype}. Contains problematic entries. Example: {df[column].head().tolist()}")

        # 4. Detect outliers (example using IQR for numerical columns)
        print("\n--- 4. Outliers (Numerical Columns) ---")
        for column in df.select_dtypes(include=np.number).columns:
            Q1 = df[column].quantile(0.25)
            Q3 = df[column].quantile(0.75)
            IQR = Q3 - Q1
            lower_bound = Q1 - 1.5 * IQR
            upper_bound = Q3 + 1.5 * IQR
            outliers = df[(df[column] < lower_bound) | (df[column] > upper_bound)]
            if not outliers.empty:
                print(f"Column '{column}': Detected {len(outliers)} outliers.")
                print(outliers[[column]].head())
            else:
                print(f"Column '{column}': No obvious outliers detected using IQR method.")

        # 5. Check for inconsistent categorical values (e.g., 'Male' vs 'male')
        print("\n--- 5. Inconsistent Categorical Values ---")
        for column in df.select_dtypes(include='object').columns:
            unique_values = df[column].unique()
            if len(unique_values) > 0 and isinstance(unique_values[0], str): # Check if values are strings
                # Convert to lowercase and check for inconsistencies
                lower_case_unique = pd.Series(unique_values).str.lower().unique()
                if len(unique_values) != len(lower_case_unique):
                    print(f"Column '{column}': Inconsistent casing detected. Original unique: {unique_values}, Lowercase unique: {lower_case_unique}")
                elif len(unique_values) > 20: # Arbitrary threshold for too many unique values
                    print(f"Column '{column}': Has a large number of unique values ({len(unique_values)}). Consider if this column should be categorical or if there are typos. Sample: {unique_values[:5]}")
                else:
                    print(f"Column '{column}': Appears consistent in casing or has few unique values. Unique: {unique_values}")
            elif len(unique_values) == 0:
                 print(f"Column '{column}': No unique values (column might be empty after cleaning).")
            else:
                 print(f"Column '{column}': Contains non-string object types, skipping case consistency check.")


        # 6. Check for duplicate rows
        print("\n--- 6. Duplicate Rows ---")
        duplicates = df[df.duplicated()]
        if not duplicates.empty:
            print(f"Detected {len(duplicates)} duplicate rows:")
            print(duplicates.head())
        else:
            print("No duplicate rows detected.")

        # 7. Check for rows with an unexpected number of columns (requires re-reading with no header)
        # This is harder to catch if pandas successfully infers columns initially.
        # It's often caught by ParserError, but sometimes can create NaN columns.
        print("\n--- 7. Malformed Rows (e.g., wrong number of columns) ---")
        try:
            # Re-read without a header to count columns per row
            with open(file_path, 'r') as f:
                lines = f.readlines()
            # Assuming first row is header, skip it for data rows
            if len(lines) > 1:
                # Check column count of the first data row
                expected_cols = len(lines[1].strip().split(','))
                malformed_rows = []
                for i, line in enumerate(lines[1:]): # Start from 1 to skip header
                    current_cols = len(line.strip().split(','))
                    if current_cols != expected_cols:
                        malformed_rows.append(f"Row {i+2}: Expected {expected_cols} columns, got {current_cols}. Content: {line.strip()}")
                if malformed_rows:
                    print("Detected malformed rows:")
                    for row_info in malformed_rows:
                        print(row_info)
                else:
                    print("No obvious malformed rows (unexpected column counts per row) detected after initial load.")
            else:
                print("CSV has too few lines to check for malformed rows beyond initial parser error.")
        except Exception as e:
            print(f"Error checking for malformed rows manually: {e}")


    except FileNotFoundError:
        print(f"Error: File not found at {file_path}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

# Run the detection on our corrupted file
detect_corrupted_data('corrupted_data.csv')

# Example of a clean file
print("\n--- Testing with a clean CSV file ---")
clean_data = {
    'feature1': [1, 2, 3, 4, 5],
    'feature2': [10.1, 11.2, 12.3, 13.4, 14.5],
    'feature3': ['Apple', 'Banana', 'Cherry', 'Date', 'Elderberry'],
    'target': [0, 1, 0, 1, 0]
}
df_clean = pd.DataFrame(clean_data)
df_clean.to_csv('clean_data.csv', index=False)
detect_corrupted_data('clean_data.csv')

# Clean up the created files
import os
os.remove('corrupted_data.csv')
os.remove('clean_data.csv')
print("\nCleaned up dummy CSV files.")