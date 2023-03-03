from django.shortcuts import render
import webbrowser
from django.http import JsonResponse
import requests
from cgi import parse

googletokenlink="https://oauth2.googleapis.com/token"
primarycallink="https://www.googleapis.com/calendar/v3/users/me/calendarList/primary"
google_clientid="698062112558-q3hagrfhgk9t7rek71aku8tnukr2uj72.apps.googleusercontent.com"
secret_key="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" 



constantlink="https://accounts.google.com/o/oauth2/v2/auth?scope=https://www.googleapis.com/auth/calendar.readonly&access_type=offline&include_granted_scopes=true&response_type=code&state=state_parameter_passthrough_value&redirect_uri=http://localhost:8000/rest/v1/calendar/redirect/&client_id=698062112558-q3hagrfhgk9t7rek71aku8tnukr2uj72.apps.googleusercontent.com"


def GoogleCalendarInitView(request):
    webbrowser.open(constantlink)
    return JsonResponse("redirection sucessful",safe=False)

def GoogleCalendarRedirectView(request):
  
 print(request)
 request_p = request.build_absolute_uri()#coverting wsgi req to string to extract code
 errcheck=request_p.find('error')
 print(errcheck)
 if (errcheck!=-1):
    return JsonResponse("authorization failed",safe=False)

 x=request_p.find('&code=') #decoding the code received
 y=request_p.find('&scope=')
 code=request_p[x+6:y]
 code=code.replace("%2F", "/" )

 payloadtoken={
    "code":code,
    "client_id":"698062112558-q3hagrfhgk9t7rek71aku8tnukr2uj72.apps.googleusercontent.com",
    "client_secret":"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",
    "redirect_uri":"http://localhost:8000/rest/v1/calendar/redirect/",
    "grant_type":"authorization_code"
} #payload to generate bearer token

 brtokengen=requests.post(url=googletokenlink,params=payloadtoken)
 if(brtokengen.status_code==200):
    bearertoken=brtokengen.json()['access_token']
    headbrtoken = {'Authorization': 'Bearer ' + bearertoken}

    primarycalender=requests.get(url=primarycallink,headers=headbrtoken)
    if(primarycalender.status_code==200):
        pcalid=primarycalender.json()['id']
        event_link="https://www.googleapis.com/calendar/v3/calendars/"+pcalid+"/events"

        calenderuser=requests.get(url=event_link,headers=headbrtoken)
        if calenderuser.status_code==200:
            return JsonResponse(calenderuser.json(),safe=False)
        return JsonResponse("error can't fetch events",safe=False)
    return(JsonResponse("Can't fetch primary calender",safe=False))
 return (JsonResponse("cannot generate bearer token ",safe=False))