EVENT_TYPES = {
    #session lifecycle
    "session_start",
    "session_end",

    #level lifecycle
    "level_start",
    "level_complete",

    #stage lifecycle
    "stage_start",
    "stage_complete",
    "stage_fail",
    "stage_retry",

    #turn lifecycle
    "turn_start",
    "turn_end",

    #player actions
    "character_move",
    "character_attack",
    "character_heal",
    "payer_damage", #added during second sprint, track damage recieved
    "player_death", #added during second sprint, track player death

    #enemy actions
    "enemy_move",
    "enemy_attack",
    "enemy_damage", #added during second sprint, track damage dealth to enemies

    #configuration
    "settings_change",

    #player closes game to quit
    "quit"
}
