import os
import sys
import json
import asyncio
from datetime import date

import aio_pika
from dotenv import load_dotenv
from sqlalchemy.orm import Session

from database import SessionLocal, engine, Base
from models import DailySummary

env_file = ".env" if os.getenv("DOCKER_ENV") == "true" else ".env.local"
load_dotenv(env_file)

RABBITMQ_URL = os.getenv("RABBITMQ_URL", "amqp://guest:guest@localhost:5672/")
EXCHANGE_NAME = "task_events"
QUEUE_NAME = "analytics_summary"

Base.metadata.create_all(bind=engine)


def process_event(body: dict, db_session=None):
    event = body.get("event")
    user_id = body.get("user_id")
    today = date.today()

    db = db_session or SessionLocal()
    own_session = db_session is None
    try:
        summary = (
            db.query(DailySummary)
            .filter(DailySummary.date == today, DailySummary.user_id == user_id)
            .first()
        )
        if not summary:
            summary = DailySummary(date=today, user_id=user_id, total_created=0, total_completed=0)
            db.add(summary)

        if event == "task.created":
            summary.total_created += 1
        elif event == "task.completed":
            summary.total_completed += 1

        db.commit()
        print(f"Processed {event} for user {user_id}")
        sys.stdout.flush()
    except Exception as e:
        print(f"Error processing event: {e}")
        if own_session:
            db.rollback()
    finally:
        if own_session:
            db.close()


async def main():
    connection = await aio_pika.connect_robust(RABBITMQ_URL)
    async with connection:
        channel = await connection.channel()
        exchange = await channel.declare_exchange(EXCHANGE_NAME, aio_pika.ExchangeType.FANOUT, durable=True)
        queue = await channel.declare_queue(QUEUE_NAME, durable=True)
        await queue.bind(exchange)

        print(f"Listening for events on queue '{QUEUE_NAME}'...")
        sys.stdout.flush()

        async with queue.iterator() as queue_iter:
            async for message in queue_iter:
                async with message.process():
                    body = json.loads(message.body.decode())
                    process_event(body)


if __name__ == "__main__":
    asyncio.run(main())
