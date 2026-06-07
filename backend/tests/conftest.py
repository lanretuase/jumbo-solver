"""Shared pytest fixtures for the Jumble Solver test suite."""

import tempfile
from collections.abc import Generator
from pathlib import Path

import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient

from app.confidence import ConfidenceScorer
from app.dictionary import DictionaryService
from app.models import SolveMode
from app.router import router
from app.solver import JumbleSolver
from app.word_classifier import WordClassifier

# Known word list used across all tests.
_TEST_WORDS = [
    "dog",
    "god",
    "do",
    "go",
    "dogs",
    "cat",
    "act",
    "tac",
    "at",
    "a",       # len < 2 → filtered out
    "123",     # non-alpha → filtered out
    "hello",
    "world",
]


@pytest.fixture()
def small_word_list(tmp_path: Path) -> Path:
    """Create a temporary word file containing the known test words."""
    word_file = tmp_path / "words.txt"
    word_file.write_text("\n".join(_TEST_WORDS), encoding="utf-8")
    return word_file


@pytest.fixture()
def dictionary_service(small_word_list: Path) -> DictionaryService:
    """Return a loaded :class:`DictionaryService` backed by the test word list."""
    svc = DictionaryService(small_word_list)
    svc.load()
    return svc


@pytest.fixture()
def classifier() -> WordClassifier:
    """Return a :class:`WordClassifier` for English."""
    return WordClassifier(language="en")


@pytest.fixture()
def scorer(classifier: WordClassifier) -> ConfidenceScorer:
    """Return a :class:`ConfidenceScorer` backed by the classifier."""
    return ConfidenceScorer(classifier, language="en")


@pytest.fixture()
def solver(dictionary_service: DictionaryService, scorer: ConfidenceScorer) -> JumbleSolver:
    """Return a :class:`JumbleSolver` in PERMISSIVE mode (backward-compatible).

    Uses PERMISSIVE so that existing tests see the same results as before
    the NLP validation layer was added.
    """
    return JumbleSolver(dictionary_service, scorer, default_mode=SolveMode.PERMISSIVE)


@pytest.fixture()
def strict_solver(dictionary_service: DictionaryService, scorer: ConfidenceScorer) -> JumbleSolver:
    """Return a :class:`JumbleSolver` in STRICT mode."""
    return JumbleSolver(dictionary_service, scorer, default_mode=SolveMode.STRICT)


@pytest.fixture()
def client(
    dictionary_service: DictionaryService,
    scorer: ConfidenceScorer,
    solver: JumbleSolver,
) -> Generator[TestClient, None, None]:
    """Create a FastAPI ``TestClient`` with the solver wired into app state.

    The lifespan is bypassed: we set ``app.state`` manually so tests are
    deterministic and do not depend on a real dictionary file.
    """
    app = FastAPI(title="Jumble Solver API – Test", version="2.0.0")
    app.include_router(router)
    app.state.dictionary = dictionary_service
    app.state.scorer = scorer
    app.state.solver = solver

    with TestClient(app) as tc:
        yield tc
