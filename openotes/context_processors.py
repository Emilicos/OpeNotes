import os 

def export_vars(request):
    data = {}
    data['SSO_URL'] = os.environ.get('SSO_URL')
    data['APP_URL'] = os.environ.get('APP_URL')
    data["NAVBAR_MENU"] = [
        {
            "name": "Home",
            "url": "/"
        },
        {
            "name": "Mata Kuliah",
            "url": "/course/"
        },
    ]

    if(request.user.is_authenticated):
        data["NAVBAR_MENU"] += [{
            "name": "Favorit Saya",
            "url": "/favorite"
        }]
    
    return data