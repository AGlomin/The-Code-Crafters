#rule based suggestions.py
def suggest_level_changes(params, level_key):
  suggestions=[]
  level=params[level_key]

  #diffficulty scaling
  if level["difficultyAttackScaling"]>0.5:
    suggestions.append(f"{level_key}:Difficulty scaling is too high.")
  if level["difficultyAttackScaling"]<0.1:
    suggestions.append(f"{level_key}: Difficulty scaling is too low (game might be too easy).")

  #Player agents
  for player in ["brawler","bomber","medic"]:
    p=level[player]

    if p["health"]<=0:
      suggestions.append(f"{level_key}:{player} health is zero or negative.")

    if p["attack"]<=0:
      suggestions.append(f"{level_key}:{player} attack is zero or negative.")

    if p["attack_range"]<=0:
      suggestions.append(f"{level_key}:{player} attack range is too low.")

    if p["move_speed"]<=0:
      suggestions.append(f"{level_key}:{player} movement speed is too low.")

  #Enemies

  for enemy in ["en0","en1","en2"]:
    e=level[enemy]

    if e["health"]<=0:
      suggestions.append(f"{level_key}: {enemy} health is zero or negative.")

    if e["attack"]<0:
      suggestions.append(f"{level_key}: {enemy} attack is invalid.")

    if e["attack_range"]<0:
      suggestions.append(f"{level_key}: {enemy} attack range is negative.")

    if e["move_speed"]<=0:
      suggestions.append(f"{level_key}: {enemy} movement speed is too low.")

#balance comparison rules
#compare player vs enemy strength
  avg_player_attack= (
    level["brawler"]["attack"]+
    level["bomber"]["attack"]+
    level["medic"]["attack"]
   ) / 3

  avg_enemy_health= (
    level["en0"]["health"]+
    level["en1"]["health"]+
    level["en2"]["health"]
) / 3

  if avg_enemy_health> avg_player_attack *5:
    suggestions.append(f"{level_key}: Enemies may take too long to kill.")

  if avg_player_attack> avg_enemy_health:
    suggestions.append(f"{level_key}: Players may be too strong compared to enemies.")

#config check
  if all(level[player]["health"]==0 for player in ["brawler", "bomber", "medic"]):
    suggestions.append(f"{level_key}: All player stats are zero- level not configured.")

  if all(level[enemy]["health"]==0 for enemy in ["en0", "en1","en2"]):
    suggestions.append(f"{level_key}: All enemy stats are zero- no challenge present.")

  return suggestions
