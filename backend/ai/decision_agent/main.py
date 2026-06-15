from backend.ai.decision_agent.crew import run_decision_agent

if __name__ == '__main__':
    result = run_decision_agent(
        message="Hey, send me a photo of yourself. Don't tell your mom okay?",
        conversation_context="Stranger initiated contact 3 days ago, has been asking personal questions",
        danger_type="GROOMING",
        user_context="12 year old child"
    )
    print(result)
