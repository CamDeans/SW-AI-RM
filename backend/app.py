import os
import sys
import json
import logging
import threading
import time
from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
from dotenv import load_dotenv

# Add the current directory to the Python path
current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, current_dir)

from backend.core.swarm_structure import SwarmStructure
from backend.core.task_manager import TaskManager
from backend.integrations.anthropic_ai import generate_code_snippets, analyze_project_requirements

load_dotenv()

# Set up logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "http://localhost:3000"}})

# Create instances of SwarmStructure and TaskManager
swarm = SwarmStructure()
task_manager = TaskManager()

# Add a new dictionary to store code snippets
code_snippets_cache = {}

def update_tasks():
    while not task_manager.wait_for_all_tasks_completed(timeout=5):
        all_completed = task_manager.process_tasks()
        logger.info(f"Tasks progressed. All completed: {all_completed}")
    logger.info("All tasks completed. Task update loop has ended.")

# Start the update_tasks function in a separate thread
task_update_thread = threading.Thread(target=update_tasks)
task_update_thread.start()

@app.route('/tasks', methods=['GET'])
def get_tasks():
    all_tasks = task_manager.get_all_tasks()
    task_status = {
        "pending": [task for task in all_tasks if task['status'] == 'pending'],
        "in_progress": [task for task in all_tasks if task['status'] == 'in_progress'],
        "completed": [task for task in all_tasks if task['status'] == 'completed']
    }
    logger.info(f"Current task status: {task_status}")
    return jsonify(task_status)

@app.route('/projects', methods=['POST'])
def create_project():
    project_description = request.json.get('description')
    logger.info(f"Received project description: {project_description}")

    try:
        logger.info("Analyzing project requirements")
        requirements = analyze_project_requirements(project_description)
        if requirements is None:
            logger.error("Failed to analyze project requirements")
            return jsonify({"error": "Failed to analyze project requirements"}), 500
        
        logger.info(f"Analyzed requirements: {requirements}")
        
        logger.info("Analyzing project with lead developer")
        swarm.lead_developer.analyze_project(requirements)
        tasks = swarm.lead_developer.project_tasks
        logger.info(f"Generated tasks: {tasks}")
        
        created_task_ids = []
        for task in tasks:
            logger.info(f"Creating task: {task}")
            task_id = task_manager.create_task(task['description'], task.get('technology', []), task.get('priority', 1))
            created_task_ids.append(task_id)
            logger.info(f"Created task with ID: {task_id}")
            
            logger.info(f"Generating code snippets for task: {task['description']}")
            snippets = generate_code_snippets(task['description'])
            code_snippets_cache[task_id] = snippets
            logger.info(f"Generated snippets: {snippets}")
        
        logger.info(f"Project created with {len(created_task_ids)} tasks")
        return jsonify({
            "message": "Project created successfully",
            "agents": [agent.to_dict() for agent in swarm.get_all_agents()],
            "tasks": task_manager.get_all_tasks(),
            "created_task_ids": created_task_ids
        }), 201
    except Exception as e:
        logger.error(f"Error creating project: {str(e)}")
        logger.exception("Exception details:")
        return jsonify({"error": f"Internal server error: {str(e)}"}), 500

@app.route('/swarm/status', methods=['GET'])
def get_swarm_status():
    try:
        return jsonify({
            "agents": [agent.to_dict() for agent in swarm.get_all_agents()],
            "tasks": task_manager.get_all_tasks()
        })
    except Exception as e:
        logger.error(f"Error getting swarm status: {str(e)}")
        return jsonify({"error": "Internal server error"}), 500

@app.route('/api/code_snippets/<task_id>', methods=['GET'])
def get_code_snippet(task_id):
    task = task_manager.get_task(task_id)
    if task:
        if task_id in code_snippets_cache:
            snippet = code_snippets_cache[task_id]
        else:
            snippet = generate_code_snippets(task['description'])
            code_snippets_cache[task_id] = snippet
        return jsonify({"task": task, "code_snippet": snippet})
    return jsonify({"error": "Task not found"}), 404

@app.route('/progress_tasks', methods=['POST'])
def progress_tasks():
    progress = task_manager.get_progress()
    all_completed = progress['completed'] == progress['total']
    return jsonify({'all_completed': all_completed, 'progress': progress})

@app.route('/save_snippets', methods=['POST'])
def save_snippets():
    try:
        with open('code_snippets.json', 'w') as f:
            json.dump(code_snippets_cache, f)
        return jsonify({"message": "Code snippets saved successfully"}), 200
    except Exception as e:
        logger.error(f"Error saving code snippets: {str(e)}")
        return jsonify({"error": "Failed to save code snippets"}), 500

@app.route('/load_snippets', methods=['GET'])
def load_snippets():
    try:
        if os.path.exists('code_snippets.json'):
            with open('code_snippets.json', 'r') as f:
                global code_snippets_cache
                code_snippets_cache = json.load(f)
            return jsonify({"message": "Code snippets loaded successfully"}), 200
        else:
            return jsonify({"message": "No saved code snippets found"}), 404
    except Exception as e:
        logger.error(f"Error loading code snippets: {str(e)}")
        return jsonify({"error": "Failed to load code snippets"}), 500

if __name__ == '__main__':
    app.run(debug=True)