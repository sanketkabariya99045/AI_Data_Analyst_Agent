from backend.agents.planner_agent import planner_agent
from backend.agents.sql_agent import sql_agent

plan = planner_agent.analyze(
    "How many rows are in the dataset?"
)

sql_result = sql_agent.generate_sql(
    plan=plan
)

print(sql_result)