import sqlite3

database = sqlite3.connect('../database.db')
cursor = database.cursor()

# cursor.execute(f"ALTER TABLE users ADD selected_category TEXT")

cursor.execute(f'ALTER TABLE users ADD selected_category TEXT DEFAULT "category_random"')

database.commit()
