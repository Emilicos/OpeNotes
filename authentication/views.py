import os
from django.http import HttpResponseRedirect
from requests import Response
from rest_framework import status
from rest_framework.views import APIView

import xmltodict
import urllib3

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
            return HttpResponseRedirect("/")
        except urllib3.exceptions.HTTPError as e:
            print(e)
            return Response({"error": e}, status=status.HTTP_400_BAD_REQUEST)