import os
import pandas as pd
from mp_api.client import MPRester

# Replace with your Materials Project API Key
API_KEY = 'dkf3W24fQGTCES3r2uRQAd6io8W63TvJ'  # 

# Directory to save CIF files
cif_directory = 'cif_files'
os.makedirs(cif_directory, exist_ok=True)

# CSV file path
csv_file_path = "materials_formation_energies.csv"

# Initialize MPRester
with MPRester(API_KEY) as mpr:
    print("🔍 Fetching materials from Materials Project API...")

    try:
        # Query 5000 materials with formation energy data
        materials = mpr.materials.summary.search(
            fields=['material_id', 'formation_energy_per_atom'],  
            num_chunks=50, chunk_size=100  # Fetch 5000 materials efficiently
        )
    except Exception as e:
        print(f"❌ API Error: {e}")
        exit(1)

    # Check if we got any results
    if not materials:
        print("⚠️ No materials found. Check your API key and connection.")
        exit(1)

    print(f"✅ Successfully retrieved {len(materials)} materials!")

    # Initialize list for CSV data
    data = []

    # Loop through materials and save CIF files
    for index, material in enumerate(materials, start=1):
        material_id = material.material_id
        formation_energy = material.formation_energy_per_atom  # Get formation energy

        # Skip materials with missing formation energy
        if formation_energy is None:
            print(f"⚠️ Skipping {material_id} (No formation energy available)")
            continue

        # Format material ID with "mp-" prefix
        formatted_material_id = f"mp-{material_id}"

        print(f"📥 Downloading CIF for {formatted_material_id}...")

        # Get CIF structure
        try:
            structure = mpr.get_structure_by_material_id(material_id, final=True)
            cif_data = structure.to(fmt='cif')

            # Save CIF file as mp-materialid.cif
            cif_file_path = os.path.join(cif_directory, f"{formatted_material_id}.cif")
            with open(cif_file_path, 'w') as cif_file:
                cif_file.write(cif_data)

            # Append material ID and formation energy to the list
            data.append({'mp-materialid': formatted_material_id, 'formation_energy': formation_energy})

            # Progress update every 500 materials
            if index % 500 == 0:
                print(f"🔄 Downloaded {index}/5000 materials...")

        except Exception as e:
            print(f"⚠️ Error fetching CIF for {formatted_material_id}: {e}")

# Create and save CSV file
df = pd.DataFrame(data)
df.to_csv(csv_file_path, index=False)

print(f"\n✅ Download complete! CIF files saved in '{cif_directory}'")
print(f"✅ CSV file saved as '{csv_file_path}' with material IDs and formation energies.")
