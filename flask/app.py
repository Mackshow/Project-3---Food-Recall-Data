# import necessary libraries
import json
from flask import Flask, render_template, request
import sqlite3

################################################
# Flask Setup
##################################################

app = Flask(__name__)
#*******************frontend endpoints*******************
# create route that renders index.html template
@app.route("/")
def home():
    return render_template("index.html")

#***********************API endpoints*********************************
#connect to database
def getcur():
    conn = sqlite3.connect('database/foodReaction.db')        
    return conn

#Round the age to a whole number
def round_age():
    conn = getcur()
    cursor = conn.cursor()    
    # Execute the SQLite query
    cursor.execute("update Consumers set Age = round(Age)")
    conn.commit()
    conn.close()

#-----------------------------------------------------
#select year from 2000 till 2023---dropdown menu
@app.route("/select_years")
def select_years ():    
    conn = getcur()
    cursor = conn.cursor()    
    # Execute the SQLite query
    cursor.execute("SELECT substr(DateStarted, 1, 4) AS Year1 FROM FoodReactions where  Year1 > '2000' group by Year1  ")

    # Fetch all the results
    results = cursor.fetchall()
    json_data=[]    
    for row in results:
        json_data.append(row[0])    

    # Close the connection
    conn.close()
    
    return json.dumps(json_data)

#---------------------------------------------------------
#count of food reactions by industry and age---Age Chart
@app.route("/select_ages_by_year")
def select_ages_by_year ():
    year = request.args.get('year', '2000')    
    age = request.args.get('age', '20')    
    conn = getcur()
    cursor = conn.cursor()    
    # Execute the SQLite query
    sql=f"""
    select  count(*) cnt,
        i.IndustryName
    from 
    Consumers c inner join  FoodReactions f on f.consumerID = c.ID
    inner join Products p on p.FoodReactionID =f.ID
    inner join IndustryNames i on i.ID = p.IndustryNameID 
    where not i.IndustryName = 'Cosmetics'
        and age= {age}
    group by i.IndustryName
    order by cnt desc
    LIMIT 10
    """
    cursor.execute(sql)
 
    # Fetch all the results
    results = cursor.fetchall()
    json_data=[]    
    for row in results:        
        json_data.append([row[0],row[1]])

    # Close the connection
    conn.close()    
    return json.dumps(json_data)

#-----------------------------------------------------------
# Top 5 Outcomes of Food reactions by year---Outcomes Chart
@app.route("/select_by_outcomes_by_year")
def select_by_outcomes_by_year ():

    year = request.args.get('year', '2000')    
    conn = getcur()
    cursor = conn.cursor()    
    # Execute the SQLite query
    sql=f"""
    select  count(*) cnt , OutcomeTypeName
    from   FoodReactions f 
    inner join Outcomes o on f.ID = o.FoodReactionID
        inner join OutcomesTypes ot on o.OutcomesTypeID = ot.ID  
    where substr(f.DateStarted, 1, 4) = '{year}'  
    group by OutcomeTypeName order by cnt desc 
    limit 5
    """ 
      
    cursor.execute(sql) 
    # Fetch all the results
    results = cursor.fetchall()
    json_data=[]    
    for row in results:        
        json_data.append([row[0],row[1] ])

    # Close the connection
    conn.close()    
    return json.dumps(json_data)

#---------------------------------------------------------------------------------------------
# Top Brand names that have most reactions---Brands Pie Chart
@app.route("/select_brands_by_year")
def select_brands_by_year ():

    year = request.args.get('year', '2000')    
    limit  = request.args.get('limit', '')    
    conn = getcur()
    cursor = conn.cursor()    
    # Execute the SQLite query
    if len(limit )>0:
        limit ='LIMIT '+limit 
    
    sql=f"""
    select  count(*) cnt,
         b.BrandName 
    from
    FoodReactions f 
    inner join Reactions r on f.ID = r.FoodReactionID
    inner join ReactionsTypes rt on r.ReactionTypeID = rt.ID 
    inner join Products p on p.FoodReactionID =f.ID
    inner join IndustryNames i on i.ID = p.IndustryNameID
    inner join Brands b on b.ID = p.BrandID
    where substr(f.DateStarted, 1, 4) = '{year}'
        and not i.IndustryName = 'Cosmetics'
        and not b.BrandName = 'EXEMPTION 4'
    group by  b.BrandName 
    order by cnt desc
    {limit}
    """ 
   
    cursor.execute(sql)
 
    # Fetch all the results
    results = cursor.fetchall()
    json_data=[]    
    for row in results:        
        json_data.append([row[0],row[1]])
    # Close the connection
    conn.close()    
    return json.dumps(json_data)

#---------------------------------------------------------------------
#Top count brand names that cause diarrhea per Gender---Diarhea Chart
@app.route("/select_count_dia_brand_year")
def select_count_dia_brand_year():

    year = request.args.get('year', '2000')    
    conn = getcur()
    cursor = conn.cursor()    
    # Execute the SQLite query
    sql=f"""
 select 
    SUM(CASE WHEN c.Gender = 'Male' THEN 1 ELSE 0 END) AS MaleCount,
    SUM(CASE WHEN c.Gender = 'Female' THEN 1 ELSE 0 END) AS FemaleCount,
      i.IndustryName 
    from
    FoodReactions f 
    inner join Reactions r on f.ID = r.FoodReactionID
    inner join ReactionsTypes rt on r.ReactionTypeID = rt.ID 
    inner join Products p on p.FoodReactionID =f.ID
    inner join IndustryNames i on i.ID = p.IndustryNameID    
    inner join Consumers c on c.ID = f.consumerID
    where substr(f.DateStarted, 1, 4) = '{year}' 
        and rt.ReactionTypeName='Diarrhoea'         
    group by  i.IndustryName
    
    limit 10;
   
"""
    cursor.execute(sql)
 
    # Fetch all the results
    results = cursor.fetchall()
    json_data=[]    
    for row in results:        
        json_data.append([row[0],row[1],row[2]])
    data=json_data
    # Close the connection
    conn.close()    
    
    return json.dumps(json_data)
    

if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0", port=80)
    
