from backend.database.database import database_manager

print("Tables in database:")
print(database_manager.list_tables())