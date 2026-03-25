import os
import pandas as pd

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
ROOT_DIR = os.path.dirname(BASE_DIR)
AGENT_INFO_PATH = os.path.join(ROOT_DIR, "agent_information.csv")

def getPlayerAndEnemyInformation():
    players = {}
    enemies = {}

    with open(AGENT_INFO_PATH, newline="", encoding="utf-8") as csvfile:
        reader = pd.read_csv(csvfile)

    # Convert CSV rows into list of dicts
    row_data = reader.to_dict(orient="records")

    for item in row_data:
        entry = {
            "char_label": item["char_label"],
            "player_agent": bool(item["player_agent"]),
            "health": float(item["health_points"]),
            "attack": float(item["base_attack"]),
            "attack_range": float(item["attack_range"]),
            "move_speed": float(item["move_speed"]),
        }

        if entry["player_agent"]:
            players[entry["char_label"]] = entry
        else:
            enemies[entry["char_label"]] = entry

    
    return players, enemies

def suggest_level_changes(params, level_key):

  basePlayers, baseEnemies = getPlayerAndEnemyInformation()
  
  suggestions=[]
  level=params[level_key]

  #difficulty scaling
  if level["difficultyAttackScaling"]>0.5:
    suggestions.append(f"{level_key}:Difficulty scaling is too high.")
  if level["difficultyAttackScaling"]<0.1:
    suggestions.append(f"{level_key}: Difficulty scaling is too low (game might be too easy).")

  #Player agents
  for player in ["brawler","bomber","medic"]:
    p=level[player]

    if basePlayers[player]["health"] + p["health"]<=0:
      suggestions.append(f"{level_key}:{player} health is zero or negative.")

    if basePlayers[player]["attack"] + p["attack"]<=0:
      suggestions.append(f"{level_key}:{player} attack is zero or negative.")

    if basePlayers[player]["attack_range"] + p["attack_range"]<=0:
      suggestions.append(f"{level_key}:{player} attack range is too low.")

    if basePlayers[player]["move_speed"] + p["move_speed"]<=0:
      suggestions.append(f"{level_key}:{player} movement speed is too low.")

  #Enemies

  for enemy in ["en0","en1","en2"]:
    e=level[enemy]

    if baseEnemies[enemy]["health"] + e["health"]<=0:
      suggestions.append(f"{level_key}: {enemy} health is zero or negative.")

    if baseEnemies[enemy]["attack"] + e["attack"]<0:
      suggestions.append(f"{level_key}: {enemy} attack is invalid.")

    if baseEnemies[enemy]["attack_range"] + e["attack_range"]<0:
      suggestions.append(f"{level_key}: {enemy} attack range is negative.")

    if baseEnemies[enemy]["move_speed"] + e["move_speed"]<=0:
      suggestions.append(f"{level_key}: {enemy} movement speed is too low.")

  #balance comparison rules
  #compare player vs enemy strength
  #sums base and balance stats to get averages
  avg_player_attack=(
    basePlayers["brawler"]["attack"]+
    basePlayers["bomber"]["attack"]+
    basePlayers["medic"]["attack"]+
    level["brawler"]["attack"]+
    level["bomber"]["attack"]+
    level["medic"]["attack"]
  )/3

  avg_enemy_health=(
    baseEnemies["en0"]["health"]+
    baseEnemies["en1"]["health"]+
    baseEnemies["en2"]["health"]+
    level["en0"]["health"]+
    level["en1"]["health"]+
    level["en2"]["health"]
  )/3

  if avg_enemy_health> avg_player_attack *5:
    suggestions.append(f"{level_key}: Enemies may take too long to kill.")

  if avg_player_attack> avg_enemy_health:
    suggestions.append(f"{level_key}: Players may be too strong compared to enemies.")

  #config check
  if all((basePlayers[player]["health"] + level[player]["health"]) == 0 for player in ["brawler", "bomber", "medic"]):
    suggestions.append(f"{level_key}: All player stats (base + level) are zero - level not configured.")

  if all((baseEnemies[enemy]["health"] + level[enemy]["health"]) == 0 for enemy in ["en0", "en1","en2"]):
    suggestions.append(f"{level_key}: All enemy stats (base + level) are zero - no challenge present.")

  return suggestions

