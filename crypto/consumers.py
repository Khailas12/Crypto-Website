from channels.generic.websocket import AsyncJsonWebsocketConsumer
import json



class CoinsConsumers(AsyncJsonWebsocketConsumer):
    async def connect(self):
        await self.channel_layer.group_add('crypto', self.channel_name)
        await self.accept()
        
    async def disconnet(self, code):
        await self.channel_layer.group_discard('crypto', self.channel_name)
        
    async def send_new_data(self, event):
        new_data = event['text']    # fetches coins data from tasks in async_to_sync 
        await self.send(json.dumps(new_data))