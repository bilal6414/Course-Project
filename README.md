# Indian House Rent Prediction Project

This project predicts house rent prices in India based on various features like location, furnishing status, size, and more. It includes data preprocessing, model training, and deployment as a Flask-based web application.

---
![1](https://github.com/user-attachments/assets/3a060891-90a0-4ffc-93f8-c0b327ec4659)

![2](https://github.com/user-attachments/assets/b881db7d-e254-4bdf-8310-9f279f37d598)

---
## Table of Contents
1. [Overview](#overview)
2. [Problem Statement](#problem-statement)
3. [Technologies Used](#technologies-used)
4. [Dataset](#dataset)
5. [Project Workflow](#project-workflow)
6. [Installation and Setup](#installation-and-setup)
7. [Usage](#usage)
8. [Model Deployment](#model-deployment)
9. [Folder Structure](#folder-structure)
10. [Results](#results)
11. [Contributing](#contributing)
12. [License](#license)
13. [Acknowledgments](#acknowledgments)

---

## Overview

This project aims to provide a data-driven solution for predicting house rent prices in India. It involves:
- **Exploratory Data Analysis (EDA)** to clean and analyze the dataset.
- **Model Training** to build a machine learning model for predictions.
- **Deployment** of the model as a web application using Flask.

---

## Problem Statement

Renting a house in India involves several factors such as location, furnishing status, and size. This project predicts house rent prices based on these features, making the process easier and more efficient.

---

## Technologies Used

- **Python**: Programming language for data processing and modeling.
- **Pandas, NumPy**: Libraries for data manipulation and analysis.
- **Matplotlib, Seaborn**: Libraries for data visualization.
- **Scikit-learn**: For building and evaluating machine learning models.
- **Flask**: For deploying the model as a web application.
- **HTML, Bootstrap**: For the frontend of the web application.

---

## Dataset

The dataset contains information about houses, including:
- House Type
- Location
- Status (e.g Furnished , UnFurnished)
- Number of Bathrooms
- Number of Balconies
- BHK
- Rent Price (Target variable)


---

## Project Workflow

1. **Data Collection**:
   - Import and inspect the dataset.
2. **Exploratory Data Analysis (EDA)**:
   - Handle missing values, outliers, and analyze features.
   - Visualize distributions and correlations.
3. **Feature Engineering**:
   - Encode categorical variables.
   - Scale numerical features.
4. **Model Training**:
   - Train machine learning models such as Linear Regression or Random Forest.
   - Evaluate models using metrics like RMSE, MAE, and R².
5. **Model Deployment**:
   - Build a Flask-based web app for predictions.

---

## Installation and Setup

To run the project locally, follow these steps:

---

### Clone the Repository

```bash
git clone https://github.com/your-username/indian-house-rent-prediction.git
cd indian-house-rent-prediction
```
### Create a virtual environment and install the required Python libraries:
```bash
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```
---
### Run Flask App

```bash
python app.py
```

### Access the Application
Open your browser and navigate to ```http://127.0.0.1:5000.```


---
### Results
The best-performing model achieved the following metrics:
**R² Score:** 98.16
**RMSE:** 18.58
**MAE:** 13.56
