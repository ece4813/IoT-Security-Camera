## Adding one more component, no style yet

# -*- coding: utf-8 -*-
import dash
import dash_core_components as dcc
import dash_html_components as html
import boto3, json
import subprocess
# import itertools
import operator
# from itertools import groupby 
import os
import time
# import itertools 
from boto3.dynamodb.conditions import Key, Attr
import datetime


with open('/home/fiifi/Desktop/4813/PROJECT/IoTCamera/setup/aws_config/config.json') as aws_config:
    data = json.load(aws_config)

dynamodb = boto3.resource('dynamodb')

AWS_KEY= data.get('AWS_KEY', '')
AWS_SECRET= data.get('AWS_SECRET', '')
REGION = data.get('REGION', '')
BUCKET = data.get('BUCKET', '')

table = dynamodb.Table('human-detections')
table2 = dynamodb.Table('false-positives')
table3 = dynamodb.Table('weapon-detections')

#human
response = table.scan()
items = response['Items']

#false positives
response2 = table2.scan()
items2 = response2['Items']

#weapons 
response3 = table3.scan()
items3 = response3['Items']

#human data
humandata = []
for item in items:
    humandata.append(item['timestamp'])

#false positive data
fpdata = []
for item in items2:
    fpdata.append(item['timestamp'])

#false positive data
wdata = []
for item in items3:
    wdata.append(item['timestamp'])



def most_common(lst):
    return max(set(lst), key=lst.count)



# HUMAN DATA
datearr = []
timearr = []
hyear = []
hmonth = []
hday = []
hhour = []
hmins = []

for entry in humandata:
    [date, time] = entry.split()
    datearr.append(date)
    timearr.append(time)

for entry in timearr:
    [hour,mins,sec] = entry.split(':')
    hour = int(hour)
    mins = int(mins)
    # sec = float(sec)
    hhour.append(hour)
    hmins.append(mins)

for entry in datearr:
    [year, month, day] = entry.split('-')
    year = int(year)
    month = int(month)
    day = int(day)
    hday.append(day)
    hmonth.append(month)
    hyear.append(year)


# False Postive data
fpdatearr = []
fptimearr = []
fpyear = []
fpmonth = []
fpday = []
fphour = []
fpmins = []

for entry in fpdata:
    [date, time] = entry.split()
    fpdatearr.append(date)
    fptimearr.append(time)

for entry in fptimearr:
    [hour,mins,sec] = entry.split(':')
    hour = int(hour)
    mins = int(mins)
    # sec = float(sec)
    fphour.append(hour)
    fpmins.append(mins)

for entry in fpdatearr:
    [year, month, day] = entry.split('-')
    year = int(year)
    month = int(month)
    day = int(day)
    fpday.append(day)
    fpmonth.append(month)
    fpyear.append(year)


# Weapons Data
wdatearr = []
wtimearr = []
wyear = []
wmonth = []
wday = []
whour = []
wmins = []

for entry in wdata:
    [date, time] = entry.split()
    wdatearr.append(date)
    wtimearr.append(time)

for entry in wtimearr:
    [hour,mins,sec] = entry.split(':')
    hour = int(hour)
    mins = int(mins)
    # sec = float(sec)
    whour.append(hour)
    wmins.append(mins)

for entry in wdatearr:
    [year, month, day] = entry.split('-')
    year = int(year)
    month = int(month)
    day = int(day)
    wday.append(day)
    wmonth.append(month)
    wyear.append(year)


humanobjects = os.popen('aws s3 ls s3://raspcam-archive/human/ --recursive --summarize | grep -o "Total Objects.*" | cut -f2- -d:').read()
fpobjects = os.popen('aws s3 ls s3://raspcam-archive/false_positive/ --recursive --summarize | grep -o "Total Objects.*" | cut -f2- -d:').read()
weaponobjects = os.popen('aws s3 ls s3://raspcam-archive/weapons/ --recursive --summarize | grep -o "Total Objects.*" | cut -f2- -d:').read()

Days = range(1,32)
Months = range(1,13)
Hours = range(1,25)
Mins = range(1,61)
# data for humans
days_dict= dict.fromkeys(Days)
months_dict = dict.fromkeys(Months)
hours_dict = dict.fromkeys(Hours)
mins_dict = dict.fromkeys(Mins)
# print hday

