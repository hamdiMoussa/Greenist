from .models import *

def result():
    post = Node.objects.order_by('-IdNode').first()
    tempp = post.temperature
    humm = post.humidity
    windd = post.wind

    if tempp > 30 and humm < 30 and windd > 30:
        status = 'Risk'
    else:
        status = 'SAFE'
    return status