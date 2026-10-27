from foodverse.llm import parse_json
from foodverse.nutrition import daily_targets
from foodverse.schemas import UserProfile

def test_parse_json_strips_fences():
    assert parse_json('```json\n{"a": 1}\n```') == {"a": 1}

def test_targets_goal_ordering():
    lose = daily_targets(UserProfile(goal="lose"))["calories"]
    gain = daily_targets(UserProfile(goal="gain"))["calories"]
    assert lose < gain

def test_macros_add_up():
    t = daily_targets(UserProfile())
    kcal = t["protein_g"] * 4 + t["carbs_g"] * 4 + t["fat_g"] * 9
    assert abs(kcal - t["calories"]) < 15
