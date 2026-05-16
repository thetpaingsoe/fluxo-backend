from sqlalchemy import Column, Integer, Date, UniqueConstraint
from database import Base


class DailySummary(Base):
    __tablename__ = "daily_summaries"

    id = Column(Integer, primary_key=True, index=True)
    date = Column(Date, nullable=False)
    user_id = Column(Integer, nullable=False)
    total_created = Column(Integer, default=0)
    total_completed = Column(Integer, default=0)

    __table_args__ = (UniqueConstraint("date", "user_id", name="uq_date_user"),)
