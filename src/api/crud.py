# Placeholder for CRUD functions
# Implement database query functions here for endpoints

from sqlalchemy.orm import Session
from sqlalchemy import func, cast, Date, text
from .database import SessionLocal
from .models import FctMessage, DimChannel

def get_top_products(limit: int = 10):
    session = SessionLocal()
    try:
        sql = text("""
            SELECT unnest(product_mentions) AS product, COUNT(*) AS mention_count
            FROM fct_messages
            WHERE product_mentions IS NOT NULL
            GROUP BY product
            ORDER BY mention_count DESC
            LIMIT :limit
        """)
        result = session.execute(sql, {"limit": limit}).fetchall()
        return [{"product": row[0], "mention_count": row[1]} for row in result]
    finally:
        session.close()

def get_channel_activity(channel_name: str, period: str = "daily"):
    session = SessionLocal()
    try:
        query = session.query(
            cast(FctMessage.message_date, Date).label('date'),
            func.count(FctMessage.message_pk).label('message_count')
        ).join(DimChannel, FctMessage.channel_sk == DimChannel.channel_sk)
        query = query.filter(DimChannel.channel_name == channel_name)
        if period == "weekly":
            query = query.group_by(func.date_trunc('week', FctMessage.message_date))
            query = query.with_entities(func.date_trunc('week', FctMessage.message_date).label('week'), func.count(FctMessage.message_pk).label('message_count'))
        else:
            query = query.group_by(cast(FctMessage.message_date, Date))
        results = query.order_by('date' if period == 'daily' else 'week').all()
        if period == "weekly":
            return [{"week": str(row[0]), "message_count": row[1]} for row in results]
        else:
            return [{"date": str(row[0]), "message_count": row[1]} for row in results]
    finally:
        session.close()

def search_messages(query: str):
    session = SessionLocal()
    try:
        results = session.query(FctMessage).filter(FctMessage.message_text.ilike(f"%{query}%")).all()
        return [{
            "message_id": m.message_id,
            "message_text": m.message_text,
            "channel_sk": m.channel_sk,
            "message_date": m.message_date.isoformat() if m.message_date else None
        } for m in results]
    finally:
        session.close() 