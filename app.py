import streamlit as st
from load_lstm import LSTM_functions
from load_bert import BertClassifier, BertClassifierMultiLabel
from utils import process_image
from gemini import Suggestions_model, log
import time
import os
from PIL import Image
import pandas as pd  # Import pandas for CSV handling

# Disable oneDNN optimizations
os.environ['TF_ENABLE_ONEDNN_OPTS'] = '1'

# Initialize logging
log.info("Libraries Loaded")

# Streamlit UI Configuration
st.set_page_config(page_title="Cybercrime Taxonomy", page_icon="🐱‍💻", layout="wide")

# Custom CSS for background image, smooth transition, and styling
st.markdown(
    """
    <style>
        /* Background Image */
        body {
            background-image: url('https://wallpaperaccess.com/full/3288227.jpg');
            background-size: cover;
            background-position: center center;
            background-repeat: no-repeat;
            min-height: 100vh;
            color: white;
        }

        /* Gradient Overlay */
        .stApp {
            background: rgba(0, 0, 0, 0.7);  /* Black overlay with some transparency */
            padding: 20px;
            border-radius: 15px;
            border: 3px solid #FFD700;  /* Gold border to match the theme */
        }

        /* Keyframes for smooth top-to-bottom animation */
        @keyframes fadeIn {
            from {
                opacity: 0;
                transform: translateY(-20px);
            }
            to {
                opacity: 1;
                transform: translateY(0);
            }
        }

        /* Apply animation to all elements */
        .stTextInput, .stTextArea, .stButton, .stRadio, h1, h2 {
            animation: fadeIn 1s ease-in-out forwards;
        }

        /* Header text */
        h1, h2 {
            color: #FFD700;  /* Bright Gold header text */
            text-align: center;
            font-size: 2.5em;
        }

        /* Button styles */
        .stButton>button {
            background-color: #4CAF50;  /* Green color for buttons */
            color: white;  /* Fixed text color */
            font-weight: bold;
            border-radius: 15px;
            padding: 15px 30px;
            box-shadow: 0 5px 15px rgba(0, 0, 0, 0.2);
            transition: background-color 0.3s ease, box-shadow 0.3s ease;
            border: 2px solid transparent;
        }

        /* Button Hover */
        .stButton>button:hover {
            background-color: #45a049;  /* Darker Green on hover */
            box-shadow: 0 5px 25px rgba(0, 0, 0, 0.3);
            border: 2px solid #ffffff;  /* White border on hover */
        }

        /* Button Click */
        .stButton>button:active {
            background-color: #388E3C;  /* Even darker green on click */
        }

        /* Model Selection buttons */
        .model-btn {
            padding: 15px 25px;
            font-size: 16px;
            font-weight: bold;
            border-radius: 12px;
            cursor: pointer;
            margin: 10px;
            transition: background-color 0.3s ease;
            width: 100%;
            background-color: #008CBA;
            color: white;
            border: 2px solid transparent;
        }

        /* Hover effect for model buttons */
        .model-btn:hover {
            background-color: #005f6a;
            box-shadow: 0 5px 15px rgba(0, 0, 0, 0.3);
            border: 2px solid #ffffff;
        }

        /* Text input and text area styling */
        .stTextInput input, .stTextArea textarea {
            background-color: #F0F8FF;
            color: #333333;
            border-radius: 8px;
            border: 2px solid #ADD8E6;
            padding: 10px;
            font-size: 16px;
        }

        /* Hover effect for Text input and text area */
        .stTextInput input:hover, .stTextArea textarea:hover {
            border-color: #1E90FF;
        }

        /* Placeholder styling */
        .stTextInput input::placeholder, .stTextArea textarea::placeholder {
            color: #B0C4DE;
        }

        /* Gradient Progress Bar */
        .progress-bar {
            width: 100%;
            height: 20px;
            background: linear-gradient(to right, #00C9FF, #92FE9D); /* Gradient from blue to green */
            border-radius: 10px;
            position: relative;
            box-shadow: 0 5px 15px rgba(0, 0, 0, 0.2);
        }

        .progress-bar-fill {
            height: 100%;
            border-radius: 10px;
            background: #FFD700;
            transition: width 0.2s ease;
        }

        /* Text for the loading message */
        .loading-message {
            text-align: center;
            color: white;
            font-size: 1.2em;
        }
    </style>
    """, unsafe_allow_html=True
)

