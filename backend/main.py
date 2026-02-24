import json
import os
import random
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from dotenv import load_dotenv

load_dotenv()

app = FastAPI(title="Plotlyst API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://127.0.0.1:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class StoryRequest(BaseModel):
    genre: str
    characters: str
    setting: str
    theme: str


class StoryResponse(BaseModel):
    story: str
    title: str
    characters: list[str]
    world: str


# ---------- Template-based fallback generator ----------

OPENERS = {
    "Fantasy": [
        "In an age when magic still breathed through the roots of ancient trees,",
        "Beyond the silver mists of the Enchanted Vale,",
        "When the old gods slumbered and dragons ruled the skies,",
    ],
    "Sci-Fi": [
        "Three thousand light-years from the dying sun of Earth,",
        "In the cold silence between stars, where no voice carries,",
        "As the colony ship breached the outer rim of the known galaxy,",
    ],
    "Mystery": [
        "The fog had settled low over the city the night the body was found,",
        "Nobody noticed the locked door until the screaming stopped,",
        "It began with a letter that arrived without a postmark,",
    ],
    "Romance": [
        "She had sworn off love after the last disaster, yet fate had other plans,",
        "Their eyes met across a crowded marketplace in the heart of the old city,",
        "It was the wrong train, the wrong seat, and undeniably the right person,",
    ],
    "Horror": [
        "The house at the edge of the moor had been empty for thirty years — or so they believed,",
        "Nobody in the village spoke of what happened after dark,",
        "The scratching started on the first night of the new moon,",
    ],
    "Adventure": [
        "The map had been hidden inside the old captain's boot for a century,",
        "They said no one had ever crossed the Crimson Desert and returned,",
        "The expedition set out at dawn with three weeks of rations and one impossible goal,",
    ],
    "Historical Fiction": [
        "The year was 1347, and the ships arriving in port carried more than silks and spices,",
        "In the shadow of a crumbling empire, one family held a dangerous secret,",
        "The revolution had come at last, and with it, a reckoning none could escape,",
    ],
}

TRANSITIONS = [
    "As the days wore on,",
    "Against all odds,",
    "With courage drawn from unexpected places,",
    "Through sacrifice and determination,",
    "When darkness seemed unassailable,",
    "Driven by the bonds forged between them,",
]

CLIMAX_BEATS = [
    "the truth revealed itself in the most unexpected of moments, reshaping everything they thought they knew.",
    "a final confrontation forced each of them to choose between safety and what was right.",
    "the culmination of every choice, every wound, and every hope collided in a single breathless instant.",
    "old wounds were laid bare, and only through vulnerability could victory be claimed.",
]

CLOSINGS = [
    "Though the road ahead remained uncertain, they walked it together, changed and undaunted.",
    "The world would never be the same — and neither would they.",
    "In the end, it was not glory that sustained them, but the quiet understanding of those who had endured.",
    "And if the songs that followed did not capture every detail, they captured the most important truth of all: they had prevailed.",
]

WORLD_DESCRIPTIONS = {
    "Fantasy": "A realm of sweeping mountain ranges and ancient forests, where magic courses through ley lines beneath the earth and every ruin holds the memory of civilisations long forgotten.",
    "Sci-Fi": "A vast interstellar civilisation spanning dozens of star systems, connected by jump gates and governed by a fragile coalition of factions whose alliances shift as swiftly as solar winds.",
    "Mystery": "A fog-wrapped city of gaslit streets and shadowed alleyways, where every closed door conceals a secret and the line between law and corruption is perilously thin.",
    "Romance": "A vibrant world of sun-drenched piazzas and candlelit parlours, where chance encounters spark destinies and the heart's geography proves more treacherous than any map.",
    "Horror": "A landscape of isolated villages and forgotten estates, where ancient pacts fester beneath the surface of ordinary life and the night holds things that do not obey natural law.",
    "Adventure": "An age of exploration where uncharted territories still blaze white on every map, fortunes are won and lost on the turning of a tide, and courage is the only true currency.",
    "Historical Fiction": "A world in transition — empires rise and crumble, old certainties dissolve, and ordinary people find themselves swept into the currents of history with no choice but to swim.",
}


def _parse_characters(characters_str: str) -> list[str]:
    """Split a characters string into individual character descriptions."""
    # Try splitting by common delimiters
    for sep in [" and ", ", and ", ","]:
        parts = [p.strip() for p in characters_str.split(sep) if p.strip()]
        if len(parts) >= 2:
            return parts[:3]
    return [characters_str.strip()]


def _capitalise_first(s: str) -> str:
    return s[:1].upper() + s[1:] if s else s


def _build_title(genre: str, setting: str) -> str:
    setting_word = setting.split()[0].title() if setting else "Unknown"
    titles = {
        "Fantasy": f"The {setting_word} Chronicles",
        "Sci-Fi": f"Beyond {setting_word}",
        "Mystery": f"Shadows Over {setting_word}",
        "Romance": f"Hearts of {setting_word}",
        "Horror": f"The Darkness of {setting_word}",
        "Adventure": f"The {setting_word} Expedition",
        "Historical Fiction": f"The {setting_word} Legacy",
    }
    return titles.get(genre, f"A Tale of {setting_word}")


def _fallback_generate(req: StoryRequest) -> StoryResponse:
    genre = req.genre
    characters_list = _parse_characters(req.characters)
    char_names = ", ".join(_capitalise_first(c) for c in characters_list)

    opener = random.choice(OPENERS.get(genre, OPENERS["Adventure"]))
    transition = random.choice(TRANSITIONS)
    climax = random.choice(CLIMAX_BEATS)
    closing = random.choice(CLOSINGS)

    story = (
        f"{opener} {_capitalise_first(req.setting)} stood as both refuge and crucible for those brave or desperate "
        f"enough to call it home. Among them were {char_names} — unlikely companions bound together by the threads "
        f"of {req.theme}.\n\n"
        f"Their journey began without fanfare: a single moment of decision that set everything in motion. "
        f"The {req.setting} they thought they knew revealed hidden depths at every turn — dangers lurking beneath "
        f"familiar surfaces, and allies waiting in places they least expected. The weight of {req.theme} pressed "
        f"upon them constantly, shaping every choice, every sacrifice.\n\n"
        f"{transition} the stakes grew impossible to ignore. Each of them carried scars — some visible, some buried "
        f"deep — and it was precisely those wounds that forged the strange, resilient bond between them. They argued, "
        f"doubted, and at their lowest moments nearly surrendered. Yet something held.\n\n"
        f"In the heart of {req.setting}, {climax} The echoes of {req.theme} rang clear in the aftermath, a reminder "
        f"of how far they had come and how much it had cost.\n\n"
        f"{closing}"
    )

    title = _build_title(genre, req.setting)
    world = WORLD_DESCRIPTIONS.get(genre, f"A world defined by {req.setting}, where {req.theme} shapes every destiny.")

    character_descriptions = [
        f"{_capitalise_first(c)} — a compelling figure whose journey through {req.setting} tests every limit they possess."
        for c in characters_list
    ]

    return StoryResponse(story=story, title=title, characters=character_descriptions, world=world)


# ---------- OpenAI generator ----------

def _openai_generate(req: StoryRequest) -> StoryResponse:
    from openai import OpenAI  # type: ignore[import]

    client = OpenAI(api_key=os.environ["OPENAI_API_KEY"])

    prompt = (
        f"You are a creative fiction author. Write a compelling short story with the following details:\n"
        f"Genre: {req.genre}\n"
        f"Characters: {req.characters}\n"
        f"Setting: {req.setting}\n"
        f"Theme: {req.theme}\n\n"
        f"Respond ONLY with valid JSON in this exact structure:\n"
        f'{{"title": "...", "story": "...", "characters": ["...", "..."], "world": "..."}}\n'
        f"The story should be 200-350 words. Characters is a list of 2-3 short character descriptions. "
        f"World is a 1-2 sentence description of the story world."
    )

    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.85,
    )

    content = response.choices[0].message.content or "{}"
    data = json.loads(content)

    return StoryResponse(
        title=data.get("title", "Untitled"),
        story=data.get("story", ""),
        characters=data.get("characters", []),
        world=data.get("world", ""),
    )


# ---------- Routes ----------

@app.get("/")
def health_check():
    return {"status": "ok"}


@app.post("/generate", response_model=StoryResponse)
def generate_story(req: StoryRequest):
    try:
        if os.environ.get("OPENAI_API_KEY"):
            return _openai_generate(req)
        return _fallback_generate(req)
    except Exception as exc:
        raise HTTPException(status_code=500, detail=str(exc)) from exc
