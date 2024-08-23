import openai
import anthropic

# Function to interact with the Anthropic API and generate code for a specific task
def generate_code_for_task(task_description):
    prompt = f"Write the full C# code for the following Unity task: {task_description}"
    
    # Assuming you have an API client set up for Anthropic
    response = anthropic_api.send_request(prompt)
    
    # Extract the code from the response
    code = response.get('completion')
    
    return code
