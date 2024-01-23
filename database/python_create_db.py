import sqlite3

# Connect to SQLite database (or create if not exists)
conn = sqlite3.connect('foodReaction.db')
cursor = conn.cursor()
 
# Create ReactionsTypes table
cursor.execute('''
CREATE TABLE IF NOT EXISTS ReactionsTypes (
    ID INTEGER PRIMARY KEY AUTOINCREMENT,
    ReactionTypeName VARCHAR(150) NOT NULL
    
)
''')

# Create Reactions table
cursor.execute('''
CREATE TABLE IF NOT EXISTS Reactions (
    ID INTEGER PRIMARY KEY AUTOINCREMENT,
    ReactionTypeID INTEGER NOT NULL,
    FoodReactionID INTEGER NOT NULL,
    
    FOREIGN KEY (ReactionTypeID) REFERENCES ReactionsTypes (ID),
    FOREIGN KEY (FoodReactionID) REFERENCES FoodReactions (ID)
)
''')

# Create OutcomesTypes table
cursor.execute('''
CREATE TABLE IF NOT EXISTS OutcomesTypes (
    ID INTEGER PRIMARY KEY AUTOINCREMENT,
    OutcomeTypeName VARCHAR(150) NOT NULL
    
)
''')

# Create Outcomes table
cursor.execute('''
CREATE TABLE IF NOT EXISTS Outcomes (
    ID INTEGER PRIMARY KEY AUTOINCREMENT,
    OutcomesTypeID INTEGER NOT NULL,
    FoodReactionID INTEGER NOT NULL,
    FOREIGN KEY (OutcomesTypeID) REFERENCES OutcomesTypes (ID),
    FOREIGN KEY (FoodReactionID) REFERENCES FoodReactions (ID)
)
''')

# Create Products table
cursor.execute('''
CREATE TABLE IF NOT EXISTS Products (
    ID INTEGER PRIMARY KEY AUTOINCREMENT,
    IndustryNameID INTEGER NOT NULL,
    BrandID INTEGER NOT NULL,
    RoleID INTEGER NOT NULL,
    FoodReactionID INTEGER NOT NULL,
    FOREIGN KEY (IndustryNameID) REFERENCES IndustryNames (ID),
    FOREIGN KEY (BrandID) REFERENCES Brands (ID),
    FOREIGN KEY (RoleID) REFERENCES Roles (ID),
    FOREIGN KEY (FoodReactionID) REFERENCES FoodReactions (ID)
)
''')

# Create FoodReactions table
cursor.execute('''
CREATE TABLE IF NOT EXISTS FoodReactions (
    ID INTEGER PRIMARY KEY AUTOINCREMENT,
    ReportNumber VARCHAR(25) NOT NULL,
    DateCreated VARCHAR(20)  ,
    DateStarted VARCHAR(20)  ,
    consumerID INTEGER  ,
    FOREIGN KEY (consumerID) REFERENCES Consumers (ID)
)
''')

# Create Consumers table
cursor.execute('''
CREATE TABLE IF NOT EXISTS Consumers (
    ID INTEGER PRIMARY KEY AUTOINCREMENT,
    Age INTEGER  ,
    AgeUnit VARCHAR(20)  ,
    Gender VARCHAR(10) 
)
''')

# Create IndustryNames table
cursor.execute('''
CREATE TABLE IF NOT EXISTS IndustryNames (
    ID INTEGER PRIMARY KEY AUTOINCREMENT,
    IndustryCode INTEGER NOT NULL,
    IndustryName VARCHAR(100) NOT NULL
)
''')

# Create Brands table
cursor.execute('''
CREATE TABLE IF NOT EXISTS Brands (
    ID INTEGER PRIMARY KEY AUTOINCREMENT,
    BrandName VARCHAR(150) NOT NULL
)
''')

# Create Roles table
cursor.execute('''
CREATE TABLE IF NOT EXISTS Roles (
    ID INTEGER PRIMARY KEY AUTOINCREMENT,
    RoleName VARCHAR(100) NOT NULL
)
''')

# Commit changes and close connection
conn.commit()
conn.close()

print("SQLite database and tables created successfully.")


