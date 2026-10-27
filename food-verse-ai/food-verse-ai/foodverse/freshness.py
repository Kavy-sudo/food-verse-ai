"""Visual freshness assessment with explicit, checkable signs."""
from PIL import Image
from .llm import ask_json
from .schemas import Freshness

SYSTEM = ("You assess food freshness from images. List the specific visual signs you rely on "
          "(color, mold, texture, wilting, discoloration). You cannot smell or taste, so when "
          "evidence is weak say 'unknown' and recommend caution. Never certify food as safe.")
PROMPT = ('Return JSON: {"food","status":"fresh|use_soon|spoiled|unknown","score":0-100,'
          '"signs":[...],"advice"}')

def check_freshness(image: Image.Image) -> Freshness:
    return Freshness(**ask_json(SYSTEM, PROMPT, [image]))
