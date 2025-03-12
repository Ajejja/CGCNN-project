import os
import pandas as pd
from mp_api.client import MPRester
from pymatgen.core.structure import Structure

# Replace with your Materials Project API Key
API_KEY = "API-KEY"

# Directory to save CIF files
cif_directory = "cif_files"
os.makedirs(cif_directory, exist_ok=True)

# CSV file path
csv_file_path = "materials_bandgaps.csv"

# Initialize MPRester
with MPRester(API_KEY) as mpr:
    print("🔍 Fetching materials with valid neighbors from Materials Project API...")

    try:
        # Query 5000 materials with band gap data
        materials = mpr.materials.summary.search(
            fields=["material_id", "band_gap", "structure"],  # Fetch band gap and structure
            num_chunks=20, chunk_size=100  # 🔹 Get 5000 materials
        )
    except Exception as e:
        print(f"❌ API Error: {e}")
        exit(1)

    if not materials:
        print("⚠️ No materials found. Check your API key and connection.")
        exit(1)

    print(f"✅ Successfully retrieved {len(materials)} materials!")

    # Initialize list for CSV data
    data = []

    # Loop through materials and save CIF files
    for index, material in enumerate(materials, start=1):
        material_id = material.material_id
        band_gap = material.band_gap  # Get band gap value

        # Format material ID
        formatted_material_id = f"{material_id}"

        print(f"📥 Downloading CIF for {formatted_material_id}...")

        # Get CIF structure
        try:
            structure = material.structure  # Retrieve structure directly
            if not isinstance(structure, Structure):
                raise ValueError("Invalid structure format")

            # Convert structure to CIF format
            cif_data = structure.to(fmt="cif")

            # Save CIF file
            cif_file_path = os.path.join(cif_directory, f"{formatted_material_id}.cif")
            with open(cif_file_path, "w") as cif_file:
                cif_file.write(cif_data)

            # Append material ID and band gap to the dataset
            data.append({"Material ID": formatted_material_id, "Band Gap (eV)": band_gap})

            # Progress update every 500 materials
            if index % 500 == 0:
                print(f"🔄 Processed {index}/5000 materials...")

        except Exception as e:
            print(f"⚠️ Skipping {formatted_material_id}: {e}")

# Create and save CSV file
df = pd.DataFrame(data)
df.to_csv(csv_file_path, index=False)

print(f"\n✅ Download complete! CIF files saved in '{cif_directory}'")
print(f"✅ CSV file saved as '{csv_file_path}' with material IDs and band gaps.")
