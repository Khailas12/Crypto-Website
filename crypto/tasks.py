import requests
from .models import Coin
from celery import shared_task
from channels.layers import get_channel_layer
from django.forms.models import model_to_dict
from asgiref.sync import async_to_sync


channel_layer = get_channel_layer()

@shared_task    # refreshes the coins price every 10 secs
def crypto_data():
    url = 'https://api.coingecko.com/api/v3/coins/markets?vs_currency=inr&order=market_cap_desc&per_page=100&page=1&sparkline=false'  
    coins_data = requests.get(url).json()
    
    crypto = []
    
    for coin in coins_data:
        obj, created = Coin.objects.get_or_create(symbol=coin['symbol'])
        
        obj.name = coin['name']
        obj.symbol = coin['symbol']
        
        if obj.price > coin['current_price']:    # on dip
            state = 'fall'  
            
        elif obj.price < coin['current_price']:     # on pump
            state = 'raise'
            
        elif obj.price == coin['current_price']:    # same as invested amnt
            state = 'same'
        
        obj.price = coin['current_price']
        obj.rank = coin['market_cap_rank']
        obj.image = coin['image']
        
        obj.save()
        
        new_data = model_to_dict(obj)
        new_data.update({'state': state})
        
        crypto.append(new_data)
        
    async_to_sync(channel_layer.group_send)
    ('coins', {
        'type': 'send_new_data',
        'text': crypto,
    })