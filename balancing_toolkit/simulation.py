import json #to load params
from suggestions import suggest_level_changes

#prevent sim from crashing due to typos
def safe_get(level, key, default=0):
    return level.get(key, default)

#simple sim
def simulate_level(level_data):
    player_attack=(
        safe_get(level_data["brawler"], "attack")+
        safe_get(level_data["bomber"], "attack")+
        safe_get(level_data["medic"], "attack")
    )
    enemy_health=(
        safe_get(level_data["en0"], "health")+
        safe_get(level_data["en1"], "health")+
        safe_get(level_data["en2"], "health")
    )
    if player_attack<=0:
        return float("inf")

    turns=enemy_health/player_attack
    return max(1, int(turns))


def run_simulations(params):
    results={}

    for level_key, level_data in params.items():
        print(f"\n=== {level_key.upper()}===")
        suggestions=suggest_level_changes(params,level_key)
        turns=simulate_level(level_data)
        results[level_key]={
            "turns_to_win":turns,
            "suggestions":suggestions
        }
        #prints results
        print(f"Estimated turns to defeat enemies: {turns}")
        print("suggestions:")
        if suggestions:
            for s in suggestions:
                print("-",s)
        else:
            print("No Issues detected.")
    return results

if __name__=="__main__":
    try:
        with open("parameters.json", "r") as f:
            params=json.load(f)
    except:
        print("Could not load parameters.json".)
        exit()
    run_simulations(params)

