import logging
from typing import List, Dict
from backend.core.specialized_agent import SpecializedAgent
from backend.utils.communication import send_message
from backend.utils.skill_storage import store_skill, retrieve_skills
from backend.integrations.anthropic_ai import generate_code, analyze_task, analyze_project_requirements

logger = logging.getLogger(__name__)

class LeadDeveloper:
    def __init__(self):
        self.agents: Dict[str, SpecializedAgent] = {}
        self.project_tasks: List[Dict] = []

    def analyze_project(self, requirements: Dict):
        self.project_tasks = []
        for tech, details in requirements.items():
            for task in details['tasks']:
                self.project_tasks.append({
                    'description': task,
                    'technology': tech,
                    'status': 'pending'
                })
            if tech not in self.agents:
                # Adjusted to include the specialty argument
                self.agents[tech] = SpecializedAgent(tech, f"{tech} Specialist", tech)
        
        self._assign_tasks()
    
    def _assign_tasks(self):
        for task in self.project_tasks:
            agent = self.agents.get(task['technology'])
            if agent:
                agent.assign_task(task)

    def create_required_agents(self, requirements: Dict):
        for tech, details in requirements.items():
            if not self.get_agent_by_skill(tech):
                # Adjusted to include the specialty argument
                new_agent = SpecializedAgent(tech, f"{tech.capitalize()} Specialist", tech)
                self.agents[tech] = new_agent
                logger.info(f"Created new agent: {new_agent.name}")

    def break_down_tasks(self, requirements: Dict):
        for tech, details in requirements.items():
            for task in details['tasks']:
                self.project_tasks.append({
                    'description': task,
                    'technology': tech,
                    'status': 'pending'
                })
        logger.debug(f"Project tasks: {self.project_tasks}")

    def get_agent_by_skill(self, skill: str) -> SpecializedAgent:
        return next((agent for agent in self.agents.values() if agent.has_skill(skill)), None)

    def monitor_progress(self):
        for agent in self.agents.values():
            status = agent.get_current_task_status()
            if status['status'] == 'completed':
                self.review_task(agent, status['task'])

    def review_task(self, agent: SpecializedAgent, task: Dict):
        review_result = analyze_task(task['code'], task)
        if review_result['approved']:
            logger.info(f"Task '{task['description']}' completed successfully by {agent.name}")
            task['status'] = 'completed'
        else:
            logger.info(f"Task '{task['description']}' needs revision. Feedback: {review_result['feedback']}")
            agent.assign_task(task)  # Reassign for revision

    def add_agent(self, agent: SpecializedAgent):
        self.agents[agent.specialty] = agent

    def remove_agent(self, agent_id: str):
        self.agents = {skill: agent for skill, agent in self.agents.items() if agent.id != agent_id}

    def get_swarm_status(self) -> Dict:
        return {
            'agents': [agent.get_status() for agent in self.agents.values()],
            'pending_tasks': len([task for task in self.project_tasks if task['status'] == 'pending']),
            'in_progress_tasks': len([task for task in self.project_tasks if task['status'] == 'in_progress']),
            'completed_tasks': len([task for task in self.project_tasks if task['status'] == 'completed'])
        }

    def generate_project_artifact(self, artifact_type: str, project_data: Dict) -> str:
        return generate_code(artifact_type, project_data)

    def get_all_tasks(self) -> List[Dict]:
        return self.project_tasks
    
    def get_all_agents(self) -> List[SpecializedAgent]:
        return list(self.agents.values())
