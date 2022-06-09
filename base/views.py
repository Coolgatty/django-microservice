# django
from django.views.generic import TemplateView
import requests

# tasks
from base.tasks import calculate_sidi, calculate_siin, notify_when_ready

BACKEND_URL = 'https://k22ok5vv55.execute-api.us-east-1.amazonaws.com/index'
PATCH_URL = 'http://3.223.72.156'

# Create your views here.
class IndexView(TemplateView):
    template_name = 'index.html'
    
class DinDinView(TemplateView):
    template_name = 'index.html'

    def get(self, request, sender, receiver, ping_id, *args, **kwargs):

        print(f'Sender {sender}, Receiver {receiver}, ping {ping_id}')
        ## requests a backend
        sender_points = requests.get(f'{BACKEND_URL}/index-service/{sender}').json()
        receiver_points = requests.get(f'{BACKEND_URL}/index-service/{receiver}').json()
        sender_data = requests.get(f'{BACKEND_URL}/user/{sender}').json()
        receiver_data = requests.get(f'{BACKEND_URL}/user/{receiver}').json()
        sender_email = sender_data['data']['attributes']['email']
        sender_username = sender_data['data']['attributes']['username']
        receiver_username = receiver_data['data']['attributes']['username']
        print(sender_points)
        if (len(sender_points) > 0 and len(receiver_points) > 0):
            sidi = calculate_sidi(sender_points, receiver_points)
            siin = calculate_siin(sender_points, receiver_points)
            dindin = sidi*siin
            print(f'SIDI: {sidi}, SIIN: {siin}, DINDIN: {dindin}')
            payload = { "siin": siin, "sidi": sidi, "dindin": dindin, "state": 'ready' }
            notify_when_ready(sender_email, sender_username, receiver_username)
            requests.patch(f'{PATCH_URL}/index-result/update/{ping_id}', payload)
        else:
            notify_when_ready(sender_email, sender_username, receiver_username)
            requests.patch(f'{PATCH_URL}/index-result/update/{ping_id}', {"siin": 0, "sidi": 0, "dindin": 0, "state": 'missing points'})
        return super().get(self, *args, **kwargs)
