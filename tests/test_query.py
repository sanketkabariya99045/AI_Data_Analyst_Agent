from backend.database.query_executor import query_executor

result = query_executor.execute(
    "SELECT * FROM sheet1 LIMIT 5"
)

print(result)