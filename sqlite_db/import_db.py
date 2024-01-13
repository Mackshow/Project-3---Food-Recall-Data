import sqlite3
import json

def create_connection():
    # Connect to SQLite database
    conn = sqlite3.connect('foodReactions.db')
    return conn

def insert_data(conn, data):
    cursor = conn.cursor()

    # Insert data into FoodReactions table
    cursor.execute('''
        INSERT INTO FoodReactions (ReportNumber, DateCreated, DateStarted)
        VALUES (?, ?, ?)
    ''', (data['report_number'], data['date_created'], data['date_started']))

    report_number = data['report_number']

    # Insert data into Reactions table
    for reaction in data['reactions']:
        cursor.execute('''
            INSERT INTO Reactions (ReportNumber, reactions)
            VALUES (?, ?)
        ''', (report_number, reaction))

    # Insert data into Consumer table
    consumer_data = data['consumer']
    cursor.execute('''
        INSERT INTO Consumer (ReportNumber, Age, AgeUnit, Gender)
        VALUES (?, ?, ?, ?)
    ''', (report_number, consumer_data.get('age',''), consumer_data.get('age_unit',''), consumer_data.get('gender','')))

    # Insert data into Products table
    for product in data['products']:
        cursor.execute('''
            INSERT INTO Products (ReportNumber, Role, NameBrand, IndustryCode, IndusteryName)
            VALUES (?, ?, ?, ?, ?)
        ''', (report_number, product['role'], product['name_brand'], product['industry_code'], product['industry_name']))

    # Insert data into Outcomes table
    for outcome in data['outcomes']:
        cursor.execute('''
            INSERT INTO Outcomes (ReportNumber, outcome)
            VALUES (?, ?)
        ''', (report_number, outcome))

    # Commit changes
    conn.commit()

def main():
    # Read JSON file
    with open('Project-3---Food-Recall-Data/food-event-0001-of-0001.json', 'r') as file:
        json_data = json.load(file)

    # Create database connection
    conn = create_connection()
    for data in json_data['results']:            
        # Insert data into tables
        insert_data(conn, data)

    # Close connection
    conn.close()

if __name__ == '__main__':
    main()
