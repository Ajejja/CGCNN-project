import streamlit as st
import os
import subprocess
import pandas as pd
import matplotlib.pyplot as plt
import zipfile
import shutil
import time
from PIL import Image
import io
import base64

# Streamlit UI Setup
st.set_page_config(page_title='CGCNN Web App', layout='wide')

# Initialize session state variables
if 'dataset_uploaded' not in st.session_state:
    st.session_state.dataset_uploaded = False
if 'dataset_path' not in st.session_state:
    st.session_state.dataset_path = ""
if 'train_completed' not in st.session_state:
    st.session_state.train_completed = False
if 'predict_dataset_uploaded' not in st.session_state:
    st.session_state.predict_dataset_uploaded = False  
if 'progress' not in st.session_state:
    st.session_state.progress = 0  
if 'show_progress' not in st.session_state:
    st.session_state.show_progress = False  

dataset_path = "data/uploaded_dataset"
predict_path = "data/predict_dataset"

# Function to handle ZIP uploads and extraction
def upload_and_extract(zip_file, save_path, session_key):
    os.makedirs(save_path, exist_ok=True)
    zip_path = os.path.join(save_path, "uploaded_dataset.zip")

    with open(zip_path, "wb") as f:
        f.write(zip_file.getbuffer())

    with zipfile.ZipFile(zip_path, 'r') as zip_ref:
        zip_ref.extractall(save_path)

    os.remove(zip_path)

    macosx_path = os.path.join(save_path, "__MACOSX")
    if os.path.exists(macosx_path):
        shutil.rmtree(macosx_path)

    extracted_files = os.listdir(save_path)
    if len(extracted_files) == 1 and os.path.isdir(os.path.join(save_path, extracted_files[0])):
        extracted_subfolder = os.path.join(save_path, extracted_files[0])
        for file in os.listdir(extracted_subfolder):
            shutil.move(os.path.join(extracted_subfolder, file), save_path)
        shutil.rmtree(extracted_subfolder)  

    required_files = ["id_prop.csv"]
    missing_files = [f for f in required_files if not os.path.exists(os.path.join(save_path, f))]
    if missing_files:
        st.error(f"Missing required files: {', '.join(missing_files)}. Please upload a valid dataset.")
        return False

    st.success("Dataset extracted successfully!")
    st.session_state[session_key] = True  
    st.session_state.dataset_path = save_path  
    return True

# Sidebar for navigation
st.sidebar.title("Navigation")
page = st.sidebar.radio("Go to", ["Train Dataset", "Model Parameters", "Training Results", "Predict"])

# Page 1: Train Dataset
if page == "Train Dataset":
    st.title("Upload Your Dataset Folder (as ZIP)")
    
    uploaded_zip = st.file_uploader("Upload a ZIP file containing your dataset", type=['zip'])

    if uploaded_zip and not st.session_state.dataset_uploaded:
        success = upload_and_extract(uploaded_zip, dataset_path, 'dataset_uploaded')
        if success:
            st.session_state.dataset_uploaded = True

    st.markdown("<br><br>", unsafe_allow_html=True)

    col1, col2, col3 = st.columns([1, 3, 1])  
    with col2:
        st.image("cgcnn.png", use_column_width=True, caption="Crystal Graph Convolutional Neural Network (CGCNN)")

