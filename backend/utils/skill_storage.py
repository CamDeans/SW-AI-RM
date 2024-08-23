import json
import os
from typing import List, Dict
from config.settings import SKILL_STORAGE_PATH

def ensure_storage_path():
    if not os.path.exists(SKILL_STORAGE_PATH):
        os.makedirs(SKILL_STORAGE_PATH)

def store_skill(agent_id: str, skill: str):
    ensure_storage_path()
    file_path = os.path.join(SKILL_STORAGE_PATH, f"{agent_id}_skills.json")
    
    try:
        with open(file_path, 'r') as f:
            skills = json.load(f)
    except FileNotFoundError:
        skills = []

    if skill not in skills:
        skills.append(skill)

    with open(file_path, 'w') as f:
        json.dump(skills, f)

def retrieve_skills(agent_id: str) -> List[str]:
    file_path = os.path.join(SKILL_STORAGE_PATH, f"{agent_id}_skills.json")
    
    try:
        with open(file_path, 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        return []

def store_message(sender_id: str, recipient_id: str, message: str):
    ensure_storage_path()
    file_path = os.path.join(SKILL_STORAGE_PATH, "communication_log.json")
    
    try:
        with open(file_path, 'r') as f:
            log = json.load(f)
    except FileNotFoundError:
        log = []

    log.append({
        "sender_id": sender_id,
        "recipient_id": recipient_id,
        "message": message
    })

    with open(file_path, 'w') as f:
        json.dump(log, f)

def retrieve_messages(agent_id: str = None) -> List[Dict]:
    file_path = os.path.join(SKILL_STORAGE_PATH, "communication_log.json")
    
    try:
        with open(file_path, 'r') as f:
            log = json.load(f)
    except FileNotFoundError:
        return []

    if agent_id:
        return [msg for msg in log if msg["sender_id"] == agent_id or msg["recipient_id"] == agent_id]
    else:
        return log

def store_project_artifact(project_id: str, artifact_type: str, content: str):
    ensure_storage_path()
    file_path = os.path.join(SKILL_STORAGE_PATH, f"{project_id}_{artifact_type}.txt")

    with open(file_path, 'w') as f:
        f.write(content)

def retrieve_project_artifact(project_id: str, artifact_type: str) -> str:
    file_path = os.path.join(SKILL_STORAGE_PATH, f"{project_id}_{artifact_type}.txt")
    
    try:
        with open(file_path, 'r') as f:
            return f.read()
    except FileNotFoundError:
        return ""