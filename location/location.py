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
    df = pd.read_csv('./data/data.csv', engine='python', encoding='utf-8')
    result = []
    for index in range(1,len(df)) :
        tmp = {}
        
        data = df['latitude'][index], df['longitude'][index]
        
        if haversine(location, data) < 5 :
            tmp['place_1'] = df['place'][index]
            # tmp['place_2'] = []
            tmp['movearound_date'] = df['date'][index]
            tmp['km'] = haversine(location, data)
            result.append(tmp)
            
    if result == [] :
        html = render_template('location_out.html', score = 0)
        return html
    
    result = sorted(result, key = lambda x : x['km'])
    df2 = pd.DataFrame(result)
    
    
    
    data = df2[df2['movearound_date']!= 'NaN/NaN']
    
    data['movearound_date'] = pd.to_datetime('2020/'+data['movearound_date'])
    
    result2 = data.groupby('movearound_date').count()['place_1'][-7:].reset_index()
    result2.rename(columns={'place_1':'count'}, inplace=True)
    today = datetime.date.today()  
    day = {(today  - datetime.timedelta(4)).strftime("%Y-%m-%d"):0, (today - datetime.timedelta(5)).strftime("%Y-%m-%d") : 0, (today - datetime.timedelta(6)).strftime("%Y-%m-%d") : 0, (today - datetime.timedelta(7)).strftime("%Y-%m-%d") : 0, (today - datetime.timedelta(8)).strftime("%Y-%m-%d") : 0, (today - datetime.timedelta(9)).strftime("%Y-%m-%d") : 0, (today - datetime.timedelta(10)).strftime("%Y-%m-%d") : 0,
        (today  - datetime.timedelta(11)).strftime("%Y-%m-%d"):0, (today - datetime.timedelta(12)).strftime("%Y-%m-%d") : 0, (today - datetime.timedelta(13)).strftime("%Y-%m-%d") : 0, (today - datetime.timedelta(14)).strftime("%Y-%m-%d") : 0, (today - datetime.timedelta(15)).strftime("%Y-%m-%d") : 0, (today - datetime.timedelta(16)).strftime("%Y-%m-%d") : 0, (today - datetime.timedelta(17)).strftime("%Y-%m-%d") : 0}
    
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
    
    score = (km_data['1km']*10 + km_data['2km']*8 + km_data['3km']*6 + km_data['4km']*4 + km_data['5km']*2)/len(df)
    
    score = int(score * 200)
    if score > 100 :
        score = 100
    html = render_template('location.html', info = result, day = day, km_data = km_data, id=id, score = score)
    return html

@location_blue.route('/map')
def map() :
    df = pd.read_csv('./data/data.csv', engine='python', encoding='utf-8')
    
    df =  df.dropna(axis=0)
    
    lat = list(df['latitude'])
    lon = list(df['longitude'])
    movearound_date = list(df['date'])
    place_info1 = list(df['place'])
    place_info2 = []
    # list(df['place-info2'])
    number = list(df['tag'])
    html = render_template('map.html', df = df, lat=lat, lon=lon, movearound_date=movearound_date, place_info1=place_info1, place_info2=place_info2, number=number)
    return html


@location_blue.route('/upload_kmlam')
def load_file():

    html = render_template('upload.html')
    
    return html

@location_blue.route('/uploader', methods = ['GET', 'POST'])
def upload_file():
   if request.method == 'POST':
      f = request.files['file']
      f.save("./data/" + secure_filename(f.filename))
      return 'file uploaded successfully'


@location_blue.route('/protection')
def protection() :
    data = pd.read_csv('./data/tlscjswl.csv')
    location = list(data['주소'])
    lat = list(data['위도'])
    lon = list(data['경도'])
    html = render_template('protection.html', location=location, lat=lat, lon=lon)
    
    return html


@location_blue.route('/protection1', defaults={'latitude' : 37.5796653058195, 'longitude' : 126.998962996348, 'id' : 1})
@location_blue.route('/protection1/latitude=<latitude>', defaults={'longitude' : 126.998962996348, 'id' : 1})
@location_blue.route('/protection1/latitude=<latitude>/longitude=<longitude>/<id>')
def protection1(latitude, longitude, id) :
    latitude = float(latitude)
    longitude = float(longitude)

    location = (latitude, longitude)
    df = pd.read_csv('./data/tlscjswl.csv')
    result = []
    for index in range(1,len(df)) :
        tmp = {}
        
        data = df['위도'][index], df['경도'][index]
        
        if haversine(location, data) < 3 :
            
            tmp['place_1'] = df['주소'][index]
            
            result.append(tmp)
    
    if result == [] :
        html = render_template('protection1_out.html', score=0)
        return html
    
    score = len(result)*10
    if score >= 100 :
        score = 100
    html = render_template('protection1.html', info = result, score = score)
    return html
    