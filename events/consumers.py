import json
from channels.generic.websocket import AsyncWebsocketConsumer
from .models import Event
from .serializers import EventSerializer

class EventConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        await self.accept()

    async def disconnect(self, close_code):
        pass

    async def receive(self, text_data):
        data = json.loads(text_data)
        event_id = data['event_id']
        action = data['action']

        event = await self.get_event(event_id)

        if action == "join":
            event.joiners.add(self.scope["user"])
        elif action == "cancel":
            await event.delete()

        await self.send_event_update(event)

    async def send_event_update(self, event):
        serializer = EventSerializer(event)
        await self.send(text_data=json.dumps(serializer.data))

    @database_sync_to_async
    def get_event(self, event_id):
        return Event.objects.get(id=event_id)
