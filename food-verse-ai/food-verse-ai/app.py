import json, os, tempfile
import streamlit as st
from PIL import Image
from foodverse import recognition, freshness, hygiene, cooking, nutrition
from foodverse.schemas import UserProfile

st.set_page_config(page_title="Food Verse AI", page_icon="🥗", layout="wide")
st.title("Food Verse AI")
st.caption("Multimodal food intelligence: recognition, freshness, hygiene, cooking, nutrition.")

if not os.getenv("ANTHROPIC_API_KEY"):
    st.error("Set ANTHROPIC_API_KEY in your environment, then restart the app.")
    st.stop()

with st.sidebar:
    st.header("Your profile")
    p = UserProfile(
        age=st.number_input("Age", 10, 100, 30),
        sex=st.selectbox("Sex", ["female", "male"]),
        height_cm=st.number_input("Height (cm)", 100, 230, 165),
        weight_kg=st.number_input("Weight (kg)", 30, 250, 65),
        activity=st.selectbox("Activity", list(nutrition.ACTIVITY), index=2),
        goal=st.selectbox("Goal", ["lose", "maintain", "gain"], index=1),
        diet=st.selectbox("Diet", ["none", "vegetarian", "vegan", "keto", "halal", "jain"]),
        allergies=[a.strip() for a in st.text_input("Allergies (comma separated)").split(",") if a.strip()],
    )
    st.caption("Stays in this session. Nothing is stored. Estimates are not medical advice.")

def img_input(key):
    f = st.file_uploader("Upload a photo", type=["jpg", "jpeg", "png"], key=key)
    return Image.open(f) if f else None

tabs = st.tabs(["Food recognition", "Freshness", "Hygiene monitor", "Cooking assistant", "Nutrition plan"])

with tabs[0]:
    img = img_input("rec")
    if img and st.button("Analyze meal"):
        st.image(img, width=360)
        with st.spinner("Analyzing..."):
            r = recognition.analyze_food(img)
        st.metric("Estimated calories", r.total_calories)
        st.dataframe([i.model_dump() for i in r.items], use_container_width=True)
        st.caption(f"Confidence: {r.confidence}. {r.notes}")

with tabs[1]:
    img = img_input("fresh")
    if img and st.button("Check freshness"):
        st.image(img, width=360)
        with st.spinner("Inspecting..."):
            r = freshness.check_freshness(img)
        st.subheader(f"{r.food}: {r.status.replace('_', ' ')} ({r.score}/100)")
        st.write("Signs observed:", r.signs)
        st.info(r.advice)
        st.caption("Visual check only. When in doubt, throw it out.")

with tabs[2]:
    v = st.file_uploader("Upload kitchen video", type=["mp4", "mov", "avi"])
    n = st.slider("Frames to analyze", 4, 12, 8)
    if v and st.button("Audit hygiene"):
        with tempfile.NamedTemporaryFile(suffix=".mp4", delete=False) as tmp:
            tmp.write(v.read())
        with st.spinner("Sampling frames and auditing..."):
            r = hygiene.audit_video(tmp.name, n)
        os.unlink(tmp.name)
        st.metric("Hygiene score", f"{r.score}/100")
        st.write(r.summary)
        for x in r.violations:
            st.warning(f"[{x.get('severity')}] frame {x.get('frame')}: {x.get('issue')}")
        for g in r.good_practices:
            st.success(g)

with tabs[3]:
    txt = st.text_input("Ingredients you have (or upload a photo)")
    img = img_input("cook")
    mins = st.slider("Minutes available", 10, 90, 30)
    if (txt or img) and st.button("Suggest recipes"):
        with st.spinner("Cooking up ideas..."):
            st.session_state["recipes"] = cooking.suggest_recipes(img, txt, p, mins)
    rec = st.session_state.get("recipes")
    if rec:
        st.write("Detected:", rec.get("detected_ingredients"))
        for r in rec.get("recipes", []):
            with st.expander(f"{r['name']} ({r['time_min']} min)"):
                st.write("Missing:", r.get("missing_ingredients") or "nothing")
                st.write("\n".join(f"{i+1}. {s}" for i, s in enumerate(r["steps"])))
    st.divider()
    step = st.text_input("Current recipe step")
    shot = img_input("coach")
    if step and shot and st.button("Is it ready?"):
        c = cooking.coach_step(step, shot)
        st.write(("Ready. " if c.get("ready") else "Not yet. ") + c.get("observation", ""))
        st.info(c.get("next_action", ""))

with tabs[4]:
    t = nutrition.daily_targets(p)
    cols = st.columns(4)
    for c, (k, val) in zip(cols, t.items()):
        c.metric(k.replace("_", " "), val)
    days = st.slider("Days", 1, 7, 3)
    if st.button("Generate meal plan"):
        with st.spinner("Planning..."):
            plan = nutrition.meal_plan(p, days)["plan"]
        for d in plan.get("days", []):
            with st.expander(f"Day {d['day']} ({d.get('total_calories')} kcal)", expanded=d["day"] == 1):
                st.table(d["meals"])
        st.write("Shopping list:", plan.get("shopping_list"))
