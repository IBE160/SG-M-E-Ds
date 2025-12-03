from datetime import datetime, timezone
from sqlalchemy.orm import Session
from models import GameSession

def create_game_session(db_session: Session, player_id: str, theme: str = "mystery", location: str = "mansion", difficulty: str = "medium") -> GameSession:
    """
    Initializes and stores a new GameSession in the database.
    """
    new_session = GameSession(
        player_id=player_id,
        theme=theme,
        location=location,
        difficulty=difficulty,
        start_time=datetime.now(timezone.utc),
        last_updated=datetime.now(timezone.utc)
    )
    db_session.add(new_session)
    db_session.commit()
    db_session.refresh(new_session)
    return new_session

def get_game_session(db_session: Session, session_id: int) -> GameSession | None:
    """
    Retrieves a GameSession by its ID.
    """
    return db_session.query(GameSession).filter(GameSession.id == session_id).first()

def update_game_session(db_session: Session, session_id: int, **kwargs) -> GameSession | None:
    """
    Updates an existing GameSession with the given keyword arguments.
    """
    game_session = get_game_session(db_session, session_id)
    if game_session:
        for key, value in kwargs.items():
            if hasattr(game_session, key):
                setattr(game_session, key, value)
        game_session.last_updated = datetime.now(timezone.utc)
        db_session.commit()
        db_session.refresh(game_session)
    return game_session

def delete_game_session(db_session: Session, session_id: int) -> bool:
    """
    Deletes a GameSession by its ID.
    """
    game_session = get_game_session(db_session, session_id)
    if game_session:
        db_session.delete(game_session)
        db_session.commit()
        return True
    return False

def update_player_inventory(db_session: Session, session_id: int, item: str, action: str) -> GameSession | None:
    """
    Adds or removes an item from the player's inventory.
    Action can be 'add' or 'remove'.
    """
    game_session = get_game_session(db_session, session_id)
    if not game_session:
        return None

    inventory = list(game_session.inventory) # Create a mutable copy
    
    if action == 'add':
        if item not in inventory:
            inventory.append(item)
    elif action == 'remove':
        if item in inventory:
            inventory.remove(item)
    else:
        # Invalid action, return the session without updating
        return game_session
    
    game_session.inventory = inventory # Reassign the modified list
    game_session.last_updated = datetime.now(timezone.utc)
    db_session.commit()
    db_session.refresh(game_session)
    return game_session
