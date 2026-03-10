EVENT_TYPES = {
    # session lifecycle
    "session_start",
    "session_end",

    # level lifecycle
    "level_start",
    "level_complete",

    # stage lifecycle
    "stage_start",
    "stage_complete",
    "stage_fail",
    "stage_retry",

    # turn lifecycle
    "turn_start",
    "turn_end",

    # player actions
    "character_move",
    "character_attack",
    "character_heal",
    "player_damage",
    "player_death",

    # enemy actions
    "enemy_move",
    "enemy_attack",
    "enemy_damage",

    # economy / progression
    "resource_gain",
    "resource_spend",
    "item_pickup",

    # boss mechanics
    "boss_start",
    "boss_fail",
    "boss_win",

    # configuration
    "settings_change",

    # player quits game
    "quit"
}