def getdayValue():
    for day in days_dict:
        day = int(day)
        days_dict[day] = 0
        
    for entry in hday:
        if entry in days_dict:
            days_dict[entry]+=1
    return days_dict

def getmonthValue():
    for mnth in months_dict:
        mnth = int(mnth)
        months_dict[mnth] = 0
        
    for entry in hmonth:
        if entry in months_dict:
            months_dict[entry]+=1
    return months_dict

def gethourValue():
    for hr in hours_dict:
        hr = int(hr)
        hours_dict[hr] = 0
        
    for entry in hhour:
        if entry in hours_dict:
            hours_dict[entry]+=1
    return hours_dict

def getminsValue():
    for mins in mins_dict:
        mins = int(mins)
        mins_dict[mins] = 0
        
    for entry in hmins:
        if entry in mins_dict:
            mins_dict[entry]+=1
    return mins_dict

# Call helpers 
getdayValue()
getmonthValue()
gethourValue()
getminsValue()
# data for fp
fpDays = range(1,32)
fpMonths = range(1,13)
fpHours = range(1,25)
fpMins = range(1,61)

fpdays_dict= dict.fromkeys(fpDays)
fpmonths_dict = dict.fromkeys(fpMonths)
fphours_dict = dict.fromkeys(fpHours)
fpmins_dict = dict.fromkeys(fpMins)

# print hday

def fpgetdayValue():
    for day in fpdays_dict:
        day = int(day)
        fpdays_dict[day] = 0
        
    for entry in fpday:
        if entry in fpdays_dict:
            fpdays_dict[entry]+=1
    return fpdays_dict

def fpgetmonthValue():
    for mnth in fpmonths_dict:
        mnth = int(mnth)
        fpmonths_dict[mnth] = 0
        
    for entry in fpmonth:
        if entry in fpmonths_dict:
            fpmonths_dict[entry]+=1
    return fpmonths_dict

def fpgethourValue():
    for hr in fphours_dict:
        hr = int(hr)
        fphours_dict[hr] = 0
        
    for entry in fphour:
        if entry in fphours_dict:
            fphours_dict[entry]+=1
    return fphours_dict

def fpgetminsValue():
    for mins in fpmins_dict:
        mins = int(mins)
        fpmins_dict[mins] = 0
        
    for entry in fpmins:
        if entry in fpmins_dict:
            fpmins_dict[entry]+=1
    return fpmins_dict

# Call helpers 
fpgetdayValue()
fpgetmonthValue()
fpgethourValue()
fpgetminsValue()


#Data for weapons
wDays = range(1,32)
wMonths = range(1,13)
wHours = range(1,25)
wMins = range(1,61)

wdays_dict= dict.fromkeys(wDays)
wmonths_dict = dict.fromkeys(wMonths)
whours_dict = dict.fromkeys(wHours)
wmins_dict = dict.fromkeys(wMins)

# print hday

def wgetdayValue():
    for day in wdays_dict:
        day = int(day)
        wdays_dict[day] = 0
        
    for entry in wday:
        if entry in wdays_dict:
            wdays_dict[entry]+=1
    return wdays_dict

def wgetmonthValue():
    for mnth in wmonths_dict:
        mnth = int(mnth)
        wmonths_dict[mnth] = 0
        
    for entry in wmonth:
        if entry in wmonths_dict:
            wmonths_dict[entry]+=1
    return wmonths_dict

def wgethourValue():
    for hr in whours_dict:
        hr = int(hr)
        whours_dict[hr] = 0
        
    for entry in whour:
        if entry in whours_dict:
            whours_dict[entry]+=1
    return whours_dict

def wgetminsValue():
    for mins in wmins_dict:
        mins = int(mins)
        wmins_dict[mins] = 0
        
    for entry in wmins:
        if entry in wmins_dict:
            wmins_dict[entry]+=1
    return wmins_dict

# Call helpers 
wgetdayValue()
wgetmonthValue()
wgethourValue()
wgetminsValue()

