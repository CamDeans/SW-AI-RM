import uuid
import random
import logging
import threading
import time
from .swarm_structure import SwarmStructure  # Assuming you have this class implemented

logger = logging.getLogger(__name__)

class TaskManager:
    def __init__(self):
        self.tasks = []
        self.lock = threading.Lock()
        self.all_tasks_completed = threading.Event()
        self.swarm = SwarmStructure()  # Initialize the swarm structure
        self.stop_flag = threading.Event()

    def create_task(self, description, technology, priority=1):
        with self.lock:
            task = {
                'id': str(uuid.uuid4()),
                'description': description,
                'technology': technology,
                'priority': priority,
                'status': 'pending',
                'assigned_to': None,
                'assigned_time': None,
                'progress': 0
            }
            self.tasks.append(task)
            logger.info(f"Created task: {task['description']}")
            return task['id']

    def get_task(self, task_id):
        with self.lock:
            return next((task for task in self.tasks if task['id'] == task_id), None)

    def update_task_status(self, task_id, new_status):
        with self.lock:
            task = self.get_task(task_id)
            if task:
                task['status'] = new_status
                logger.info(f"Task {task_id} ('{task['description']}') status updated to {new_status}")

    def get_tasks_by_status(self, status):
        with self.lock:
            return [task for task in self.tasks if task['status'] == status]

    def get_all_tasks(self):
        with self.lock:
            return self.tasks

    def assign_task_to_agent(self, task_id):
        with self.lock:
            task = self.get_task(task_id)
            if task and task['assigned_to'] is None:
                agent = self.swarm.get_available_agent()
                if agent:
                    task['assigned_to'] = agent.id
                    task['assigned_time'] = time.time()
                    agent.assign_task(task_id)
                    logger.info(f"Task {task_id} assigned to agent {agent.id}")

    def unassign_task_from_agent(self, task_id):
        with self.lock:
            task = self.get_task(task_id)
            if task and task['assigned_to']:
                agent = self.swarm.get_agent_by_id(task['assigned_to'])
                if agent:
                    agent.unassign_task()
                task['assigned_to'] = None
                task['assigned_time'] = None
                logger.info(f"Task {task_id} unassigned from agent")

    def check_task_progress(self, task_id):
        task = self.get_task(task_id)
        if task:
            # Simulate progress for demonstration purposes
            # In a real scenario, you'd implement actual progress checking logic
            progress = min(task['progress'] + 10, 100)  # Increment by 10%, max 100%
            task['progress'] = progress
            return progress
        return 0

    def check_task_timeout(self, task):
        timeout = 300  # 5 minutes timeout
        if task['status'] == 'in_progress' and task['assigned_time'] and time.time() - task['assigned_time'] > timeout:
            logger.warning(f"Task {task['id']} timed out. Resetting to pending.")
            task['status'] = 'pending'
            task['progress'] = 0
            self.unassign_task_from_agent(task['id'])

    def process_tasks(self):
        with self.lock:
            pending_tasks = [task for task in self.tasks if task['status'] == 'pending']
            in_progress_tasks = [task for task in self.tasks if task['status'] == 'in_progress']
            
            if not pending_tasks and not in_progress_tasks:
                logger.info("All tasks completed.")
                self.all_tasks_completed.set()
                return True

            for task in in_progress_tasks:
                self.check_task_timeout(task)
                progress = self.check_task_progress(task['id'])
                if progress >= 100:
                    task['status'] = 'completed'
                    self.unassign_task_from_agent(task['id'])
                    logger.info(f"Task completed: {task['description']}")

            if pending_tasks:
                task = pending_tasks[0]
                self.assign_task_to_agent(task['id'])
                if task['assigned_to']:
                    task['status'] = 'in_progress'
                    logger.info(f"Started processing task: {task['description']}")

        return False

    def run_task_loop(self):
        self.stop_flag.clear()
        self.all_tasks_completed.clear()
        processing_thread = threading.Thread(target=self.process_tasks_loop)
        processing_thread.start()

    def process_tasks_loop(self):
        while not self.stop_flag.is_set():
            all_completed = self.process_tasks()
            if all_completed:
                break
            time.sleep(1)  # Small delay to prevent tight loop

    def stop_task_loop(self):
        self.stop_flag.set()

    def wait_for_all_tasks_completed(self, timeout=None):
        return self.all_tasks_completed.wait(timeout)

    def reset_tasks(self):
        with self.lock:
            self.tasks = []
            self.all_tasks_completed.clear()

    def get_progress(self):
        with self.lock:
            total_tasks = len(self.tasks)
            completed_tasks = len([task for task in self.tasks if task['status'] == 'completed'])
            in_progress_tasks = len([task for task in self.tasks if task['status'] == 'in_progress'])
            return {
                'total': total_tasks,
                'completed': completed_tasks,
                'in_progress': in_progress_tasks,
                'pending': total_tasks - completed_tasks - in_progress_tasks
            }

    def generate_code_snippets(self, task_description):
        # This is a placeholder. In a real scenario, you'd call your AI service here.
        logger.info(f"Generating code snippets for task: {task_description}")
        return f"// Code snippet for {task_description}\n// Implement your logic here"

# Usage example removed as it's now in app.py