import sqlite3
import json
from datetime import datetime
# Connect to SQLite database
conn = sqlite3.connect('foodReaction.db')
cursor = conn.cursor()

# Load JSON data from a file 
with open('food-event-0001-of-0001.json', 'r') as json_file:
    data = json.load(json_file)
 
default_consumer={"consumer": {"age": "0","age_unit": "-", "gender": "-" }} #set default value for each age, age_unit, and gender instead null
# Loop through each record in the JSON data
for record in data['results']:
    print('record:', record)
    # Insert into Consumers table
    consumer_id = None
    if record.get('consumer', default_consumer ):
        cursor.execute(f'SELECT ID FROM Consumers WHERE Age =? and AgeUnit=? and Gender = ?',
                        (record['consumer'].get('age',''), record['consumer'].get('age_unit',''), record['consumer'].get('gender',''),)) #set default value empty space instead of null
        result = cursor.fetchone()
        if result:
            print('consumer active selection : ', result) #debugging
            consumer_id= result[0]
        else:  
            print('consumer insertion:>>') #debugging
            cursor.execute('''
                INSERT INTO Consumers (Age, AgeUnit, Gender) VALUES (?, ?, ?)
            ''', (record['consumer'].get('age',0), record['consumer'].get('age_unit','-'), record['consumer'].get('gender','-')))
            conn.commit()
            consumer_id = cursor.lastrowid
            
    #debugging
    print('--> age:',record['consumer'].get('age',0), ', unit:',record['consumer'].get('age_unit','-'), ', gender:',record['consumer'].get('gender','-'), ',id:',consumer_id)
    print('--->report number: ',record.get('report_number','-'), record.get('date_created',''), record.get('date_started',''), consumer_id)

    # Insert into FoodReactions table
    cursor.execute('''
        INSERT INTO FoodReactions (ReportNumber, DateCreated, DateStarted, ConsumerID) VALUES (?, ?, ?, ?)
    ''', (record['report_number'], record['date_created'], record['date_started'], consumer_id))
    conn.commit()
    food_reaction_id = cursor.lastrowid
    print('---->food_reaction_id:',food_reaction_id) #debbuging
    


    
    # Insert into Reactions and ReactionsTypes tables
    for reaction in record['reactions']:
        # Check if the reaction type already exists
        cursor.execute('SELECT ID FROM ReactionsTypes WHERE ReactionTypeName = ?', (reaction,))
        reaction_type_id = cursor.fetchone()
        if not reaction_type_id:
            cursor.execute('INSERT INTO ReactionsTypes (ReactionTypeName) VALUES (?)', (reaction,))
            reaction_type_id = cursor.lastrowid
        else:
            reaction_type_id = reaction_type_id[0]
        cursor.execute('INSERT INTO Reactions (ReactionTypeID, FoodReactionID) VALUES (?, ?)', (reaction_type_id, food_reaction_id))
    
    # Insert into Outcomes and OutcomesTypes tables
    for outcome in record['outcomes']:
        # Check if the outcome type already exists
        cursor.execute('SELECT ID FROM OutcomesTypes WHERE OutcomeTypeName = ?', (outcome,))
        outcome_type_id = cursor.fetchone()
        if not outcome_type_id:
            cursor.execute('INSERT INTO OutcomesTypes (OutcomeTypeName) VALUES (?)', (outcome,))
            outcome_type_id = cursor.lastrowid
        else:
            outcome_type_id = outcome_type_id[0]
        cursor.execute('INSERT INTO Outcomes (OutcomesTypeID, FoodReactionID) VALUES (?, ?)', (outcome_type_id, food_reaction_id))
    
    # Insert into Products, Brands, IndustryNames, and Roles tables
    for product in record['products']:
        # Check if the brand already exists
        cursor.execute('SELECT ID FROM Brands WHERE BrandName = ?', (product['name_brand'],))
        brand_id = cursor.fetchone()
        if not brand_id:
            cursor.execute('INSERT INTO Brands (BrandName) VALUES (?)', (product['name_brand'],))
            brand_id = cursor.lastrowid
        else:
            brand_id = brand_id[0]
        
        # Check if the industry name already exists
        cursor.execute('SELECT ID FROM IndustryNames WHERE IndustryCode = ?', (product['industry_code'],))
        industry_name_id = cursor.fetchone()
        if not industry_name_id:
            cursor.execute('INSERT INTO IndustryNames (IndustryCode, IndustryName) VALUES (?, ?)', (product['industry_code'], product['industry_name']))
            industry_name_id = cursor.lastrowid
        else:
            industry_name_id = industry_name_id[0]
        
        # Check if the role already exists
        cursor.execute('SELECT ID FROM Roles WHERE RoleName = ?', (product['role'],))
        role_id = cursor.fetchone()
        if not role_id:
            cursor.execute('INSERT INTO Roles (RoleName) VALUES (?)', (product['role'],))
            role_id = cursor.lastrowid
        else:
            role_id = role_id[0]
        
        # Insert into Products table
        cursor.execute('''
            INSERT INTO Products (IndustryNameID, BrandID, RoleID, FoodReactionID) VALUES (?, ?, ?, ?)
        ''', (industry_name_id, brand_id, role_id, food_reaction_id))

# Commit the changes
conn.commit()

# Close the connection
conn.close()




