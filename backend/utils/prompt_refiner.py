def refine_prompt_for_code(task_description: str, context: str) -> str:
    """
    Enhances the user's task description by integrating additional context,
    ensuring the AI understands the requirements, even if the user is not
    experienced with coding.

    Args:
        task_description (str): The user's description of the task they want to accomplish.
        context (str): Extra information about the project or environment that helps the AI
                       generate more accurate and relevant code.

    Returns:
        str: A refined and comprehensive prompt for the AI, designed to produce the best
             possible code based on the provided inputs.
    """
    # Combine the task description with context, formatted for clarity and best AI performance
    refined_prompt = (
        f"You are an experienced developer tasked with generating code.\n\n"
        f"Project Context: {context}\n"
        f"Task Description: {task_description}\n\n"
        f"Please generate code that accomplishes the task above, ensuring it is well-documented, "
        f"follows best practices, and is easy to understand for developers at all skill levels."
    )
    
    return refined_prompt
