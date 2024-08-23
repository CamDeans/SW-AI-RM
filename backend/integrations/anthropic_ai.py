import httpx
import logging
import anthropic
import re
from anthropic import Client, APIStatusError, APITimeoutError, APIConnectionError
from dotenv import load_dotenv
import json
import os
from typing import Dict, List
from config.settings import ANTHROPIC_API_KEY
from file_manager import process_generated_code


load_dotenv()

logger = logging.getLogger(__name__)

ANTHROPIC_API_KEY = os.getenv('ANTHROPIC_API_KEY')
client = anthropic.Anthropic(api_key=ANTHROPIC_API_KEY)

def generate_code_snippets(task):
    try:
        logger.info(f"Generating code snippets for task: {task}")
        response = client.completions.create(
            model="claude-2",
            prompt=f"\n\nHuman: Generate code for the following task: {task}\n\nAssistant:",
            max_tokens_to_sample=1000,
            stop_sequences=["\n\nHuman:"]
        )
        logger.info("Successfully generated code snippets")
        return response.completion
    except Exception as e:
        logger.exception(f"Unexpected error generating code snippets: {str(e)}")
        return None

def generate_code_for_task(prompt):
    client = Client(api_key=ANTHROPIC_API_KEY)
    try:
        response = client.completions.create(
            model="claude-2",
            prompt=f"\n\nHuman: {prompt}\n\nAssistant:",
            max_tokens_to_sample=1000,
            stop_sequences=["\n\nHuman:"]
        )
        return response.completion
    except httpx.HTTPStatusError as e:
        logging.error(f"HTTP error occurred: {str(e)}")
        raise
    except Exception as e:
        logging.error(f"Unexpected error occurred: {str(e)}")
        raise   

def generate_code(task_description: str, requirements: List[str]) -> str:
    try:
        prompt = f"{anthropic.HUMAN_PROMPT} Task: {task_description}\nRequirements:\n{' '.join(f'- {req}' for req in requirements)}\n\nPlease generate Python code that fulfills this task and meets all the requirements.{anthropic.AI_PROMPT}"

        message = client.completions.create(
            prompt=prompt,
            model="claude-2",
            max_tokens_to_sample=1000,
            stop_sequences=[anthropic.HUMAN_PROMPT]
        )

        return message.completion

    except Exception as e:
        logger.error(f"Error in generate_code: {e}", exc_info=True)
        raise

def generate_code_and_create_files(project_description: str, project_id: str):
    try:
        logger.debug(f"Generating code for project: {project_description}")
        prompt = f"{anthropic.HUMAN_PROMPT} {project_description}.\n\nProvide the code and file names in JSON format, like this: {{'file1.html': 'code content', 'file2.js': 'code content'}}{anthropic.AI_PROMPT}"
    
        message = client.completions.create(
            prompt=prompt,
            model="claude-2",
            max_tokens_to_sample=2000,
            stop_sequences=[anthropic.HUMAN_PROMPT]
        )
        code_map = json.loads(message.completion)
        process_generated_code(project_id, code_map)
        return code_map
    except Exception as e:
        logger.error(f"Error in generate_code_and_create_files: {e}", exc_info=True)
        raise

def analyze_task(code: str, task: Dict) -> Dict:
    try:
        prompt = f"{anthropic.HUMAN_PROMPT} Task: {task['description']}\nRequirements:\n{' '.join(f'- {req}' for req in task['requirements'])}\n\nCode:\n{code}\n\nPlease analyze this code and provide feedback on whether it meets the task requirements. Also, identify any skills demonstrated in this code.\n\nRespond in the following JSON format:\n{{\n    \"approved\": true/false,\n    \"feedback\": \"Your detailed feedback here\",\n    \"skills\": [\"list\", \"of\", \"skills\", \"demonstrated\"]\n}}{anthropic.AI_PROMPT}"

        message = client.completions.create(
            prompt=prompt,
            model="claude-2",
            max_tokens_to_sample=1000,
            stop_sequences=[anthropic.HUMAN_PROMPT]
        )

        return json.loads(message.completion)  # Convert the JSON string to a Python dictionary
    except Exception as e:
        logger.error(f"Error in analyze_task: {e}", exc_info=True)
        raise

def generate_project_artifact(artifact_type: str, project_data: Dict) -> str:
    try:
        prompt = f"{anthropic.HUMAN_PROMPT} Artifact Type: {artifact_type}\nProject Data:\n{project_data}\n\nPlease generate a {artifact_type} based on the provided project data.{anthropic.AI_PROMPT}"

        message = client.completions.create(
            prompt=prompt,
            model="claude-2",
            max_tokens_to_sample=2000,
            stop_sequences=[anthropic.HUMAN_PROMPT]
        )

        return message.completion
    except Exception as e:
        logger.error(f"Error in generate_project_artifact: {e}", exc_info=True)
        raise

def analyze_project_requirements(project_description):
    try:
        logger.info(f"Analyzing project requirements: {project_description}")
        response = client.completions.create(
            model="claude-2",
            prompt=f"\n\nHuman: Analyze the following project description and break it down into required technologies and tasks:\n\nProject: {project_description}\n\nProvide a JSON response with the following structure:\n{{\n    \"technology1\": {{\n        \"importance\": \"high/medium/low\",\n        \"tasks\": [\"task1\", \"task2\", ...]\n    }},\n    \"technology2\": {{\n        \"importance\": \"high/medium/low\",\n        \"tasks\": [\"task1\", \"task2\", ...]\n    }},\n    ...\n}}\nEnsure your response is a valid JSON object.\n\nAssistant:",
            max_tokens_to_sample=1000,
            stop_sequences=["\n\nHuman:"]
        )
        logger.info("Successfully received response from Anthropic API")
        
        # Extract JSON from the response
        json_match = re.search(r'\{.*\}', response.completion, re.DOTALL)
        if json_match:
            json_str = json_match.group(0)
            return json.loads(json_str)
        else:
            logger.error("No valid JSON found in the response")
            return None
    except json.JSONDecodeError as e:
        logger.error(f"JSON decoding error: {str(e)}")
        return None
    except Exception as e:
        logger.exception(f"Unexpected error analyzing project requirements: {str(e)}")
        return None

def improve_code(code: str, feedback: str) -> str:
    try:
        prompt = f"{anthropic.HUMAN_PROMPT} Original Code:\n{code}\n\nFeedback:\n{feedback}\n\nPlease improve the code based on the given feedback.{anthropic.AI_PROMPT}"

        message = client.completions.create(
            prompt=prompt,
            model="claude-2",
            max_tokens_to_sample=2000,
            stop_sequences=[anthropic.HUMAN_PROMPT]
        )

        return message.completion
    except Exception as e:
        logger.error(f"Error in improve_code: {e}", exc_info=True)
        raise
