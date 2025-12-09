from sqlalchemy import (
    Column,
    Integer,
    String,
    DateTime,
    JSON,
    func,
    ForeignKey,
)
from sqlalchemy.orm import declarative_base, relationship
import datetime


Base = declarative_base()


class GameSession(Base):
    __tablename__ = "game_sessions"

    id = Column(Integer, primary_key=True)
    player_id = Column(String, nullable=False)
    current_room = Column(String, default="start_room")
    current_room_description = Column(String)

    inventory = Column(JSON, default=lambda: [])
    game_history = Column(JSON, default=lambda: [])
    narrative_state = Column(JSON, default=lambda: {})
    narrative_archetype = Column(String)

    puzzle_state = Column(JSON, default=lambda: {})
    puzzle_dependencies = Column(JSON, default=lambda: [])
    start_time = Column(DateTime(timezone=True), default=func.now())
    last_updated = Column(
        DateTime(timezone=True), default=func.now(), onupdate=func.now()
    )
    theme = Column(String, default="mystery")
    location = Column(String, default="mansion")
    difficulty = Column(String, default="medium")

    # Relationship to saved games
    saved_games = relationship("SavedGame", back_populates="game_session")

    def to_dict(self):
        return {
            "id": self.id,
            "player_id": self.player_id,
            "current_room": self.current_room,
            "current_room_description": self.current_room_description,
            "inventory": self.inventory,
            "game_history": self.game_history,
            "narrative_state": self.narrative_state,
            "narrative_archetype": self.narrative_archetype,
            "puzzle_state": self.puzzle_state,
            "puzzle_dependencies": self.puzzle_dependencies,
            "start_time": self.start_time.isoformat() if self.start_time else None,
            "last_updated": self.last_updated.isoformat() if self.last_updated else None,
            "theme": self.theme,
            "location": self.location,
            "difficulty": self.difficulty,
        }

    def __repr__(self):
        return f"<GameSession(id={self.id}, player_id='{self.player_id}', current_room='{self.current_room}')>"


class SavedGame(Base):
    __tablename__ = "saved_games"

    id = Column(Integer, primary_key=True)
    player_id = Column(String, nullable=False)
    session_id = Column(Integer, ForeignKey("game_sessions.id"), nullable=False)
    save_name = Column(String, nullable=False)
    saved_at = Column(DateTime(timezone=True), default=func.now())
    game_state = Column(JSON, nullable=False)

    game_session = relationship("GameSession", back_populates="saved_games")

    def to_dict(self):
        return {
            "id": self.id,
            "player_id": self.player_id,
            "session_id": self.session_id,
            "save_name": self.save_name,
            "saved_at": self.saved_at.isoformat(),
            "game_state": self.game_state,
        }

    def __repr__(self):
        return f"<SavedGame(id={self.id}, session_id={self.session_id}, save_name='{self.save_name}')>"


class PlayerSettings(Base):
    __tablename__ = "player_settings"

    player_id = Column(String, primary_key=True, nullable=False)
    settings = Column(JSON, default=lambda: {})
    last_updated = Column(
        DateTime(timezone=True), default=func.now(), onupdate=func.now()
    )

    def to_dict(self):
        return {
            "player_id": self.player_id,
            "settings": self.settings,
            "last_updated": self.last_updated.isoformat(),
        }

    def __repr__(self):
        return f"<PlayerSettings(player_id='{self.player_id}')>"
