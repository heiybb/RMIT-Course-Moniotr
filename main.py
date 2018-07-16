import requests
from lxml import html
import json
import re

username = 's*******'
password = '******'

login = 'https://sso-cas.rmit.edu.au/rmitcas/login'
timetableurl = 'https://mytimetable.rmit.edu.au/even/student'

with requests.session() as c:
    tokenrequest = c.get(login)
    tokentree = html.fromstring(tokenrequest.content)

    tokens = tokentree.xpath('//input[@type="hidden"]/@name')
    values = tokentree.xpath('//input[@type="hidden"]/@value')

    # Add credentials to postdata
    payload = {
        'username': username,
        'password': password
    }
    # Add additional login tokens
    for i, t in enumerate(tokens):
        payload.update({t: values[i]})

    loginrequest = c.post(login, data=payload)

    ttreq = c.get(timetableurl)
    sstoken = re.search("(?<=ss=).*", ttreq.url).group()
    querystring = {"ss": sstoken}

    # Only cover the AP Course
    url = "https://mytimetable.rmit.edu.au/even/rest/student/s3677943/subject/COSC1295_1850_1725_AUSCY/group/PRA01/activities/"
    response = c.request("GET", url,params=querystring)

    timeTable = json.loads(response.text)
    # print(timeTable)
    for course in timeTable:
        print(course)
        print('时间：\t\t' + timeTable[course]['day_of_week'] + ' ' + timeTable[course]['start_time'])
        print('教室：\t\t' + timeTable[course]['location'])
        print('可选状态：\t' + timeTable[course]['selectable'])
        print('剩余位置：\t' + str(timeTable[course]['availability']))
