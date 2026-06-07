"""API route definitions."""

import logging
from typing import Any

from fastapi import APIRouter, HTTPException, Request

from app.models import (
    DictionaryStats,
    HealthResponse,
    ModeInfo,
    SolveMode,
    SolveRequest,
    SolveResponse,
)
from app.solve_mode import MODE_CONFIGS

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api", tags=["jumble"])


def _get_solver(request: Request) -> Any:
    """Retrieve the JumbleSolver instance from app state."""
    solver = getattr(request.app.state, "solver", None)
    if solver is None:
        raise HTTPException(
            status_code=503,
            detail="Solver is not initialised. The server may still be starting up.",
        )
    return solver


def _get_dictionary(request: Request) -> Any:
    """Retrieve the DictionaryService instance from app state."""
    dictionary = getattr(request.app.state, "dictionary", None)
    if dictionary is None:
        raise HTTPException(
            status_code=503,
            detail="Dictionary is not loaded. The server may still be starting up.",
        )
    return dictionary


# ------------------------------------------------------------------
# Endpoints
# ------------------------------------------------------------------


@router.post("/solve", response_model=SolveResponse)
async def solve(body: SolveRequest, request: Request) -> SolveResponse:
    """Solve a jumble: find all words formable from the given letters."""
    solver = _get_solver(request)
    try:
        result: SolveResponse = solver.solve(body.letters, mode=body.mode)
    except Exception as exc:
        logger.exception("unexpected error during solve")
        raise HTTPException(status_code=500, detail=str(exc)) from exc
    return result


@router.get("/health", response_model=HealthResponse)
async def health(request: Request) -> HealthResponse:
    """Return service health and dictionary metadata."""
    dictionary = _get_dictionary(request)
    return HealthResponse(
        status="ok",
        dictionary_size=dictionary.word_count,
        version="2.0.0",
    )


@router.get("/stats", response_model=DictionaryStats)
async def stats(request: Request) -> DictionaryStats:
    """Return dictionary statistics."""
    dictionary = _get_dictionary(request)
    return dictionary.stats


@router.get("/modes", response_model=list[ModeInfo])
async def modes() -> list[ModeInfo]:
    """Return all available solving modes with descriptions."""
    return [
        ModeInfo(
            mode=mode,
            description=config.description,
            min_confidence=config.min_confidence,
            include_abbreviations=config.include_abbreviations,
            include_archaic=config.include_archaic,
        )
        for mode, config in MODE_CONFIGS.items()
    ]
