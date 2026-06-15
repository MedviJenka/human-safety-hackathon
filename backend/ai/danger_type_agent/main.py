from backend.ai.danger_type_agent.crew import run_danger_type_agent

if __name__ == '__main__':
    result = run_danger_type_agent(
        message="Hey, send me a photo of yourself. Don't tell your mom okay?",
        conversation_context="Stranger initiated contact 3 days ago, has been asking personal questions"
    )
    print(result)
