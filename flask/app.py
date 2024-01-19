# import necessary libraries
import json
import numpy as np
import pandas as pd

from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, render_template, request, jsonify, redirect
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

#round the age to a whole number
def round_age():
    conn = getcur()
    cursor = conn.cursor()    
    # Execute the SQLite query
    cursor.execute("update Consumers set Age = round(Age)")
    conn.commit()
    conn.close()


#select year from 2000 till 2023
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

#donut chart selection
@app.route("/select_ages_by_year")
def select_ages_by_year ():
    year = request.args.get('year', '2000')    
    conn = getcur()
    cursor = conn.cursor()    
    # Execute the SQLite query
    sql=f"""
    select  count(*) cnt,
        i.IndustryName, c.Age    
    from 
    Consumers c inner join  FoodReactions f on f.consumerID = c.ID
    inner join Products p on p.FoodReactionID =f.ID
    inner join IndustryNames i on i.ID = p.IndustryNameID 
    where substr(DateStarted, 1, 4) = '{year}' group by Age
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

"""
        cursor.execute(sql)
        row_headers = [x[0] for x in cur.description]  
        rv = cursor.fetchall()
        json_data = []
        for result in rv:
            json_data.append(dict(zip(row_headers, result)))
        rr = {
            'code': 20000,
            'data': json_data
        }
"""
    
# (top 5 food industries that have most reactions) bubble chart selection
@app.route("/select_top5_brand_fir_by_year")
def select_top5_fir_brand_by_year ():

    year = request.args.get('year', '2000')
    conn = getcur()
    cursor = conn.cursor()    
    # Execute the SQLite query
    sql=f"""
    select  count(*) cnt,
        i.IndustryName, b.BrandName, rt.ReactionTypeName
    from
    FoodReactions f 
    inner join Reactions r on f.ID = r.FoodReactionID
    inner join ReactionsTypes rt on r.ReactionTypeID = rt.ID 
    inner join Products p on p.FoodReactionID =f.ID
    inner join IndustryNames i on i.ID = p.IndustryNameID
    inner join Brands b on b.ID = p.BrandID
    where substr(f.DateStarted, 1, 4) = '{year}'
        and not i.IndustryName = 'Cosmetics'
    group by i.IndustryName, b.BrandName, rt.ReactionTypeName
    order by cnt desc
    """ 
    sql=f"""
    select  count(*) cnt,
        i.IndustryName, b.BrandName, rt.ReactionTypeName
    from
    FoodReactions f 
    inner join Reactions r on f.ID = r.FoodReactionID
    inner join ReactionsTypes rt on r.ReactionTypeID = rt.ID 
    inner join Products p on p.FoodReactionID =f.ID
    inner join IndustryNames i on i.ID = p.IndustryNameID
    inner join Brands b on b.ID = p.BrandID
    where   not i.IndustryName = 'Cosmetics'
    group by i.IndustryName, b.BrandName, rt.ReactionTypeName
    order by cnt desc
    """ 
    #----------------------
   
    cursor.execute(sql)
 
    # Fetch all the results
    results = cursor.fetchall()
    json_data=[]    
    for row in results:        
        json_data.append([row[0],row[1],row[2],row[3]])

    # Close the connection
    conn.close()    
    return json.dumps(json_data)


# (count by food reations by year  ) board chart 
@app.route("/select_count_by_food_reactions_by_year")
def select_count_by_food_reactions_by_year ():

    year = request.args.get('year', '2000')    
    conn = getcur()
    cursor = conn.cursor()    
    # Execute the SQLite query
    sql=f"""
    select  count(*) cnt,  rt.ReactionTypeName
    from

    FoodReactions f 
    inner join Reactions r on f.ID = r.FoodReactionID
        inner join ReactionsTypes rt on r.ReactionTypeID = rt.ID 
         
    where substr(f.DateStarted, 1, 4) = '{year}' 
    group by  rt.ReactionTypeName
    order by cnt desc
    """ 
    #----------------------   
    cursor.execute(sql)
 
    # Fetch all the results
    results = cursor.fetchall()
    json_data=[]    
    for row in results:        
        json_data.append([row[0],row[1] ])

    # Close the connection
    conn.close()    
    return json.dumps(json_data)

# (total number of food reations by year  ) board chart
@app.route("/select_total_food_reactions_by_year")
def select_total_food_reactions_by_year ():

    year = request.args.get('year', '2000')    
    conn = getcur()
    cursor = conn.cursor()    
    # Execute the SQLite query
    sql=f"""
    select  count(*) cnt 
    from   FoodReactions f 
    inner join Reactions r on f.ID = r.FoodReactionID
        inner join ReactionsTypes rt on r.ReactionTypeID = rt.ID  
    where substr(f.DateStarted, 1, 4) = '{year}'  
    """ 
    #----------------------   
    cursor.execute(sql)
 
    # Fetch all the results
    results = cursor.fetchall()
    json_data=[]    
    for row in results:        
        json_data.append([row[0][0] ])

    # Close the connection
    conn.close()    
    return json.dumps(json_data)



# (total number of hosp by year) board chart
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
    """ 
    #----------------------   
    cursor.execute(sql) 
    # Fetch all the results
    results = cursor.fetchall()
    json_data=[]    
    for row in results:        
        json_data.append([row[0],row[1] ])

    # Close the connection
    conn.close()    
    return json.dumps(json_data)


