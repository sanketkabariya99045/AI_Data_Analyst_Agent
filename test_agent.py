from backend.agents.agent_manager import agent_manager

result = agent_manager.process(
    question="How many spam and ham messages are there?"
)

print(result)