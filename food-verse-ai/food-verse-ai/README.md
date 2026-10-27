# Food Verse AI

A modular, multimodal food intelligence platform. Computer vision, video analysis and LLM reasoning
in one Streamlit app.

| Module | File | What it does |
|---|---|---|
| Food recognition | `foodverse/recognition.py` | Photo to items, portions, calories, macros |
| Freshness | `foodverse/freshness.py` | Visual spoilage signs with a score and advice |
| Hygiene monitor | `foodverse/hygiene.py` | Samples video frames, flags violations by frame |
| Cooking assistant | `foodverse/cooking.py` | Recipes from your ingredients; "is it ready?" photo coach |
| Nutrition planner | `foodverse/nutrition.py` | Mifflin-St Jeor targets + constrained meal plans |

## Architecture
All model calls go through `foodverse/llm.py`, so swapping the model or provider touches one file.
Outputs are validated with Pydantic schemas. Calorie totals and macro targets are computed in code,
not trusted from the model.

## Run
```bash
pip install -r requirements.txt
export ANTHROPIC_API_KEY=...      # see .env.example
streamlit run app.py
pytest                            # offline tests
```

## Transparency and limits
- Calorie and macro values are estimates from images. Freshness checks are visual only and never
  certify food as safe. Hygiene audits are an aid, not a replacement for inspection.
- Nothing is stored; your profile lives only in the session.
- Not medical advice.

## Extending
Add a module in `foodverse/`, a schema in `schemas.py`, and a tab in `app.py`.
Roadmap: barcode and label OCR, meal history, a REST API (FastAPI), live camera streams.

## License
MIT
