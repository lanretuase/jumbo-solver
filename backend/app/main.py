"""FastAPI application entry point."""

import logging
from collections.abc import AsyncGenerator
from contextlib import asynccontextmanager
from pathlib import Path

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import RedirectResponse

from app.confidence import ConfidenceScorer
from app.config import get_settings
from app.dictionary import DictionaryService
from app.logging_config import setup_logging
from app.router import router
from app.solver import JumbleSolver
from app.word_classifier import WordClassifier

logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
    """Application lifespan: load dictionary, build NLP pipeline, initialise solver."""
    setup_logging()
    settings = get_settings()

    # Resolve dictionary path relative to the *backend* directory.
    backend_dir = Path(__file__).resolve().parent.parent
    dict_path = backend_dir / settings.dictionary_path

    logger.info("starting up | dictionary_path=%s", dict_path)

    # ── Load dictionary ─────────────────────────────────────────────
    dictionary = DictionaryService(dict_path)
    dictionary.load()

    # ── Build NLP validation pipeline ───────────────────────────────
    classifier = WordClassifier(language=settings.wordfreq_language)
    scorer = ConfidenceScorer(classifier, language=settings.wordfreq_language)

    # Pre-compute confidence scores for the entire dictionary.
    logger.info("precomputing confidence scores for %d words…", dictionary.word_count)
    scorer.precompute(dictionary.all_words)

    # ── Create solver ───────────────────────────────────────────────
    solver = JumbleSolver(dictionary, scorer)

    app.state.dictionary = dictionary
    app.state.classifier = classifier
    app.state.scorer = scorer
    app.state.solver = solver

    logger.info(
        "startup complete | words=%d | buckets=%d | cached_scores=%d",
        dictionary.word_count,
        len(dictionary.words_by_length),
        scorer.cache_size,
    )
    yield
    logger.info("shutting down")


def create_app() -> FastAPI:
    """Build and return the configured FastAPI application."""
    settings = get_settings()

    app = FastAPI(
        title="Jumble Solver API",
        version="2.0.0",
        description="Solve jumble puzzles with NLP-validated confidence scoring.",
        lifespan=lifespan,
    )

    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.cors_origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    app.include_router(router)

    @app.get("/", include_in_schema=False)
    async def root() -> RedirectResponse:
        """Redirect root to interactive API docs."""
        return RedirectResponse(url="/docs")

    return app


app = create_app()
