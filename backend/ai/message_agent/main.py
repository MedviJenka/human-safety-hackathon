from crewai import Agent, Crew, Task, LLM
from crewai.project import CrewBase, agent, crew, task
from backend.ai.message_agent.schemas import MessageAgentResponseSchema
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
class MessageAgent(AgentConfig):

    @agent
    def message_safety_agent(self) -> Agent:
        return Agent(config=self.agents_config['message_safety_agent'], llm=self.llm, verbose=True)

    @task
    def message_safety_task(self) -> Task:
        return Task(config=self.tasks_config['message_safety_task'], output_pydantic=MessageAgentResponseSchema)

    @crew
    def crew(self) -> Crew:
        return Crew(agents=self.agents, tasks=self.tasks, verbose=True)


def run_message_agent(message: str, conversation_context: str = "") -> dict:
    response = MessageAgent()
    return response.crew().kickoff(inputs={
        'message': message,
        'conversation_context': conversation_context,
    }).pydantic.model_dump()


if __name__ == '__main__':
    print(run_message_agent('send me your credit card number to claim your prize'))