from database import db
from datetime import datetime, timezone, timedelta

utc_now = datetime.utcnow().replace(tzinfo=timezone.utc)

vietnam_tz = timezone(timedelta(hours=7))
vietnam_now = utc_now.astimezone(vietnam_tz)
class MessageModel:
    collection = db.messages  # Định nghĩa collection cho MongoDB

    @staticmethod
    def save_message(user, message, room):
        """ Lưu tin nhắn vào MongoDB """
        msg = {
            "user": user,
            "message": message,
            "room": room,
            "timestamp": vietnam_now.isoformat(timespec="milliseconds")
        }
        MessageModel.collection.insert_one(msg)
        return msg

    @staticmethod
    def get_messages(room):
        """ Lấy danh sách tin nhắn từ MongoDB theo phòng chat """
        messages = MessageModel.collection.find({"room": room}).sort("timestamp", 1)
        return [
            {
                "user": msg["user"],
                "message": msg["message"],
                "timestamp": msg["timestamp"]
            }
            for msg in messages
        ]
