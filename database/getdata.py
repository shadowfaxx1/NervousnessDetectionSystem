import sqlite3

# Function to connect to the database
def connect_db():
    conn = sqlite3.connect('nervousness_data.db')
    return conn

# Function to fetch all records
def fetch_all_records():
    conn = connect_db()
    c = conn.cursor()
    c.execute('SELECT * FROM Nervousness')
    rows = c.fetchall()
    conn.close()
    return rows

# Function to fetch records by name
def fetch_records_by_name(name):
    conn = connect_db()
    c = conn.cursor()
    c.execute('SELECT * FROM Nervousness WHERE name = ?', (name,))
    rows = c.fetchall()
    conn.close()
    return rows

# Function to delete records by name
def delete_records_by_name(name):
    conn = connect_db()
    c = conn.cursor()
    c.execute('DELETE FROM Nervousness WHERE name = ?', (name,))
    conn.commit()
    conn.close()

# Function to update records by name
def update_records_by_name(name, weak, strong, neutral):
    conn = connect_db()
    c = conn.cursor()
    c.execute('''UPDATE Nervousness 
                 SET weak = ?, strong = ?, neutral = ?
                 WHERE name = ?''', (weak, strong, neutral, name))
    conn.commit()
    conn.close()

# Example usage
if __name__ == '__main__':
    print("All Records:")
    records = fetch_all_records()
    for record in records:
        print(record)

    print("\nRecords for John Doe:")
    records = fetch_records_by_name("John Doe")
    for record in records:
        print(record)
    
    print("\nUpdating records for John Doe...")
    update_records_by_name("John Doe", 10, 20, 30)
    
    print("\nRecords for John Doe after update:")
    records = fetch_records_by_name("John Doe")
    for record in records:
        print(record)
    
    print("\nDeleting records for John Doe...")
    delete_records_by_name("kaif")
    
    print("\nRecords for John Doe after deletion:")
    records = fetch_records_by_name("John Doe")
    for record in records:
        print(record)
