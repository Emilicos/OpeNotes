import os 

def export_vars(request):
    data = {}
    data['SSO_URL'] = os.environ.get('SSO_URL')
    data['APP_URL'] = os.environ.get('APP_URL')
    
    return data