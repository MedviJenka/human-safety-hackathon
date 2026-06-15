from crewai.flow.flow import Flow, listen, start, router
from pydantic import BaseModel, Field
from backend.ai.message_agent.main import run_message_agent
from backend.ai.danger_type_agent.crew import run_danger_type_agent
from backend.ai.decision_agent.crew import run_decision_agent


CONFIDENCE_THRESHOLD = 80.0
MAX_RESCAN_ATTEMPTS = 2


class SafetyFlowState(BaseModel):
    message: str = ""
    conversation_context: str = ""
    user_context: str = ""
    is_safe: bool = True
    confidence_level: float = 100.0
    danger_type: str = ""
    safety_report: dict = Field(default_factory=dict)


class SafetyFlow(Flow[SafetyFlowState]):

    @start()
    def validate_message(self):
        result = run_message_agent(self.state.message, self.state.conversation_context)
        self.state.is_safe = result['is_safe']
        self.state.confidence_level = result['confidence_level']

        # rescan if flagged but confidence is low — avoids false positives
        attempts = 1
        while (
            not self.state.is_safe
            and self.state.confidence_level < CONFIDENCE_THRESHOLD
            and attempts < MAX_RESCAN_ATTEMPTS
        ):
            result = run_message_agent(self.state.message, self.state.conversation_context)
            self.state.is_safe = result['is_safe']
            self.state.confidence_level = result['confidence_level']
            attempts += 1

        return result

    @router(validate_message)
    def route_after_validation(self):
        if self.state.is_safe:
            return "safe"
        return "classify_danger"

    @listen("classify_danger")
    def classify_danger(self):
        result = run_danger_type_agent(
            message=self.state.message,
            conversation_context=self.state.conversation_context,
        )
        self.state.danger_type = result['danger_type']
        return result

    @listen(classify_danger)
    def generate_report(self):
        result = run_decision_agent(
            message=self.state.message,
            conversation_context=self.state.conversation_context,
            danger_type=self.state.danger_type,
            user_context=self.state.user_context,
        )
        self.state.safety_report = result
        return result

    @listen("safe")
    def handle_safe(self):
        return {"status": "safe"}


def analyze_message(
    message: str,
    conversation_context: str = "",
    user_context: str = "",
) -> dict:
    flow = SafetyFlow()
    flow.state.message = message
    flow.state.conversation_context = conversation_context
    flow.state.user_context = user_context
    flow.kickoff()

    if flow.state.is_safe:
        return {"status": "safe"}
    return flow.state.safety_report


if __name__ == '__main__':
    report = analyze_message(
        message="Hey sweetheart, send me a photo. Don't tell your parents we're talking.",
        conversation_context="Unknown adult contacted the user 2 days ago via the platform.",
        user_context="13 year old girl",
    )
    print(report)