# Page 2: Model Parameters
elif page == "Model Parameters":
    st.title("Set Model Parameters")
    
    if not st.session_state.dataset_uploaded:
        st.warning("Please upload a dataset first on the 'Train Dataset' page.")
    else:
        train_ratio = st.slider("Training Set Ratio", 0.1, 0.9, 0.6)
        test_ratio = st.slider("Test Set Ratio", 0.1, 0.9, 0.2)
        val_ratio = st.slider("Validation Set Ratio", 0.1, 0.9, 0.2)
        epochs = st.number_input("Epochs", min_value=1, value=30)
        model_name = st.text_input("Model Name", "CGCNN_Example")

        if st.button("Start Training"):
            # ✅ Reset progress bar before training starts
            st.session_state.progress = 0  
            st.session_state.show_progress = True  
            # Read GIF as binary
            def get_base64_gif(gif_path):
              """Convert a local GIF file to a base64-encoded string."""
              with open(gif_path, "rb") as file:
                  encoded_gif = base64.b64encode(file.read()).decode("utf-8")
              return f"data:image/gif;base64,{encoded_gif}"

            gif_data = get_base64_gif("experiment.gif")
            gif1 = get_base64_gif("experiment1.gif")  

         # Embed the Base64 GIF in HTML
            st.markdown(
   f"""
    <div style="display: flex; justify-content: center; gap: 20px;">
        <img src="{gif1}" width="250" height="250" autoplay loop>
        <img src="{gif_data}" width="250" height="250" autoplay loop>
    </div>
    """,
    unsafe_allow_html=True
)


            progress_bar = st.progress(0)
            status_text = st.empty()  # Placeholder for "Training in Progress" text
            status_text.text("Training in Progress...")  

            command = [
                "python", "main.py", dataset_path,
                "--train-ratio", str(train_ratio), "--val-ratio", str(val_ratio), "--test-ratio", str(test_ratio),
                "--epochs", str(epochs)
            ]

            # Start training with logs in terminal
            process = subprocess.Popen(command, text=True)

            progress_file = "progress.txt"
            while not os.path.exists(progress_file):
                time.sleep(1)

            while process.poll() is None:
                with open(progress_file, "r") as f:
                    lines = f.readlines()
                    if lines:
                        last_line = lines[-1].strip()
                        if last_line.isdigit():
                            epoch_progress = int(last_line)
                            st.session_state.progress = epoch_progress / epochs
                            progress_bar.progress(st.session_state.progress)
                time.sleep(1)

            # ✅ Hide progress bar & text when training completes
            time.sleep(1)  
            st.session_state.progress = 0
            st.session_state.show_progress = False  
            progress_bar.empty()
            status_text.empty()
            st.session_state.train_completed = True  
            st.success("Training Completed!")

            # ✅ Delete progress.txt after training completes
            if os.path.exists(progress_file):
                os.remove(progress_file)

# Page 3: Training Results
elif page == "Training Results":
    st.title("Training Results")

    results_image = "training_results.png"  

    if st.session_state.train_completed and os.path.exists(results_image):
        st.image(results_image, caption="Validation Metric Over Epochs")
    else:
        st.warning("No training results available yet. Train a model first.")


# Page 4: Predict
elif page == "Predict":
    
    st.title("Upload Test Dataset Folder (as ZIP)")
    model_choice = st.text_input("Enter Model Name", "CGCNN_Example")
    uploaded_test_zip = st.file_uploader("Upload a ZIP file containing your test dataset", type=['zip'])

    if uploaded_test_zip:
        upload_and_extract(uploaded_test_zip, predict_path, 'predict_dataset_uploaded')

    if st.button("Run Prediction"):
        command = ["python", "predict.py", f"model_best.pth.tar", predict_path]
        result = subprocess.run(command, capture_output=True, text=True)
        st.text(result.stdout)

        # Check if prediction results exist and display them
        results_file = "test_results.csv"
        if os.path.exists(results_file):
            df_results = pd.read_csv(results_file, header=None, names=["Material ID", "Other Column", "Predicted Value"])

            st.subheader("Prediction Results")

            # Create clickable links using Markdown
            df_results["Material Link"] = df_results["Material ID"].apply(
                lambda x: f"[🔗 Check Material](https://next-gen.materialsproject.org/materials/{x})"
            )

            # Select only relevant columns
            df_display = df_results[["Material ID", "Predicted Value", "Material Link"]]

            # Save results as CSV for download
            csv_file = "prediction_results.csv"
            df_display.to_csv(csv_file, index=False)

            # Place download button **above** the table
            with open(csv_file, "rb") as f:
                st.download_button(
                    label="📥 Download Results as CSV",
                    data=f,
                    file_name="prediction_results.csv",
                    mime="text/csv"
                )

            # Display the results table
            st.write("### 📊 Prediction Results Table")
            st.markdown(df_display.to_markdown(index=False), unsafe_allow_html=True)
        else:
            st.warning("No prediction results found. Please check if the model ran successfully.")
