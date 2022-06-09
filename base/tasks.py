# celery
from celery import shared_task
from math import sqrt, log
import requests
from django.core.mail import send_mail
from django.conf import settings

BACKEND_URL = 'https://k22ok5vv55.execute-api.us-east-1.amazonaws.com/index'
PATCH_URL = 'http://3.223.72.156'

# The "shared_task" decorator allows creation
# of Celery tasks for reusable apps as it doesn't
# need the instance of the Celery app.
# @celery_app.task()

def centroid(points):
    sum_lat = 0
    sum_long = 0

    for  p  in  points:
        sum_lat += p['lat']
        sum_long += p['long']
    return {'lat': sum_lat/len(points), 'long': sum_long/len(points)}

@shared_task
def calculate_sidi(sender_points, receiver_points):
    # calculo
    c1 = centroid(sender_points)
    c2 = centroid(receiver_points)
    d = sqrt((c2['lat'] - c1['lat'])**2 + (c2['long'] - c1['long'])**2)
    sidi = (len(sender_points) + len(receiver_points))/log(d)

    return sidi

@shared_task
def calculate_siin(sender_points, receiver_points):

    tags = requests.get(f'{BACKEND_URL}/tag/all').json()

    sender_interests = {tag['attributes']['name']: 0 for tag in tags['data']}
    receiver_interests = {tag['attributes']['name']: 0 for tag in tags['data']}
    
    for point in sender_points:
        for tag in point["tags"]:
            sender_interests[tag] += 1
    
    for point in receiver_points:
        for tag in point["tags"]:
            receiver_interests[tag] += 1
    
    # calculo
    sum = 0
    diff = 0
    for tag in sender_interests.keys():
        sum += sender_interests[tag] + receiver_interests[tag]
        diff += abs(sender_interests[tag] - receiver_interests[tag])

    siin = (sum - diff)/sum
    return siin

@shared_task
def notify_when_ready(email, sender, receiver):
    send_mail(
    'Calculo de indíces finalizado',
    f'¡Hola {sender}!, los indices asociados al ping que le hiciste a {receiver} ya estan disponibles',
    settings.EMAIL_HOST_USER,
    [email],
    fail_silently=False)

@shared_task
def recalculate_indexes():
    pings = requests.get(f'{BACKEND_URL}/ping/index').json()
    print(pings)
    return

@shared_task
def recalculate_index(sender, receiver, ping_id):

    print(f'Sender {sender}, Receiver {receiver}, ping {ping_id}')
    sender_points = requests.get(f'{BACKEND_URL}/index-service/{sender}').json()
    receiver_points = requests.get(f'{BACKEND_URL}/index-service/{receiver}').json()
    if (len(sender_points) > 0 and len(receiver_points) > 0):
        sidi = calculate_sidi(sender_points, receiver_points)
        siin = calculate_siin(sender_points, receiver_points)
        dindin = sidi*siin
        print(f'SIDI: {sidi}, SIIN: {siin}, DINDIN: {dindin}')
        payload = { "siin": siin, "sidi": sidi, "dindin": dindin, "state": 'ready' }
        requests.patch(f'{PATCH_URL}/index-result/update/{ping_id}', payload)
    else:
        requests.patch(f'{PATCH_URL}/index-result/update/{ping_id}', {"siin": 0, "sidi": 0, "dindin": 0, "state": 'missing points'})
    return


