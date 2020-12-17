import pandas as pd
from haversine import haversine
from flask import Blueprint, render_template, request, session
import datetime
location_blue = Blueprint('location_blue', __name__)

@location_blue.route('/location', defaults={'latitude' : 37.5796653058195, 'longitude' : 126.998962996348, 'id' : 1})
@location_blue.route('/location/latitude=<latitude>', defaults={'longitude' : 126.998962996348, 'id' : 1})
@location_blue.route('/location/latitude=<latitude>/longitude=<longitude>/<id>')
def location(latitude, longitude, id) :
    latitude = float(latitude)
    longitude = float(longitude)

    location = (latitude, longitude)
    df = pd.read_csv('./data/data.csv')
    result = []
    for index in range(1,len(df)) :
        tmp = {}
        
        data = df['latitude'][index], df['longitude'][index]
        
        if haversine(location, data) < 5 :
            
            tmp['place_1'] = df['place-info1'][index]
            tmp['place_2'] = df['place-info2'][index]
            tmp['movearound_date'] = df['movearound_date'][index]
            tmp['km'] = haversine(location, data)
            result.append(tmp)
    
    df2 = pd.DataFrame(result)
    
    data = df2[df2['movearound_date']!= 'NaN/NaN']
    data['movearound_date'] = pd.to_datetime('2020/'+data['movearound_date'])
    
    result2 = data.groupby('movearound_date').count()['place_1'][-7:].reset_index()
    result2.rename(columns={'place_1':'count'}, inplace=True)
    today = datetime.date.today()  
    day = {today.strftime("%Y-%m-%d"):0, (today - datetime.timedelta(1)).strftime("%Y-%m-%d") : 0, (today - datetime.timedelta(2)).strftime("%Y-%m-%d") : 0, (today - datetime.timedelta(3)).strftime("%Y-%m-%d") : 0, (today - datetime.timedelta(4)).strftime("%Y-%m-%d") : 0, (today - datetime.timedelta(5)).strftime("%Y-%m-%d") : 0, (today - datetime.timedelta(6)).strftime("%Y-%m-%d") : 0}
    
    day_list = list(result2['movearound_date'])
    day_list = str(day_list)
    for row in day :
        if row in day_list :
            day[row] = result2[result2['movearound_date'] == row]['count'].values[0]
    day = pd.DataFrame({'movearound_date':list(day.keys()), 'count':list(day.values())})
    km_data = {'1km':0,'2km':0,'3km':0,'4km':0,'5km':0}
    for i in range(len(result)) :
        
        if result[i]['km'] < 1 :
            km_data['1km'] = km_data['1km'] + 1
        elif result[i]['km'] < 2 :
            km_data['2km'] = km_data['2km'] + 1
        elif result[i]['km'] < 3 :
            km_data['3km'] = km_data['3km'] + 1
        elif result[i]['km'] < 4 :
            km_data['4km'] = km_data['4km'] + 1
        elif result[i]['km'] < 5 :
            km_data['5km'] = km_data['5km'] + 1

    score = km_data['1km'] + km_data['2km'] + km_data['3km'] + km_data['4km'] + km_data['5km']
    
    score = score/len(df)

    html = render_template('location.html', info = result, day = day, km_data = km_data, id=id)
    return html