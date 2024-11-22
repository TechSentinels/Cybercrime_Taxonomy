## Cybercrime Taxonomy -NCRP Assistant Overview

The **NCRP Assistant** is an innovative complaint management system designed to streamline the process of submitting and managing complaints related to cybercrime. By leveraging **AI-driven suggestions** and the powerful capabilities of **Gemini**, this application enhances user experience through intelligent categorization and personalized recommendations.

## 🚀 Prerequisites

Before you begin, ensure you have the following installed:

- **Anaconda** (for environment management)
- **Python 3.9.4**
- **Google Cloud Service Account Key** (if applicable)

## 🛠️ Setup Instructions

### 1. Create a New Environment
To start, create a virtual environment with the required version of Python:

```bash
conda create -n venv python==3.9.4
```

### 2. Activate the Virtual Environment
Activate your environment by running:

```bash
conda activate venv
```

### 3. Install Requirements
Install the necessary dependencies:

```bash
pip install -r requirements.txt
```

### 4. Add Your Gemini Google API Key
Open the `env.txt` file in your project directory and add your Gemini Google API key:

```plaintext
GEMINI_API_KEY=YOUR_GEMINI_API_KEY
```

### 5. Set Up Google Cloud Authentication (If Applicable)
If using Gemini's API with Google Cloud services, follow these steps:

- **Create a Service Account Key:**
  1. Go to the Google Cloud Console.
  2. Navigate to IAM & Admin > Service Accounts.
  3. Select your project and click on "Create Service Account."
  4. Assign the necessary permissions and click "Done."
  5. Download the JSON key file for your service account.

- **Set the GOOGLE_APPLICATION_CREDENTIALS Environment Variable:**
  - On Linux/macOS:
    ```bash
    export GOOGLE_APPLICATION_CREDENTIALS="/path/to/service-account-file.json"
    ```
  - On Windows:
    ```cmd
    set GOOGLE_APPLICATION_CREDENTIALS=C:\path\to\service-account-file.json
    ```

**Troubleshooting:** If you encounter issues like "Compute Engine Metadata server unavailable" or "Gemini Model Initialization Failed," verify that the `GOOGLE_APPLICATION_CREDENTIALS` path is correct and that the environment variable is properly set.

### 🎉 Run the Streamlit Application
To run the application, execute:

```bash
streamlit run app.py
```

If you face authentication issues, revisit Step 5 to ensure correct setup of the service account key.

## 🧑‍💻 NCRP Assistant User Flow

The NCRP Assistant enhances the complaint submission process through intelligent features:

1. **Complaint Submission:** Users can submit complaints by providing basic details such as their name and complaint description.
2. **Categorization and Suggestions:** As users type their complaints, AI models analyze input to provide real-time categorization and suggestions for improving clarity and completeness.
3. **Personalized Recommendations:** The assistant utilizes previous complaints and organizational knowledge to suggest relevant information or actions for effective issue resolution.
4. **Efficient Complaint Management:** The advanced features enable organizations to quickly understand complaint nature, facilitating tailored responses for better outcomes.

## 🧑‍💼 Key Features

- **AI-Powered Categorization:** Automatically categorizes complaints based on user input.
- **Real-Time Suggestions:** Offers suggestions to enhance clarity and quality of complaints.
- **Personalized Recommendations:** Provides relevant information or actions based on past complaints.
- **Interactive Streamlit UI:** Delivers a smooth and intuitive user interface.
- **Easy Setup:** Quick installation with clear instructions.

## 📜 License

This project is licensed under the MIT License.

## 🌟 Acknowledgments

- **Gemini API** for its powerful language processing capabilities.
- **Streamlit** for enabling interactive web app development.
- **Google Cloud** for robust services and authentication systems.

## Working:
https://github.com/user-attachments/assets/3a0fd246-0987-4d9e-b095-b0d75bc0ed0a



Citations:
[1] https://kanerika.com/blogs/google-gemini-ai/

[2] https://cloud.google.com/vertex-ai/generative-ai/docs/models/tune_gemini/tune-gemini-learn

[3] https://www.techtarget.com/searchenterpriseai/definition/Google-Gemini

[4] https://redapplelearning.in/google-ai-gemini-vs-chatgpt-which-ai-language-model-is-better/

[5] https://dorik.com/blog/how-to-use-gemini-ai

[6] https://blog.google/technology/ai/google-gemini-ai/

[7] https://deepmind.google/technologies/gemini/

[8] https://cloud.google.com/gemini/docs/codeassist/supported-languages
