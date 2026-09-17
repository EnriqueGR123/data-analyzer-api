from sqlalchemy import Integer, String
from sqlalchemy.orm import Mapped, mapped_column
from datetime import datetime
from app.db.dependencies import Base

class Dataset(Base):
    __tablename__ = 'Datasets'
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    filename:Mapped[str] = mapped_column(String(255), nullable=False)
    rows:Mapped[int] = mapped_column(Integer,nullable=False)
    columns:Mapped[int] = mapped_column(Integer, nullable=False)
    created_at:Mapped[datetime] = mapped_column(default=datetime.utcnow, nullable=False)




