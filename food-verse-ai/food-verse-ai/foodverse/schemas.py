from pydantic import BaseModel, Field

class FoodItem(BaseModel):
    name: str
    portion: str = ""
    calories: float = 0
    protein_g: float = 0
    carbs_g: float = 0
    fat_g: float = 0

class FoodAnalysis(BaseModel):
    items: list[FoodItem] = Field(default_factory=list)
    total_calories: float = 0
    confidence: str = "medium"
    notes: str = ""

class Freshness(BaseModel):
    food: str = ""
    status: str = "unknown"       # fresh | use_soon | spoiled | unknown
    score: int = 0                # 0-100
    signs: list[str] = Field(default_factory=list)
    advice: str = ""

class HygieneReport(BaseModel):
    score: int = 0                # 0-100
    violations: list[dict] = Field(default_factory=list)  # {issue, severity, frame}
    good_practices: list[str] = Field(default_factory=list)
    summary: str = ""

class UserProfile(BaseModel):
    age: int = 30
    sex: str = "female"
    height_cm: float = 165
    weight_kg: float = 65
    activity: str = "moderate"    # sedentary | light | moderate | active
    goal: str = "maintain"        # lose | maintain | gain
    diet: str = "none"
    allergies: list[str] = Field(default_factory=list)
