import os
import pandas as pd

def delete_duplicates(duplicates_file):
    """Read the duplicates file and delete duplicate files."""
    df = pd.read_excel(duplicates_file)
    
    for _, row in df.iterrows():
        duplicate_file = row['Duplicate File']
        if os.path.exists(duplicate_file):
            try:
                os.remove(duplicate_file)
                print(f"Deleted {duplicate_file}.")
            except Exception as e:
                print(f"Error deleting file {duplicate_file}: {e}")
        else:
            print(f"File {duplicate_file} does not exist or has already been deleted.")

if __name__ == "__main__":
    duplicates_file = "duplicates.xlsx"
    delete_duplicates(duplicates_file)
