"""Solving mode configuration for the Jumble Solver.

Each mode defines thresholds that control which words pass validation:
- **Strict**: Common English words only (portfolio-quality output).
- **Dictionary**: All corpus-attested words including rare forms.
- **Scrabble**: All valid word-game words regardless of frequency.
- **Crossword**: Broad vocabulary including abbreviations.
- **Permissive**: Unfiltered legacy behaviour.
"""

from __future__ import annotations

from dataclasses import dataclass

from app.models import SolveMode


@dataclass(frozen=True)
class ModeConfig:
    """Filter thresholds for a solving mode."""

    min_confidence: float
    include_abbreviations: bool
    include_slang: bool
    include_archaic: bool
    min_zipf: float | None
    description: str


MODE_CONFIGS: dict[SolveMode, ModeConfig] = {
    SolveMode.STRICT: ModeConfig(
        min_confidence=0.40,
        include_abbreviations=False,
        include_slang=False,
        include_archaic=False,
        min_zipf=2.0,
        description="Common English words only — high confidence, no obscure forms",
    ),
    SolveMode.DICTIONARY: ModeConfig(
        min_confidence=0.15,
        include_abbreviations=False,
        include_slang=True,
        include_archaic=True,
        min_zipf=0.5,
        description="All dictionary-attested words including rare and archaic forms",
    ),
    SolveMode.SCRABBLE: ModeConfig(
        min_confidence=0.05,
        include_abbreviations=False,
        include_slang=True,
        include_archaic=True,
        min_zipf=None,
        description="All words valid in competitive Scrabble play",
    ),
    SolveMode.CROSSWORD: ModeConfig(
        min_confidence=0.10,
        include_abbreviations=True,
        include_slang=True,
        include_archaic=True,
        min_zipf=None,
        description="Broad vocabulary including abbreviations for crossword puzzles",
    ),
    SolveMode.PERMISSIVE: ModeConfig(
        min_confidence=0.0,
        include_abbreviations=True,
        include_slang=True,
        include_archaic=True,
        min_zipf=None,
        description="All entries from the raw word list (legacy behaviour)",
    ),
}
