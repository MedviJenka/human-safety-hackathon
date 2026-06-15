from crewai import Agent, Crew, Task, LLM
from crewai.project import CrewBase, agent, crew, task
from backend.ai.decision_agent.schemas import SafetyReportSchema
from backend.settings import Config
from functools import cached_property
from dataclasses import dataclass


@dataclass
class AgentConfig:
    agents: list[Agent] = None
    tasks: list[Task] = None
    agents_config: dict = "config/agents.yaml"
    tasks_config: dict = "config/tasks.yaml"
    temperature: float = 0.0

    @cached_property
    def llm(self) -> LLM:
        return LLM(model='gpt-4o', api_key=Config.OPENAI_API_KEY, temperature=self.temperature)


@CrewBase
class DecisionAgent(AgentConfig):

    @agent
    def safety_response_agent(self) -> Agent:
        return Agent(config=self.agents_config['safety_response_agent'], llm=self.llm, verbose=True)

    @task
    def generate_safety_report_task(self) -> Task:
        return Task(config=self.tasks_config['generate_safety_report_task'], output_pydantic=SafetyReportSchema)

    @crew
    def crew(self) -> Crew:
        return Crew(agents=self.agents, tasks=self.tasks, verbose=True)


def run_decision_agent(
    message: str,
    conversation_context: str,
    danger_type: str,
    user_context: str = "",
) -> dict:
    response = DecisionAgent()
    return response.crew().kickoff(inputs={
        'message': message,
        'conversation_context': conversation_context,
        'danger_type': danger_type,
        'user_context': user_context,
    }).pydantic.model_dump()