# (total number of hosp by year  ) board chart
@app.route("/select_count_hosp_by_year")
def select_count_hosp_by_year ():

    year = request.args.get('year', '2000')    
    conn = getcur()
    cursor = conn.cursor()    
    # Execute the SQLite query
    sql=f"""
    select  count(*) cnt  
    from   FoodReactions f 
    inner join Outcomes o on f.ID = o.FoodReactionID
        inner join OutcomesTypes ot on o.OutcomesTypeID = ot.ID  
    where substr(f.DateStarted, 1, 4) = '{year}'  and OutcomeTypeName='Hospitalization'
    
    """ 
    #----------------------   
    cursor.execute(sql) 
    # Fetch all the results
    results = cursor.fetchall()
    json_data=[]    
    for row in results:        
        json_data.append([row[0][0]  ])

    # Close the connection
    conn.close()    
    return json.dumps(json_data)


# (top 5 brand names that have most reactions  )
@app.route("/select_top5_brands_by_year")
def select_top5_brands_by_year ():

    year = request.args.get('year', '2000')    
    conn = getcur()
    cursor = conn.cursor()    
    # Execute the SQLite query
    sql=f"""
    select  count(*) cnt,
        i.IndustryName, b.BrandName, rt.ReactionTypeName
    from
    FoodReactions f 
    inner join Reactions r on f.ID = r.FoodReactionID
    inner join ReactionsTypes rt on r.ReactionTypeID = rt.ID 
    inner join Products p on p.FoodReactionID =f.ID
    inner join IndustryNames i on i.ID = p.IndustryNameID
    inner join Brands b on b.ID = p.BrandID
    where substr(f.DateStarted, 1, 4) = '{year}'
        and not i.IndustryName = 'Cosmetics'
    group by i.IndustryName, b.BrandName, rt.ReactionTypeName
    order by cnt desc
    """ 
 
    #----------------------
   
    cursor.execute(sql)
 
    # Fetch all the results
    results = cursor.fetchall()
    json_data=[]    
    for row in results:        
        json_data.append([row[0],row[1],row[2],row[3]])

    # Close the connection
    conn.close()    
    return json.dumps(json_data)





#Top count brand names that cause diarrhea
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
    and rt.ReactionTypeName='Diarrhoea'         
    group by   i.IndustryName          ;
   
"""
    cursor.execute(sql)
 
    # Fetch all the results
    results = cursor.fetchall()
    json_data=[]    
    for row in results:        
        json_data.append([row[0],row[1],row[2]  ])
    data=json_data
    # Close the connection
    conn.close()    
    #return json.dumps(json_data)
    labels = [x[2] for x in data]
    male_count = [x[0] for x in data]
    female_count = [x[1] for x in data]
    return render_template('diarrheaBars.html', labels=labels, male_count=male_count, female_count=female_count)





#Top count brand names that cause diarrhea
@app.route("/select_count_by_reactions_year")
def select_count_by_reactions_year():

    year = request.args.get('year', '2000')    
    conn = getcur()
    cursor = conn.cursor()    
    # Execute the SQLite query
    sql=f"""
    select  count(*) cnt,
        ReactionTypeName 
    from
    FoodReactions f 
    inner join Reactions r on f.ID = r.FoodReactionID
    inner join ReactionsTypes rt on r.ReactionTypeID = rt.ID 
    inner join Products p on p.FoodReactionID =f.ID
    inner join IndustryNames i on i.ID = p.IndustryNameID
    inner join Brands b on b.ID = p.BrandID
    where substr(f.DateStarted, 1, 4) = '{year}'
         
    group by  ReactionTypeName
    
    order by cnt desc
    """  
    #----------------------
   
    cursor.execute(sql)
 
    # Fetch all the results
    results = cursor.fetchall()
    json_data=[]    
    for row in results:        
        json_data.append([row[0],row[1] ])

    # Close the connection
    conn.close()    
    return json.dumps(json_data)




if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0", port=80)
    #kkk()
#    select_years()