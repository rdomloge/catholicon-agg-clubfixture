from flask import Flask, request
from datetime import datetime

import requests, logging

#Configure logging
logging.basicConfig()
logging.root.setLevel(logging.DEBUG)

HOSTPORT = "rdomloge.entrydns.org:80"
FIXTURE_URL_TEMPLATE = "http://"+HOSTPORT+"/fixtures/search/findByExternalFixtureId?externalFixtureId="
CLUBS_URL_TEMPLATE = "http://"+HOSTPORT+"/clubs/search/findClubByTeamId?teamId="

fixtureDateFormat = "%Y-%m-%dT%H:%M:%SZ"

app = Flask(__name__)

def fetchFixture(fixtureId):
    response = requests.get(FIXTURE_URL_TEMPLATE+str(fixtureId))
    if response.status_code == 200:
        logging.info('Got this response for the fixture: '+response.text)
        return response.json()
    else:
        logging.warning('Response code was '+str(response.status_code))

def fetchClub(teamId):
    response = requests.get(CLUBS_URL_TEMPLATE+str(teamId))
    if response.status_code == 200:
        logging.info('Got this response for the club: '+response.text)
        return response.json()
    else:
        logging.warning('Response code was '+str(response.status_code))

def weekDayConversion(days):
    if "Mondays" == days: return 0
    if "Tuesdays" == days: return 1
    if "Wednesdays" == days: return 2
    if "Thursdays" == days: return 3
    if "Fridays" == days: return 4
    if "Saturdays" == days: return 5
    if "Sundays" == days: return 6

def fetchMatchSessionForFixture(homeTeamId, matchDate):
    club = fetchClub(homeTeamId)
    matchDayOfWeek = datetime.strptime(matchDate, fixtureDateFormat).date().weekday() # Monday is 0 & Sunday is 6
    
    for sesh in club["matchSessions"]:
        if weekDayConversion(sesh["days"]) == matchDayOfWeek: return sesh
        
    # the fixture date doesn't match any match session - maybe they are playing on a club night?
    for sesh in club["clubSessions"]:
        if weekDayConversion(sesh["days"]) == matchDayOfWeek: return sesh
            

@app.route('/', methods=['GET'])
def index():
    if request.args.get('fixtureId') == None:
        return 'Error - please specify fixtureId'
    fixtureId = request.args['fixtureId']
    fixture = fetchFixture(fixtureId=fixtureId)
    print(str(type(fixture)))
    homeTeamId = fixture["homeTeamId"]
    matchDate = fixture["matchDate"]
    matchSession = fetchMatchSessionForFixture(homeTeamId=homeTeamId, matchDate=matchDate)
    jsonResponse = {
        "fixture": fixture,
        "session": matchSession
    }
    return jsonResponse

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0') 

