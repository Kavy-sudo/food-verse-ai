"""Food recognition and nutrition estimation from a photo."""
from PIL import Image
from .llm import ask_json
from .schemas import FoodAnalysis

SYSTEM = ("You are a nutrition analyst. Identify every distinct food in the image, estimate portion "
          "size and macros. Be honest about uncertainty; these are estimates.")
PROMPT = ('Return JSON: {"items":[{"name","portion","calories","protein_g","carbs_g","fat_g"}],'
          '"total_calories","confidence":"low|medium|high","notes"}')

def analyze_food(image: Image.Image) -> FoodAnalysis:
    result = FoodAnalysis(**ask_json(SYSTEM, PROMPT, [image]))
    # Recompute total from items so the number is always internally consistent.
    result.total_calories = round(sum(i.calories for i in result.items), 1)
    return result
