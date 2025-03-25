import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from .models import Task, Comment


class TaskConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.task_id = self.scope["url_route"]["kwargs"]["task_id"]
        self.task_group_name = f"task_{self.task_id}"

        await self.channel_layer.group_add(self.task_group_name, self.channel_name)
        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(self.task_group_name, self.channel_name)

    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message_type = text_data_json["type"]

        if message_type == "task_update":
            task_data = text_data_json["task"]
            await self.update_task(task_data)
        elif message_type == "comment":
            comment_data = text_data_json["comment"]
            await self.add_comment(comment_data)

        await self.channel_layer.group_send(
            self.task_group_name,
            {"type": "broadcast_update", "message": text_data_json},
        )

    async def broadcast_update(self, event):
        message = event["message"]
        await self.send(text_data=json.dumps(message))

    @database_sync_to_async
    def update_task(self, task_data):
        task = Task.objects.get(id=self.task_id)
        task.status = task_data.get("status", task.status)
        task.priority = task_data.get("priority", task.priority)
        task.save()

    @database_sync_to_async
    def add_comment(self, comment_data):
        Comment.objects.create(
            task_id=self.task_id,
            user=self.scope["user"],
            content=comment_data["content"],
        )
