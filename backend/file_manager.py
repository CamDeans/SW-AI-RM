import os

def create_file(file_path: str, content: str):
    os.makedirs(os.path.dirname(file_path), exist_ok=True)
    with open(file_path, 'w') as file:
        file.write(content)

def process_generated_code(project_id: str, code_map: dict):
    base_dir = f"generated_code/project_{project_id}"
    for file_name, file_content in code_map.items():
        file_path = os.path.join(base_dir, file_name)
        create_file(file_path, file_content)


# Function to create the necessary project structure based on a given hierarchy
def create_project_structure(base_path, structure):
    for folder in structure:
        os.makedirs(os.path.join(base_path, folder), exist_ok=True)


# Function to create the necessary project structure based on a given hierarchy
def create_project_structure(base_path, structure):
    for folder in structure:
        os.makedirs(os.path.join(base_path, folder), exist_ok=True)

def save_code_to_file(base_path, relative_path, code):
    full_path = os.path.join(base_path, relative_path)
    os.makedirs(os.path.dirname(full_path), exist_ok=True)
    with open(full_path, 'w') as f:
        f.write(code)
