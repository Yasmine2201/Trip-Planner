import redis
import json

redis_client = redis.StrictRedis(host='localhost', port=6379, db=0)


def publish_notification(user_id, notification_data):
    print("publishing notification", notification_data)
    channel = f"user_notifications_{user_id}"
    redis_client.publish(channel, json.dumps(notification_data))

def event_stream(user_id):
    pubsub = redis_client.pubsub()
    channel = f"user_notifications_{user_id}"
    pubsub.subscribe(channel)

    try:
        for message in pubsub.listen():
            print("message", message)
            yield f"data: {message}\n\n"

    except GeneratorExit:
        pubsub.unsubscribe(channel)
        print(f"Unsubscribed from {channel}")