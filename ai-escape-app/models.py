from sqlalchemy import Column, Integer, String, DateTime, JSON, func
from sqlalchemy.orm import declarative_base


Base = declarative_base()


class GameSession(Base):
    __tablename__ = "game_sessions"

    id = Column(Integer, primary_key=True)
    player_id = Column(String, nullable=False)
    current_room = Column(String, default="start_room")
    current_room_description = Column(String)

    inventory = Column(JSON, default=[])
    game_history = Column(JSON, default=[])
    narrative_state = Column(JSON, default={})
    narrative_archetype = Column(String)

    puzzle_state = Column(JSON, default={})
    start_time = Column(DateTime(timezone=True), default=func.now())
    last_updated = Column(
        DateTime(timezone=True), default=func.now(), onupdate=func.now()
    )
    theme = Column(String, default="mystery")
    location = Column(String, default="mansion")
    difficulty = Column(String, default="medium")

    def __repr__(self):
        return f"<GameSession(id={self.id}, player_id='{self.player_id}', current_room='{self.current_room}')>"
