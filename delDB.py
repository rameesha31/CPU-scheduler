import sqlite3

# Connect to the SQLite database
conn = sqlite3.connect('file_paths.db')
c = conn.cursor()

# Execute SQL query to delete all records from the table
c.execute("DELETE FROM file_path")

# Execute SQL query to select all records from the table
c.execute("SELECT * FROM file_path")
result = c.fetchall()

# Print the result
for row in result:
    print(row)
conn.commit()  # Commit the transaction to save the changes

# Close the connection to the database
conn.close()

print("Table 1 cleared successfully.")

# Connect to the SQLite database
conn = sqlite3.connect('scheduling_algorithms.db')
c = conn.cursor()

# Execute SQL query to delete all records from the table
c.execute("DELETE FROM algo_performance")

# Execute SQL query to select all records from the table
c.execute("SELECT * FROM algo_performance")
result = c.fetchall()

# Print the result
for row in result:
    print(row)
conn.commit()  # Commit the transaction to save the changes

# Close the connection to the database
conn.close()

print("Table 2 cleared successfully.")
