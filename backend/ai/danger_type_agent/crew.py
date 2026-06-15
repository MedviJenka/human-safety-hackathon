from crewai import Agent, Crew, Task, LLM
from crewai.project import CrewBase, agent, crew, task
from backend.ai.danger_type_agent.schemas import DangerTypeResponseSchema
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
class DangerTypeAgent(AgentConfig):

    @agent
    def danger_classifier_agent(self) -> Agent:
        return Agent(config=self.agents_config['danger_classifier_agent'], llm=self.llm, verbose=True)

    @task
    def classify_danger_task(self) -> Task:
        return Task(config=self.tasks_config['classify_danger_task'], output_pydantic=DangerTypeResponseSchema)

    @crew
    def crew(self) -> Crew:
        return Crew(agents=self.agents, tasks=self.tasks, verbose=True)


def run_danger_type_agent(message: str, conversation_context: str = "") -> dict:
    response = DangerTypeAgent()
    return response.crew().kickoff(inputs={
        'message': message,
        'conversation_context': conversation_context,
    }).pydantic.model_dump()
