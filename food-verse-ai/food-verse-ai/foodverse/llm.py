"""Single gateway to the vision-language model. All modules go through here."""
import base64, io, json, os, re
import anthropic
from PIL import Image

MODEL = os.getenv("FOODVERSE_MODEL", "claude-sonnet-4-6")
_client = None

def client():
    global _client
    if _client is None:
        _client = anthropic.Anthropic()  # reads ANTHROPIC_API_KEY
    return _client

def encode_image(img: Image.Image, max_side: int = 1280) -> dict:
    img = img.convert("RGB")
    img.thumbnail((max_side, max_side))
    buf = io.BytesIO()
    img.save(buf, "JPEG", quality=85)
    data = base64.b64encode(buf.getvalue()).decode()
    return {"type": "image", "source": {"type": "base64", "media_type": "image/jpeg", "data": data}}

def parse_json(text: str) -> dict:
    text = re.sub(r"```(?:json)?", "", text).strip()
    start, end = text.find("{"), text.rfind("}")
    if start == -1 or end == -1:
        raise ValueError("Model returned no JSON object")
    return json.loads(text[start:end + 1])

def ask_json(system: str, prompt: str, images: list | None = None, max_tokens: int = 1500) -> dict:
    content = [encode_image(i) for i in (images or [])] + [{"type": "text", "text": prompt}]
    resp = client().messages.create(
        model=MODEL, max_tokens=max_tokens,
        system=system + "\nRespond with a single valid JSON object only, no prose.",
        messages=[{"role": "user", "content": content}],
    )
    return parse_json(resp.content[0].text)
