"""Kitchen hygiene monitoring from video: sample frames, then reason over them jointly."""
import cv2
from PIL import Image
from .llm import ask_json
from .schemas import HygieneReport

SYSTEM = ("You audit kitchen hygiene from sequential video frames. Check: hairnets/caps, gloves, "
          "handwashing, raw/cooked cross-contamination, surface cleanliness, food left uncovered, "
          "jewelry, phone use near food. Cite the frame number for each violation. Only report "
          "what is visible; do not infer.")
PROMPT = ('Frames are in time order, numbered from 1. Return JSON: {"score":0-100,'
          '"violations":[{"issue","severity":"low|medium|high","frame":int}],'
          '"good_practices":[...],"summary"}')

def sample_frames(path: str, n: int = 8) -> list[Image.Image]:
    cap = cv2.VideoCapture(path)
    total = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    if total <= 0:
        raise ValueError("Could not read video")
    frames = []
    for idx in [int(i * total / n) for i in range(n)]:
        cap.set(cv2.CAP_PROP_POS_FRAMES, idx)
        ok, frame = cap.read()
        if ok:
            frames.append(Image.fromarray(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)))
    cap.release()
    return frames

def audit_video(path: str, n_frames: int = 8) -> HygieneReport:
    frames = sample_frames(path, n_frames)
    return HygieneReport(**ask_json(SYSTEM, PROMPT, frames, max_tokens=2000))
