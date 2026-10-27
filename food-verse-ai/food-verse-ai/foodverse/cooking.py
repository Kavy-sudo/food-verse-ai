"""Context-aware cooking assistant: sees what you have, adapts to your diet."""
from PIL import Image
from .llm import ask_json
from .schemas import UserProfile

SYSTEM = "You are a practical home-cooking coach. Respect allergies strictly."

def suggest_recipes(ingredients_photo: Image.Image | None, ingredients_text: str,
                    profile: UserProfile, minutes: int = 30) -> dict:
    prompt = (f"Ingredients (text): {ingredients_text or 'see image'}\n"
              f"Diet: {profile.diet}. Allergies (never include): {profile.allergies}. "
              f"Time available: {minutes} min.\n"
              'Return JSON: {"detected_ingredients":[...],"recipes":[{"name","time_min",'
              '"missing_ingredients":[...],"steps":[...]}]} with 3 recipes.')
    return ask_json(SYSTEM, prompt, [ingredients_photo] if ingredients_photo else None, 2500)

def coach_step(step: str, photo: Image.Image, question: str = "") -> dict:
    """Look at the pan/pot photo and say whether the current step is done."""
    prompt = (f"Recipe step: {step}\nUser question: {question or 'Is this ready?'}\n"
              'Return JSON: {"ready":bool,"observation","next_action"}')
    return ask_json(SYSTEM, prompt, [photo])
