from llama_index.llms.gemini import Gemini
from llama_index.core import PromptTemplate
from llama_index.core.query_pipeline import QueryPipeline
import os
from dotenv import load_dotenv
import json
import logging

# Load the .env file to access the API key
load_dotenv()

# Access the API key from the environment variables
api_key = os.getenv('GOOGLE_API_KEY')

# Set up logging
logging.basicConfig(level=logging.INFO)
log = logging.getLogger(__name__)

class Suggestions_model:
    def __init__(self):
        try:
            # Initialize the Gemini model using the API key
            self.llm_model = Gemini(api_key=api_key, model_name="models/gemini-1.5-pro")
            log.info("Gemini Model Initialized Successfully")
        except Exception as e:
            log.error(f"Gemini Model Initialization Failed: {e}")
            raise  # Re-raise exception after logging it for better visibility
    
    def get_suggestions(self, user_input):
        # Define the prompt template with a placeholder for the complaint
        prompt = """
        You are a front-end officer of the Cyber Crime division. You have to analyze this complaint:
        {complaint}. Provide short suggestions to improve the complaint. The suggestions 
        should be concise, exactly two lines, and make sure the user has mentioned 
        the date of the incident. If the date is missing, remind the user to include it.
        The output should be in JSON format.
        """
        
        # Initialize the prompt template with the complaint as a dynamic placeholder
        prompt_tmpl = PromptTemplate(prompt)
        
        try:
            # Create a query pipeline with the prompt template and the LLM model
            pipe = QueryPipeline(chain=[prompt_tmpl, self.llm_model], verbose=True)
            log.info("QueryPipeline Created. Starting prediction using Gemini API.")
            
            # Run the pipeline with the user input complaint
            response = pipe.run(complaint=user_input)
            log.info("Prediction using Gemini API completed. Outputting response.")
            
            # Clean up the response to ensure it's in proper JSON format
            response = response.message.content.strip()  # Remove any leading/trailing whitespaces
            response = response.replace("```json", "").replace("```", "")  # Clean up any markdown artifacts
            
            # Attempt to load the cleaned response as a JSON object
            return json.loads(response)
        except Exception as e:
            log.error(f"Error in processing the response: {e}")
            return {"error": "Failed to process the request"}
