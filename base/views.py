# django
from django.views.generic import TemplateView
import requests

# tasks
from base.tasks import calculate_sidi, calculate_siin, notify_when_ready

BACKEND_URL = 'https://k22ok5vv55.execute-api.us-east-1.amazonaws.com/index'
# BACKEND_URL = 'http://localhost'

# Create your views here.
class IndexView(TemplateView):
    template_name = 'index.html'

class WaitView(TemplateView):
    template_name = 'index.html'

    def get(self, *args, **kwargs):
        wait_and_return.delay()
        return super().get(self, *args, **kwargs)
    
class DinDinView(TemplateView):
    template_name = 'index.html'

    def get(self, request, sender, receiver, ping_id, *args, **kwargs):

        print(f'Sender {sender}, Receiver {receiver}, ping {ping_id}')

        ## requests a backend
        # sender_points = requests.get(f'{BACKEND_URL}/index_service/{sender}')
        # receiver_points = requests.get(f'{BACKEND_URL}/map/show_ubications/{receiver}')
        # sender_data = requests.get(f'{BACKEND_URL}/user/{sender}').json()
        # receiver_data = requests.get(f'{BACKEND_URL}/user/{receiver}').json()

        # sender_email = sender_data['data']['attributes']['email']
        # sender_username = sender_data['data']['attributes']['username']
        # receiver_username = receiver_data['data']['attributes']['username']
        sender_points = [
            {
                "lat": -33.498389747758566,
                "long": -70.61207056045534,
                "tags": [
                    "Deporte"
                ]
            },
            {
                "lat": -33.439769189909796,
                "long": -70.63974949460405,
                "tags": [
                    "Parque"
                ]
            },
            {
                "lat": -33.43128553202529,
                "long": -70.55233938277696,
                "tags": [
                    "Universidad",
                    "Trabajo"
                ]
            },
            {
                "lat": -33.37265879474831,
                "long": -70.76179518185943,
                "tags": [
                    "Gimnasio"
                ]
            }
        ]
        receiver_points = [
            {
                "lat": -33.464467735677836,
                "long": -70.6101752732576,
                "tags": [
                    "Fiesta"
                ]
            },
            {
                "lat": -33.462023601556815,
                "long": -70.66064367349894,
                "tags": [
                    "Comida",
                    "Mascotas",
                    "Arte"
                ]
            }
        ]
        sidi = calculate_sidi(sender_points, receiver_points)
        siin = calculate_siin(sender_points, receiver_points)
        dindin = sidi*siin
        print(f'SIDI: {sidi}, SIIN: {siin}, DINDIN: {dindin}')
        ### HACER PATCH INDEXES
        # notify_when_ready(sender_email, sender_username, receiver_username)
        return super().get(self, *args, **kwargs)
