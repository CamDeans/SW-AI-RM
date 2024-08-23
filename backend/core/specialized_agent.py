import uuid
from typing import List, Dict
from backend.integrations.anthropic_ai import generate_code
from backend.utils.skill_storage import store_skill, retrieve_skills

class SpecializedAgent:
    def __init__(self, specialty: str, name: str, primary_skill: str):
        self.specialty = specialty
        self.tasks = []
        self.id = str(uuid.uuid4())
        self.name = name
        self.primary_skill = primary_skill
        self.skills = set([primary_skill])
        self.current_task = None
        self.task_history = []

    def assign_task(self, task):
        self.tasks.append(task)

    def complete_task(self):
        if self.current_task:
            self.task_history.append(self.current_task)
            self.current_task = None

    def add_skill(self, skill: str):
        self.skills.add(skill)
        store_skill(self.id, skill)

    def has_skill(self, skill: str) -> bool:
        return skill in self.skills

    def get_skills(self) -> List[str]:
        return list(self.skills)

    def evaluate_task_fit(self, task: Dict) -> float:
        required_skills = set(task.get('required_skills', []))
        agent_skills = set(self.skills)
        skill_match = len(required_skills.intersection(agent_skills))
        return skill_match / len(required_skills) if required_skills else 0

    def work_on_task(self) -> Dict:
        if not self.current_task:
            return {'status': 'no_task'}

        try:
            code = generate_code(self.current_task['description'], self.current_task['requirements'])
            self.current_task['code'] = code
            self.current_task['status'] = 'completed'
            return {'status': 'completed', 'code': code, 'task': self.current_task}
        except Exception as e:
            self.current_task['status'] = 'stuck'
            return {'status': 'stuck', 'error': str(e), 'task': self.current_task}

    def get_current_task_status(self) -> Dict:
        if not self.current_task:
            return {'status': 'no_task'}
        return {'status': self.current_task['status'], 'task': self.current_task}

    def is_available(self) -> bool:
        return self.current_task is None

    def get_status(self) -> Dict:
        return {
            'id': self.id,
            'name': self.name,
            'primary_skill': self.primary_skill,
            'skills': list(self.skills),
            'current_task': self.current_task,
            'task_history_length': len(self.task_history)
        }

    def load_skills(self):
        stored_skills = retrieve_skills(self.id)
        self.skills.update(stored_skills)

    def to_dict(self):
        return {
            "name": self.name,
            "specialty": self.specialty,
            "tasks": self.tasks
        }
