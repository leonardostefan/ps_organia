from sqlalchemy import Column, DateTime, Integer, String, Text
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class Review(Base):
    __tablename__ = "reviews"

    id = Column(Integer, primary_key=True, index=True)
    costumer_name = Column(Text, nullable=False)
    text = Column(Text, nullable=False)
    # "+" =  Positivo ; "0" = Neutro ; "-" = negativo ; Null = não validado/calculado
    sentiment = Column(String(1), nullable=True)
    created_at = Column(DateTime, nullable=False)

    def to_response(self):

        return {
            "id": self.id,
            "costumer_name": self.costumer_name,
            "text": self.text,
            "sentiment": self.sentiment,
            "created_at": str(self.created_at),
        }


"""
CREATE TABLE reviews (
    id SERIAL PRIMARY KEY,
    text TEXT NOT NULL,
    sentiment character (1) NULL,
    created_at TIMESTAMP NOT NULL
);
"""
