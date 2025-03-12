import pandas as pd

def sort_csv_by_material_id(csv_file):
    """
    Reads the CSV file, sorts all rows numerically by Material ID, 
    and ensures each row remains intact with the correct Formation Energy.

    Args:
        csv_file (str): Path to the CSV file to be sorted.
    """
    # Load CSV
    df = pd.read_csv(csv_file)

    # Ensure Material ID is properly formatted and sort numerically
    df["Numeric ID"] = df["Material ID"].str.replace("mp-", "").astype(int)
    df = df.sort_values(by="Numeric ID").drop(columns=["Numeric ID"])  # Remove temp column

    # Save the sorted CSV
    df.to_csv(csv_file, index=False)
    print(f"✅ CSV sorted successfully: {csv_file}")

# Example usage
csv_path = "materials_bandgaps.csv"  
sort_csv_by_material_id(csv_path)
