import os
import json
import sys
from datetime import datetime, timezone
from typing import Optional

import aio_pika
from dotenv import load_dotenv

EXCHANGE_NAME = "task_events"

_connection = None
_channel = None


def get_rabbitmq_url() -> str:
    env_file = ".env" if os.getenv("DOCKER_ENV") == "true" else ".env.local"
    load_dotenv(env_file)
    return os.getenv("RABBITMQ_URL", "amqp://guest:guest@localhost:5672/")


async def get_connection():
    global _connection
    if _connection is None or _connection.is_closed:
        url = get_rabbitmq_url()
        print(f"Connecting to RabbitMQ at {url}")
        _connection = await aio_pika.connect_robust(url)
        print("Connected to RabbitMQ")
    return _connection


async def get_channel():
    global _channel, _connection
    connection = await get_connection()
    if _channel is None or _channel.is_closed:
        _channel = await connection.channel()
    return _channel


async def publish_event(event_type: str, user_id: int, task_id: int, category: Optional[str]):
    message = {
        "event": event_type,
        "user_id": user_id,
        "task_id": task_id,
        "category": category,
        "timestamp": datetime.now(timezone.utc).isoformat(),
    }
    try:
        channel = await get_channel()
        exchange = await channel.declare_exchange(
            EXCHANGE_NAME, aio_pika.ExchangeType.FANOUT, durable=True
        )
        await exchange.publish(
            aio_pika.Message(
                body=json.dumps(message).encode(),
                delivery_mode=aio_pika.DeliveryMode.PERSISTENT,
            ),
            routing_key="",
        )
        print(f"Published {event_type} for task {task_id}")
        sys.stdout.flush()
    except Exception as e:
        global _connection, _channel
        _connection = None
        _channel = None
        print(f"Failed to publish {event_type} for task {task_id}: {e}", file=sys.stderr)
        sys.stderr.flush()
