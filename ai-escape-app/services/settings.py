from sqlalchemy.orm import Session
from sqlalchemy.orm.attributes import flag_modified
from models import PlayerSettings
from data.game_settings import GAME_SETTINGS # Assuming GAME_SETTINGS defines default values and validation rules

def get_player_settings(db_session: Session, player_id: str) -> PlayerSettings:
    """
    Retrieves a player's settings from the database. If no settings exist,
    creates a new entry with default values from GAME_SETTINGS.
    """
    player_settings = db_session.query(PlayerSettings).filter(PlayerSettings.player_id == player_id).first()

    if not player_settings:
        # Create default settings from GAME_SETTINGS
        default_settings = {key: setting["default"] for key, setting in GAME_SETTINGS.items()}
        player_settings = PlayerSettings(player_id=player_id, settings=default_settings)
        db_session.add(player_settings)
        db_session.commit()
        db_session.refresh(player_settings)
    
    return player_settings

def update_player_settings(db_session: Session, player_id: str, new_settings: dict) -> PlayerSettings | None:
    """
    Updates a player's settings in the database.
    """
    player_settings = get_player_settings(db_session, player_id) # Ensures defaults are loaded if new player
    if not player_settings: # Should not happen with get_player_settings creating defaults
        return None

    # Validate and apply new settings
    for key, value in new_settings.items():
        if key in GAME_SETTINGS: # Only update known settings
            # Basic type/range validation could go here
            if GAME_SETTINGS[key]["type"] == "slider":
                if isinstance(value, int) and GAME_SETTINGS[key]["min"] <= value <= GAME_SETTINGS[key]["max"]:
                    player_settings.settings[key] = value
                else:
                    print(f"Warning: Invalid value for slider setting '{key}': {value}")
            elif GAME_SETTINGS[key]["type"] == "select":
                valid_options = [opt["value"] for opt in GAME_SETTINGS[key]["options"]]
                if value in valid_options:
                    player_settings.settings[key] = value
                else:
                    print(f"Warning: Invalid value for select setting '{key}': {value}")
            else: # For other types not yet defined or directly assigned
                player_settings.settings[key] = value
        else:
            print(f"Warning: Attempted to update unknown setting '{key}'")
            
    flag_modified(player_settings, "settings") # Explicitly flag JSON field as modified
    db_session.commit()
    db_session.refresh(player_settings)
    return player_settings
