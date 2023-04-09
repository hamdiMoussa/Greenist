from .models import *

def result():

    post = Data.objects.order_by('-IdData').first()
    tempp = post.temperature
    humm = post.humidity
    windd = post.wind
    
    if tempp > 10 and humm < 50 and windd > 0:
    #if tempp > 20 and humm < 80 and windd > 4:
        status = 'Risk'
    else:
        status = 'SAFE'
    return status