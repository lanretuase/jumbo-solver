# 🧩 Jumble Solver

A modern, production-quality full-stack web application that unscrambles letters to find all valid English words — both full anagrams and sub-anagrams.

Built with **FastAPI** (Python 3.12+) and **React** (TypeScript + Tailwind CSS v4).

---

## ✨ Features

- **Instant solving** — find all valid words from any set of letters
- **Full & sub-anagram detection** — identifies words using all or a subset of input letters
- **Efficient algorithm** — Counter-based subset matching with precomputed cache, ~30ms query time
- **Modern dashboard** — glassmorphism UI with dark/light mode
- **Sort & filter** — sort by length or alphabetically; filter by anagram type
- **Export results** — download as CSV or JSON
- **Word length chart** — visual distribution of match lengths
- **Search history** — saved locally, click to re-run
- **Responsive** — works on desktop and mobile
- **Docker ready** — one-command deployment with Docker Compose

---

## 🏗️ Architecture

```
jumble-solver/
├── backend/           # FastAPI REST API (Python 3.12+)
│   ├── app/           # Application source
│   │   ├── main.py         # App factory, CORS, lifespan
│   │   ├── config.py       # Pydantic settings
│   │   ├── models.py       # Request/response schemas
│   │   ├── router.py       # API endpoints
│   │   ├── solver.py       # Core anagram engine
│   │   ├── dictionary.py   # Dictionary loader + cache
│   │   └── logging_config.py
│   ├── tests/         # Pytest suite
│   └── data/          # Word list
├── frontend/          # React + TypeScript + Tailwind v4
│   └── src/
│       ├── components/     # UI components
│       ├── hooks/          # Custom React hooks
│       ├── api/            # API client
│       ├── utils/          # Helpers
│       └── types/          # TypeScript interfaces
├── docs/              # Architecture & complexity analysis
├── docker-compose.yml
└── README.md
```

---

## 🚀 Quick Start

### Prerequisites

- **Python 3.12+** and **pip**
- **Node.js 18+** and **npm**
- **Docker** and **Docker Compose** (optional)

### Option 1: Docker Compose (Recommended)

```bash
docker compose up --build
```

- Frontend: [http://localhost:3000](http://localhost:3000)
- Backend API: [http://localhost:8000/docs](http://localhost:8000/docs)

### Option 2: Local Development

**Backend:**

```bash
cd backend
pip install -r requirements.txt
uvicorn app.main:app --reload --port 8000
```

**Frontend:**

```bash
cd frontend
npm install
npm run dev
```

- Frontend: [http://localhost:5173](http://localhost:5173) (Vite proxies `/api` to backend)
- Backend: [http://localhost:8000/docs](http://localhost:8000/docs) (Swagger UI)

---

## 📡 API Reference

### `POST /api/solve`

Find all words formable from the given letters.

**Request:**
```json
{
  "letters": "dog"
}
```

**Response:**
```json
{
  "input": "dog",
  "execution_ms": 4.2,
  "total_matches": 4,
  "full_anagram_count": 2,
  "sub_anagram_count": 2,
  "longest_word": "dog",
  "matches": [
    { "word": "dog", "length": 3, "type": "full_anagram" },
    { "word": "god", "length": 3, "type": "full_anagram" },
    { "word": "do", "length": 2, "type": "sub_anagram" },
    { "word": "go", "length": 2, "type": "sub_anagram" }
  ]
}
```

### `GET /api/health`

Health check with dictionary metadata.

### `GET /api/stats`

Dictionary statistics (total words, min/max/avg length).

---

## 🔬 Algorithm

**Counter-based subset matching** with length-bucketed indexing.

### How It Works

1. **Startup**: Load dictionary, precompute `Counter` for every word, group by length.
2. **Query**: Compute `Counter(input)`, iterate only over words with length ≤ input length.
3. **Match**: A word matches if every character count ≤ the input's count.
4. **Classify**: Same length → full anagram; shorter → sub-anagram.

### Complexity

| Operation | Time | Space |
|-----------|------|-------|
| Dictionary load | O(D × L) | O(D × L) |
| Query | O(D' × A) | O(M) |
| Overall | — | ~210 MB for 370K words |

Where D = dictionary size, L = avg word length, D' = candidate words (length ≤ input), A = unique chars per word, M = matches.

**Typical query time: 5–40ms** depending on input length.

See [docs/complexity.md](docs/complexity.md) for detailed analysis.

---

## 🧪 Testing

### Backend

```bash
cd backend
pip install -r requirements.txt
python -m pytest tests/ -v --cov=app --cov-report=term-missing
```

### Type Checking

```bash
cd backend
python -m mypy app/ --strict
```

---

## 📖 Documentation

- [Architecture Documentation](docs/architecture.md)
- [Complexity Analysis](docs/complexity.md)

---

## 🛠️ Tech Stack

| Layer | Technology |
|-------|------------|
| Backend | Python 3.12, FastAPI, Pydantic v2, Uvicorn |
| Frontend | React 19, TypeScript, Tailwind CSS v4, Vite |
| Testing | Pytest, httpx |
| Containerization | Docker, Docker Compose |
| Dictionary | dwyl/english-words (~370K words) |

---

## 📝 License

This project is for educational and portfolio demonstration purposes.

The word list is sourced from [dwyl/english-words](https://github.com/dwyl/english-words) (freely available).
