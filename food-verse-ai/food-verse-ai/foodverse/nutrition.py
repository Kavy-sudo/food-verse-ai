"""Deterministic targets (Mifflin-St Jeor) + LLM-generated meal plan constrained by them."""
from .llm import ask_json
from .schemas import UserProfile

ACTIVITY = {"sedentary": 1.2, "light": 1.375, "moderate": 1.55, "active": 1.725}
GOAL_ADJ = {"lose": -500, "maintain": 0, "gain": 300}

def daily_targets(p: UserProfile) -> dict:
    bmr = 10 * p.weight_kg + 6.25 * p.height_cm - 5 * p.age + (5 if p.sex.lower() == "male" else -161)
    kcal = round(bmr * ACTIVITY[p.activity] + GOAL_ADJ[p.goal])
    protein = round(p.weight_kg * (1.8 if p.goal != "maintain" else 1.4))
    fat = round(kcal * 0.28 / 9)
    carbs = round((kcal - protein * 4 - fat * 9) / 4)
    return {"calories": kcal, "protein_g": protein, "carbs_g": carbs, "fat_g": fat}

def meal_plan(p: UserProfile, days: int = 3) -> dict:
    t = daily_targets(p)
    prompt = (f"Create a {days}-day meal plan hitting about {t}. Diet: {p.diet}. "
              f"Allergies (never include): {p.allergies}.\n"
              'Return JSON: {"days":[{"day":1,"meals":[{"name","dish","calories","protein_g"}],'
              '"total_calories"}],"shopping_list":[...]}')
    plan = ask_json("You are a registered-dietitian-style planner. Not medical advice.", prompt, max_tokens=3000)
    return {"targets": t, "plan": plan}
