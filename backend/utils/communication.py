# backend/utils/communication.py

from typing import Dict
import json
from .skill_storage import store_message

def send_message(recipient, message: str):
    # In a real-world scenario, this function would use a messaging system or API
    # to send messages between agents. For this example, we'll just print the message.
    print(f"Message to {recipient.name}: {message}")
    
    # Store the message for future reference
    store_message(sender_id="system", recipient_id=recipient.id, message=message)

def broadcast_message(agents, message: str):
    for agent in agents:
        send_message(agent, message)

def format_task_message(task: Dict) -> str:
    return json.dumps({
        "task_id": task["id"],
        "description": task["description"],
        "requirements": task["requirements"],
        "priority": task["priority"]
    })

def parse_task_message(message: str) -> Dict:
    return json.loads(message)

def request_help(agent, task: Dict, skill_needed: str):
    help_message = f"Help needed for task {task['id']}. Skill required: {skill_needed}"
    send_message(agent, help_message)

def respond_to_help_request(helper_agent, requesting_agent, task: Dict, solution: str):
    response_message = f"Solution for task {task['id']}: {solution}"
    send_message(requesting_agent, response_message)

def notify_task_completion(lead_developer, agent, task: Dict):
    completion_message = f"Task {task['id']} completed by {agent.name}"
    send_message(lead_developer, completion_message)

def request_code_review(reviewer_agent, task: Dict, code: str):
    review_request = f"Please review the code for task {task['id']}:\n\n{code}"
    send_message(reviewer_agent, review_request)

def submit_code_review(author_agent, task: Dict, review_result: Dict):
    review_message = f"Code review for task {task['id']}:\n"
    review_message += f"Approved: {'Yes' if review_result['approved'] else 'No'}\n"
    review_message += f"Feedback: {review_result['feedback']}"
    send_message(author_agent, review_message)