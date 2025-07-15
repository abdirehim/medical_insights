from sqlalchemy import Column, Integer, String, Date, DateTime, Boolean, ForeignKey, Float, Text, ARRAY
from sqlalchemy.orm import declarative_base, relationship

Base = declarative_base()

class DimChannel(Base):
    __tablename__ = 'dim_channels'
    channel_sk = Column(String, primary_key=True, index=True)
    channel_name = Column(String, unique=True, nullable=False)
    messages = relationship('FctMessage', back_populates='channel')

class DimDate(Base):
    __tablename__ = 'dim_dates'
    date_day = Column(Date, primary_key=True, index=True)
    year = Column(Integer)
    month = Column(Integer)
    day_of_month = Column(Integer)
    # Add other date attributes as needed
    messages = relationship('FctMessage', back_populates='date')

class FctMessage(Base):
    __tablename__ = 'fct_messages'
    message_pk = Column(Integer, primary_key=True, index=True)
    message_id = Column(Integer, nullable=False)
    message_text = Column(Text)
    message_length = Column(Integer)
    message_date = Column(DateTime)
    views_count = Column(Integer)
    forwards_count = Column(Integer)
    replies_count = Column(Integer)
    has_reactions = Column(Boolean)
    has_photo = Column(Boolean)
    product_mentions = Column(ARRAY(String))
    scraped_at = Column(DateTime)
    channel_sk = Column(String, ForeignKey('dim_channels.channel_sk'), nullable=False)
    message_date_key = Column(Date, ForeignKey('dim_dates.date_day'), nullable=False)

    channel = relationship('DimChannel', back_populates='messages')
    date = relationship('DimDate', back_populates='messages')
    detections = relationship('FctImageDetection', back_populates='message')

class FctImageDetection(Base):
    __tablename__ = 'fct_image_detections'
    detection_pk = Column(String, primary_key=True, index=True)
    message_id = Column(Integer, ForeignKey('fct_messages.message_id'), nullable=False)
    image_id = Column(String)
    object_class = Column(String, nullable=False)
    confidence_score = Column(Float)
    detection_time = Column(DateTime)

    message = relationship('FctMessage', back_populates='detections') 