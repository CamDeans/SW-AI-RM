def refine_prompt_for_code(task_description: str, context: str) -> str:
    refined_prompt = f"Context: {context}\nTask: {task_description}\n\nPlease generate code that accomplishes the task above."
    return refined_prompt
