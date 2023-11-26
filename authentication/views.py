import os
from django.contrib.auth import login
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect
from requests import Response
from rest_framework import status
from rest_framework.views import APIView
from django.conf import settings

import xmltodict
import urllib3
import json

from authentication.models import Profile

# Create your views here.

class LoginView(APIView):
    def get(self, request):
        try:
            ticket = request.GET.get("ticket")
            http = urllib3.PoolManager()
            
            response = http.request('GET', f"{os.environ.get('SSO_URL')}/serviceValidate?ticket={ticket}&service={os.environ.get('APP_URL')}/api/auth/login/")

            rawdata = response.data.decode('utf-8')
            data = xmltodict.parse(rawdata)
            data = data.get('cas:serviceResponse').get('cas:authenticationSuccess')
            
            print(data)
            if(data.get('cas:user') == None):
                return Response({"error": "Invalid ticket"}, status=status.HTTP_400_BAD_REQUEST)
            
            user, created = User.objects.get_or_create(
                username=data.get('cas:user'), 
                email=f"{data.get('cas:user')}@ui.ac.id"
            )
                            
            if(created):
                data = data.get("cas:attributes")
                name = data.get('cas:nama')
                
                i = name.rfind(' ')
                first_name, last_name = name[:i], name[i + 1:]
                
                user.first_name = first_name
                user.last_name = last_name
                user.save()
                
                ORG_CODE = {}
                LANG = settings.SSO_UI_ORG_DETAIL_LANG
                
                with open(settings.SSO_UI_ORG_DETAIL_FILE_PATH, 'r') as ORG_CODE_FILE:
                    ORG_CODE.update(json.load(ORG_CODE_FILE))
                    
                organization = ORG_CODE[LANG][data.get("cas:kd_org")];
                
                _, created = Profile.objects.get_or_create(
                    user=user,
                    npm=data.get('cas:npm'),
                    faculty=organization.get('faculty'),
                    study_program=organization.get('study_program'),
                    educational_program=organization.get('educational_program'),
                )
            
            login(request, user)
             
            return HttpResponseRedirect("/")
               
        except urllib3.exceptions.HTTPError as e:
            print(e)
            return Response(
                {
                    "error": e
                }, 
                status=status.HTTP_400_BAD_REQUEST
            )
        except Exception as e:
            print(e)
            return Response(
                {
                    "error": "Operation Failed"
                }, 
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )