# App Overview

## Project Description
In this project, I developed a web application that simplifies the process of predicting material properties using the CGCNN model. The app is designed to allow users to upload their datasets and intuitively perform model training and prediction. Additionally, I have included a folder named 'MTcgcnn1' in the repository as an example to demonstrate how the dataset should be formatted for those unfamiliar with CGCNN. This makes it accessible for users without programming knowledge to engage in materials design using machine learning.

![Image](https://github.com/user-attachments/assets/0a5b079a-6aa3-460f-b550-ff5acf0d4da3)




## User Interface and Functionality

This web application is built using Streamlit and offers the following main features:

- **Data Upload Function**: Allows easy uploading of CIF files or CSV data.
  
- **Model Training**: Users can specify datasets and set arbitrary parameters (such as the number of epochs and learning rate) to execute training.
- 
  <img width="600" alt="Image" src="https://github.com/user-attachments/assets/7aca24ca-94a6-4c60-abab-4dbc47898214" />

- **Display of Training Results**: Users can view the results of the training process within the application.
  The user interface tracks changes in MAE (Mean Absolute Error) during the model training process and analyzes the trends. It records the progression of MAE at each epoch and visualizes the changes in prediction accuracy as training progresses.

  <img width="459" alt="Image" src="https://github.com/user-attachments/assets/95e1be96-ebd0-4079-af0e-0daa3f269dee" />

- **Prediction Function**: Uses the trained model to predict the properties of new materials and outputs the results as a downloadable CSV file. 

  Additionally, the prediction results table includes a **"Check Material"** link for each material. Clicking this link redirects users to the official **Materials Project** website, where they can verify actual material data and property values. 

  This feature allows users to easily compare and validate the model's prediction accuracy.
  
<img width="459" alt="Image" src="https://github.com/user-attachments/assets/229bbdb4-5fdb-4922-8ae6-005565b8a404" />

## Technologies and Tools

This project leverages a variety of technologies and tools to ensure efficient and effective material property predictions using machine learning:

- **Streamlit**: For creating an intuitive web interface that allows users to interact with the machine learning model directly.
- **Python**: The primary programming language used for developing the CGCNN model and handling data manipulation.
- **PyTorch**: Utilized for building and training the CGCNN model thanks to its flexibility and powerful GPU acceleration capabilities.
- **Pandas**: Used for data handling and transformations, making it easier to manage and prepare data for model training.
- **NumPy**: Essential for numerical computations, especially for manipulating large arrays and matrices of numeric data.
- **Matplotlib** and **Seaborn**: For generating visualizations of the data and results, helping to interpret the performance and outcomes of the model.
- **Materials Project API**: Integrated to fetch real-time data and properties of materials, enriching the dataset used for training and predictions.

These tools and technologies were chosen to maximize efficiency and maintain high standards of accuracy and reliability in predicting material properties.