# Dash stuff
app = dash.Dash()
# app.layout = html.H1('The time is: ' + str(datetime.datetime.now()))
app.layout = html.Div(
    html.Div([
        html.H1(children='IoT Security Camera'),

        html.Div(children='''
            A web application framework to show IoT Security Camera analytics.
        '''),

       
         dcc.Graph(
            id='example-graph-3',
            figure={
                'data': [
                    {'x':list(months_dict.keys()) , 'y': months_dict.values(), 'type': 'linear', 'mode': 'lines+markers', 'marker': {'size': 12}, 'name': 'Human Detections'},
                    {'x': list(fpmonths_dict.keys()), 'y': fpmonths_dict.values(), 'mode': 'lines+markers', 'marker': {'size': 12}, 'name': 'False-positives'},
                    {'x': list(wmonths_dict.keys()), 'y': wmonths_dict.values(), 'type': 'linear', 'mode': 'lines+markers','marker': {'size': 12}, 'name': 'Weapons'},
                ],
                'layout': {
                    'title': 'Rate of Detections Per Month',
                    'xaxis' : dict(
                        title='months',
                        titlefont=dict(
                        family='Courier New, monospace',
                        size=20,
                        color='#7f7f7f'
                    )),
                    'yaxis' : dict(
                        title='# detections',
                        titlefont=dict(
                        family='Helvetica, monospace',
                        size=20,
                        color='#7f7f7f'
                    ))
                }
            }
        ),

        dcc.Graph(
            id='example-graph-2',
            figure={
                'data': [
                    {'x': list(days_dict.keys()), 'y': days_dict.values(), 'mode': 'lines+markers', 'marker': {'size': 12}, 'name': 'Human Detections'},
                    {'x': list(fpdays_dict.keys()), 'y': fpdays_dict.values(), 'mode': 'lines+markers', 'marker': {'size': 12}, 'name': 'False-positives'},
                    {'x': list(wdays_dict.keys()), 'y': wdays_dict.values(), 'mode': 'lines+markers', 'marker': {'size': 12}, 'name': 'Wepaons'},
                ],
                'layout': {
                    'title': 'Rate of Detections Per Day',
                    'xaxis' : dict(
                        title='days',
                        titlefont=dict(
                        family='Courier New, monospace',
                        size=20,
                        color='#7f7f7f'
                    )),
                    'yaxis' : dict(
                        title='# detections',
                        titlefont=dict(
                        family='Helvetica, monospace',
                        size=20,
                        color='#7f7f7f'
                    ))
                }
            }
        ),

       
        dcc.Graph(
            id='example-graph-4',
            figure={
                'data': [
                    {'x':list(hours_dict.keys()) , 'y': hours_dict.values(), 'mode': 'lines+markers', 'marker': {'size': 12},'name': 'Human Detections'},
                    {'x': list(fphours_dict.keys()), 'y': fphours_dict.values(), 'mode': 'lines+markers', 'marker': {'size': 12},'name': 'False-positives'},
                    {'x': list(whours_dict.keys()), 'y': whours_dict.values(), 'mode': 'lines+markers', 'marker': {'size': 12}, 'name': 'Weapons'},
                ],
                'layout': {
                    'title': 'Rate of Detections per hour',
                    'xaxis' : dict(
                        title='hours',
                        titlefont=dict(
                        family='Courier New, monospace',
                        size=20,
                        color='#7f7f7f'
                    )),
                    'yaxis' : dict(
                        title='# detections',
                        titlefont=dict(
                        family='Helvetica, monospace',
                        size=20,
                        color='#7f7f7f'
                    ))
                }
            }
        ),

        dcc.Graph(
            id='example-graph-5',
            figure={
                'data': [
                    {'x':list(mins_dict.keys()) , 'y': mins_dict.values(), 'mode': 'markers', 'marker': {'size': 12}, 'name': 'Human Detections'},
                    {'x': list(fpmins_dict.keys()), 'y': fpmins_dict.values(), 'mode': 'markers', 'marker': {'size': 12},'name': 'False-positives'},
                    {'x': list(wmins_dict.keys()), 'y': wmins_dict.values(), 'mode': 'markers', 'marker': {'size': 12}, 'name': 'Weapons'},
                ],
                'layout': {
                    'title': 'Rate of Detections Per Each Minute of the Hour',
                    'xaxis' : dict(
                        title='mins',
                        titlefont=dict(
                        family='Courier New, monospace',
                        size=20,
                        color='#7f7f7f'
                    )),
                    'yaxis' : dict(
                        title='# detections',
                        titlefont=dict(
                        family='Helvetica, monospace',
                        size=20,
                        color='#7f7f7f'
                    ))
                }
            }
        )               

    ])
)

if __name__ == '__main__':
    app.run_server(debug=True)