# Streamlit UI Header
st.header("Cybercrime Taxonomy")

# Input fields for user details and complaint
name = st.text_input("Enter Your Name", placeholder="Shri Narendra Modi")
complaint = st.text_area("Enter Your Complaint **(Mandatory)**", placeholder="Describe your complaint here...")

# Instructional text for model selection
st.markdown("""<h4 style="color: #FFD700; text-align: center; font-size: 1.5em;">Please choose a model:</h4>""", unsafe_allow_html=True)

# Model selection as buttons displayed horizontally
cols = st.columns(3)
with cols[0]:
    if st.button("LSTM", key="lstm_model"):
        selected_model = "LSTM"
with cols[1]:
    if st.button("Bert", key="bert_model"):
        selected_model = "Bert"
with cols[2]:
    if st.button("Bert_Multilabel", key="bert_multilabel_model"):
        selected_model = "Bert_Multilabel"

# Custom file uploader button (removed redundant one)
image_file = st.file_uploader("Upload an Image", type=["png", "jpg", "jpeg"])

# Session state for confirmation
if "confirm_submission" not in st.session_state:
    st.session_state.confirm_submission = False

# Submit and Predict button
submit = st.button("Submit & Predict")

# Handle submit action
if submit:
    st.session_state.confirm_submission = True
    log.info("Submit Button clicked")
    log.info("Loading Confirmation Box")
    
    # Display loading message alongside gradient progress bar
    st.markdown("<div class='loading-message'>Please wait while we process your complaint and generate AI suggestions...</div>", unsafe_allow_html=True)
    
    # Create a placeholder for the progress bar
    progress_bar_placeholder = st.empty()
    progress_bar = progress_bar_placeholder.markdown(""" 
    <div class="progress-bar">
        <div class="progress-bar-fill" style="width: 0%;"></div>
    </div>
    """, unsafe_allow_html=True)
    
    # Simulate progress bar fill animation
    for percent_complete in range(1, 101):  # Update progress bar
        time.sleep(0.05)  # Simulate loading time
        progress_bar_placeholder.markdown(f"""
        <div class="progress-bar">
            <div class="progress-bar-fill" style="width: {percent_complete}%;"></div>
        </div>
        """, unsafe_allow_html=True)

    # After the progress bar is completed, show AI suggestions
    mdl = Suggestions_model()
    answer = mdl.get_suggestions(complaint)
    st.write(answer)

    st.warning("Do you want to continue submitting the complaint or re-enter it?")
    col1, col2 = st.columns(2)
    with col1:
        confirm = st.button("Confirm", key="confirm", help="Confirm your complaint submission")
    with col2:
        reenter = st.button("Re-enter", key="reenter", help="Re-enter your complaint")

    # Confirm action
    if confirm:
        st.session_state.confirm_submission = False
        st.success("You have confirmed! Processing your complaint...")
        log.info("Complaint confirmed for submission")

        # Call the model prediction
        if selected_model == "LSTM":
            lstm = LSTM_functions()
            preds = lstm.predict(complaint)
            st.success(preds)
        elif selected_model == "Bert_Multilabel":
            bert = BertClassifierMultiLabel()
            preds = bert.predict(complaint)
            st.success(preds)
        elif selected_model == "Bert":
            bert = BertClassifier()
            preds = bert.predict(complaint)
            st.success(preds)

        # Save the details into a CSV file
        df = pd.DataFrame({
            "Name": [name],
            "Complaint": [complaint],
            "Model": [selected_model],
            "Prediction": [preds],
        })

        # Ensure the 'database' folder exists
        folder_name = 'database'
        if not os.path.exists(folder_name):
            os.makedirs(folder_name)

        # Full file path for CSV
        file_name = os.path.join(folder_name, "complaint_prediction.csv")

        # Check if the file exists and append if so, else create a new one
        if os.path.exists(file_name):
            df.to_csv(file_name, mode='a', header=False, index=False)  # Append mode
            st.success(f"New record added to '{file_name}'.")
        else:
            df.to_csv(file_name, index=False)  # Create new file if doesn't exist
            st.success(f"CSV file '{file_name}' generated successfully in the 'database' folder.")

        # Provide a download button for the generated CSV
        with open(file_name, "rb") as file:
            st.download_button("Download Prediction Results", data=file, file_name="complaint_prediction.csv", mime="text/csv")

    # Re-enter action
    if reenter:
        st.session_state.confirm_submission = False
        st.experimental_rerun()
