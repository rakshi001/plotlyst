# Plotlyst — AI-Powered Story Generator

> Turn a few words into a rich, narrative story in seconds.

Plotlyst is a full-stack web application that uses AI (OpenAI GPT or a built-in template engine) to generate compelling short stories from user-supplied inputs.

---

## Features

- 🎭 **Seven genres** — Fantasy, Sci-Fi, Mystery, Romance, Horror, Adventure, Historical Fiction
- ✍️ **Custom characters, setting & theme** — shape the story your way
- 🤖 **Dual generation engines** — OpenAI GPT-3.5 when an API key is present, or a rich built-in template fallback that needs no key
- 🌍 **World description** — get a flavourful overview of the story world
- 👤 **Character cards** — each character is presented individually
- ⚡ **Fast & responsive** — React + Vite frontend, FastAPI backend

---

## Tech Stack

| Layer    | Technology                          |
|----------|-------------------------------------|
| Frontend | React 18, TypeScript, Vite          |
| Backend  | Python 3.11+, FastAPI, Pydantic v2  |
| AI       | OpenAI GPT-3.5 (optional)           |

---

## Project Structure

```
plotlyst/
├── backend/
│   ├── main.py            # FastAPI application
│   ├── requirements.txt
│   └── .env.example
├── frontend/
│   ├── src/
│   │   ├── App.tsx        # Main UI component
│   │   ├── App.css        # Component styles
│   │   └── index.css      # Global reset & base styles
│   ├── index.html
│   └── package.json
└── README.md
```

---

## Setup

### Prerequisites

- Python 3.11+
- Node.js 18+
- npm 9+

### Backend

```bash
cd backend

# Install dependencies
pip install -r requirements.txt

# (Optional) configure OpenAI
cp .env.example .env
# Edit .env and add your OPENAI_API_KEY

# Start the server
uvicorn main:app --reload
# → http://localhost:8000
```

### Frontend

```bash
cd frontend

npm install
npm run dev
# → http://localhost:5173
```

Open **http://localhost:5173** in your browser.

---

## API Documentation

### `GET /`
Health check.

**Response**
```json
{ "status": "ok" }
```

---

### `POST /generate`
Generate a story.

**Request body**
```json
{
  "genre": "Fantasy",
  "characters": "a brave knight and a wise wizard",
  "setting": "medieval kingdom",
  "theme": "redemption and sacrifice"
}
```

**Response**
```json
{
  "title": "The Kingdom Chronicles",
  "story": "...",
  "characters": [
    "A brave knight — a compelling figure whose journey...",
    "A wise wizard — a compelling figure whose journey..."
  ],
  "world": "A realm of sweeping mountain ranges..."
}
```

---

## Configuration

| Variable        | Description                         | Required |
|-----------------|-------------------------------------|----------|
| `OPENAI_API_KEY`| OpenAI API key for GPT story gen    | No       |

If `OPENAI_API_KEY` is not set, the application falls back to the built-in template-based generator which produces high-quality stories without any external API calls.

---

## Screenshots

_Coming soon — run the app locally to see it in action!_

---

## Licence

MIT
