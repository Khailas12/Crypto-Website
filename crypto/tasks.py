import requests

from Crypto_Website.main import celery
from .models import Coin
from django.forms.models import model_to_dict
from celery import shared_task


@shared_task    # refreshes the coins price every 30 secs
def crypto_data():
    url = 'https://api.coingecko.com/api/v3/coins/markets?vs_currency=inr&order=market_cap_desc&per_page=100&page=1&sparkline=false'  
    coins_data = requests.get(url).json()
    
    coins = []
    
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
        
        coins.append(new_data)