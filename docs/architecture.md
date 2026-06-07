# Architecture Documentation — Jumble Solver

## System Architecture

The Jumble Solver is a full-stack web application composed of two independent services communicating over HTTP REST APIs. It follows a clean separation of concerns with a stateless backend and a reactive frontend.

```
┌─────────────────────────────────────────────────────────────────┐
│                        Docker Compose                           │
│                                                                 │
│  ┌─────────────────────┐      ┌─────────────────────────────┐  │
│  │   Frontend (Nginx)  │      │     Backend (Uvicorn)       │  │
│  │   Port 3000 → 80    │─────▶│     Port 8000               │  │
│  │                     │ /api │                               │  │
│  │  React SPA          │      │  ┌─────────────────────────┐ │  │
│  │  TypeScript          │      │  │      FastAPI App        │ │  │
│  │  Tailwind CSS v4    │      │  │  ┌───────────────────┐  │ │  │
│  │                     │      │  │  │   API Router      │  │ │  │
│  └─────────────────────┘      │  │  │   /api/solve      │  │ │  │
│                               │  │  │   /api/health     │  │ │  │
│                               │  │  │   /api/stats      │  │ │  │
│                               │  │  └────────┬──────────┘  │ │  │
│                               │  │           │              │ │  │
│                               │  │  ┌────────▼──────────┐  │ │  │
│                               │  │  │  JumbleSolver     │  │ │  │
│                               │  │  │  (Solver Engine)  │  │ │  │
│                               │  │  └────────┬──────────┘  │ │  │
│                               │  │           │              │ │  │
│                               │  │  ┌────────▼──────────┐  │ │  │
│                               │  │  │ DictionaryService │  │ │  │
│                               │  │  │ (Counter Cache)   │  │ │  │
│                               │  │  └────────┬──────────┘  │ │  │
│                               │  └───────────┼─────────────┘ │  │
│                               │              │                │  │
│                               │     ┌────────▼──────────┐    │  │
│                               │     │   words.txt       │    │  │
│                               │     │   (~370K words)   │    │  │
│                               │     └───────────────────┘    │  │
│                               └─────────────────────────────┘  │
└─────────────────────────────────────────────────────────────────┘
```

## Backend Architecture

### Layer Diagram

```
Request Flow:
  HTTP Request
       │
       ▼
  ┌──────────────────┐
  │   CORS Middleware │     Handles cross-origin requests
  └────────┬─────────┘
           ▼
  ┌──────────────────┐
  │   API Router     │     Route matching, request validation
  └────────┬─────────┘
           ▼
  ┌──────────────────┐
  │   Pydantic Models│     Input validation, serialization
  └────────┬─────────┘
           ▼
  ┌──────────────────┐
  │   JumbleSolver   │     Core algorithm execution
  └────────┬─────────┘
           ▼
  ┌──────────────────┐
  │ DictionaryService│     Precomputed Counter cache lookup
  └──────────────────┘
```

### Components

| Component | File | Responsibility |
|-----------|------|----------------|
| **App Factory** | `main.py` | FastAPI app creation, CORS, lifespan management |
| **Configuration** | `config.py` | Environment-based settings via Pydantic BaseSettings |
| **Models** | `models.py` | Request/response schemas with validation |
| **Router** | `router.py` | HTTP endpoint definitions and dependency injection |
| **Solver** | `solver.py` | Counter-based anagram matching algorithm |
| **Dictionary** | `dictionary.py` | Word list loading, normalization, and counter caching |
| **Logging** | `logging_config.py` | Structured logging configuration |

### Data Flow

1. **Startup**: `DictionaryService` loads `words.txt` and precomputes a `Counter` for every word.
2. **Request**: Client sends `POST /api/solve` with `{"letters": "dog"}`.
3. **Validation**: Pydantic validates the input (alpha-only, 1-20 chars).
4. **Solving**: `JumbleSolver` computes `Counter("dog")` and iterates over cached dictionary entries, checking counter subset relationships.
5. **Classification**: Each match is classified as `full_anagram` (uses all letters) or `sub_anagram` (uses a subset).
6. **Response**: Results are sorted and returned with timing and statistics.

## Frontend Architecture

### Component Tree

```
App
├── Layout
│   ├── Header (title, dark mode toggle)
│   └── Footer
├── SearchPanel (input, submit button)
├── StatsPanel (5 stat cards)
├── ExportButtons (CSV, JSON)
├── ResultsTable (sortable, filterable)
├── ChartPanel (length distribution)
├── TopMatches (top 20 longest)
├── HistoryPanel (search history)
├── EmptyState (no results yet)
├── LoadingSpinner (during API call)
└── ErrorMessage (on API failure)
```

### State Management

The application uses React hooks for state management (no external state library needed at this scale):

| Hook | Purpose | Persistence |
|------|---------|-------------|
| `useSolver` | API call state, results, loading, error | Memory |
| `useTheme` | Dark/light mode toggle | localStorage |
| `useHistory` | Search history (max 20) | localStorage |

### API Communication

- All API calls go through `src/api/solver.ts`
- In development, Vite proxies `/api` requests to `http://localhost:8000`
- In production, Nginx proxies `/api` requests to the backend container

## Security Considerations

- **CORS**: Configured to allow only specific frontend origins
- **Input Validation**: Pydantic enforces alpha-only input, max 20 characters
- **No Database**: No SQL injection risk — file-based dictionary is read-only
- **Non-root Docker**: Backend runs as a non-root user
- **Rate Limiting**: Not implemented; could be added via middleware for production

## Scalability

- **Dictionary Size**: The length-bucketed index and Counter cache scale linearly with dictionary size. A ~370K word dictionary loads in ~1 second and uses ~50MB RAM.
- **Query Performance**: Each query scans relevant length buckets. For short inputs (1-5 chars), this is a small fraction of the dictionary. Worst case (~15 letter input) scans the full dictionary in ~30ms.
- **Horizontal Scaling**: The stateless backend can be replicated behind a load balancer. Each instance loads its own dictionary copy.
- **Caching Queries**: For repeated queries, a Redis LRU cache could be added. Not needed at current scale.
