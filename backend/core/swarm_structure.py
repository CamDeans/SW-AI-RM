from typing import List, Dict
from backend.core.lead_developer import LeadDeveloper
from backend.core.specialized_agent import SpecializedAgent

class SwarmStructure:
    def __init__(self):
        self.lead_developer = LeadDeveloper()
        self.agents: List[SpecializedAgent] = []

    def add_agent(self, name: str, primary_skill: str) -> SpecializedAgent:
        agent = SpecializedAgent(name, primary_skill)
        self.agents.append(agent)
        self.lead_developer.add_agent(agent)
        return agent

    def remove_agent(self, agent_id: str):
        self.agents = [agent for agent in self.agents if agent.id != agent_id]
        self.lead_developer.remove_agent(agent_id)

    def get_agent(self, agent_id: str) -> SpecializedAgent:
        return next((agent for agent in self.agents if agent.id == agent_id), None)

    def get_all_agents(self):
        return self.lead_developer.get_all_agents()

    def assign_task(self, task: Dict):
        self.lead_developer.assign_task(task)

    def get_swarm_status(self) -> Dict:
        return self.lead_developer.get_swarm_status()

    def coordinate_swarm(self):
        self.lead_developer.coordinate_swarm()

    def get_swarm_structure(self) -> Dict:
        return {
            'lead_developer': {
                'id': self.lead_developer.id,
                'name': self.lead_developer.name
            },
            'agents': [
                {
                    'id': agent.id,
                    'name': agent.name,
                    'primary_skill': agent.primary_skill,
                    'skills': list(agent.skills)
                }
                for agent in self.agents
            ]
        }

    def get_agent_network(self) -> List[Dict]:
        network = []
        for agent in self.agents:
            connections = [
                {
                    'id': other_agent.id,
                    'strength': len(set(agent.skills) & set(other_agent.skills)) / len(set(agent.skills) | set(other_agent.skills))
                }
                for other_agent in self.agents if other_agent != agent
            ]
            network.append({
                'id': agent.id,
                'connections': connections
            })
        return network
    
    def create_agent(self, specialty):
        agent = SpecializedAgent(specialty, specialty)  # Using specialty as both name and primary skill
        self.agents.append(agent)
        return agent