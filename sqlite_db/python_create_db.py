import sqlite3

# Connect to SQLite database (creates a new database if it doesn't exist)
conn = sqlite3.connect('foodReactions.db')
cursor = conn.cursor()

# Create FoodReactions table
cursor.execute('''
    CREATE TABLE IF NOT EXISTS FoodReactions (
        ReportNumber VARCHAR(25) NOT NULL,
        DateCreated DATE NOT NULL,
        DateStarted DATE,
        PRIMARY KEY (ReportNumber)
    );
''')

# Create Reactions table with foreign key constraint
cursor.execute('''
    CREATE TABLE IF NOT EXISTS Reactions (
        ReportNumber VARCHAR(25) NOT NULL,
        Reactions VARCHAR(500) NOT NULL,        
        FOREIGN KEY (ReportNumber) REFERENCES FoodReactions (ReportNumber)
    );
''')

# Create Consumer table with foreign key constraint
cursor.execute('''
    CREATE TABLE IF NOT EXISTS Consumer (
        ReportNumber VARCHAR(25) NOT NULL,
        Age INTEGER,
        AgeUnit VARCHAR(20), 
        Gender VARCHAR(20),        
        FOREIGN KEY (ReportNumber) REFERENCES FoodReactions (ReportNumber)
    );
''')

# Create Products table with foreign key constraint
cursor.execute('''
    CREATE TABLE IF NOT EXISTS Products (
        ReportNumber VARCHAR(25) NOT NULL,
        Role VARCHAR(50) NOT NULL,
        NameBrand VARCHAR(255) NOT NULL,
        IndustryCode INTEGER NOT NULL,
        IndusteryName VARCHAR(255) NOT NULL,        
        FOREIGN KEY (ReportNumber) REFERENCES FoodReactions (ReportNumber)
    );
''')

# Create Outcomes table with foreign key constraint
cursor.execute('''
    CREATE TABLE IF NOT EXISTS Outcomes (
        ReportNumber VARCHAR(25) NOT NULL,
        Outcome VARCHAR(150) NOT NULL,        
        FOREIGN KEY (ReportNumber) REFERENCES FoodReactions (ReportNumber)
    );
''')

# Commit changes and close the connection
conn.commit()
conn.close()
print("executed successfully")