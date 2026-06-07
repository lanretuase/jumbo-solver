"""Pydantic v2 request / response models for the Jumble Solver API."""

from enum import Enum

from pydantic import BaseModel, Field


# ------------------------------------------------------------------
# Enumerations
# ------------------------------------------------------------------


class SolveMode(str, Enum):
    """Available solving modes that control which words are returned."""

    STRICT = "strict"
    DICTIONARY = "dictionary"
    SCRABBLE = "scrabble"
    CROSSWORD = "crossword"
    PERMISSIVE = "permissive"


class WordCategory(str, Enum):
    """Word classification categories."""

    STANDARD = "standard"
    ARCHAIC = "archaic"
    ABBREVIATION = "abbreviation"
    SLANG = "slang"
    PROPER_NOUN = "proper_noun"
    INVALID = "invalid"


class MatchType(str, Enum):
    """How a matched word relates to the input letters."""

    FULL_ANAGRAM = "full_anagram"
    SUB_ANAGRAM = "sub_anagram"


# ------------------------------------------------------------------
# Request / Response
# ------------------------------------------------------------------


class SolveRequest(BaseModel):
    """Payload sent by the client to solve a jumble."""

    letters: str = Field(
        ...,
        min_length=1,
        max_length=20,
        pattern=r"^[a-zA-Z]+$",
        description="The scrambled letters to solve (alphabetic only).",
        examples=["dog", "CAT"],
    )
    mode: SolveMode = Field(
        default=SolveMode.STRICT,
        description="Solving mode controlling which words are returned.",
    )


class MatchResult(BaseModel):
    """A single word that can be formed from the input letters."""

    word: str
    length: int
    type: MatchType
    confidence: float = Field(
        default=0.0,
        ge=0.0,
        le=1.0,
        description="Composite confidence score (0.0–1.0).",
    )
    category: WordCategory = Field(
        default=WordCategory.STANDARD,
        description="Word classification category.",
    )
    zipf_score: float = Field(
        default=0.0,
        ge=0.0,
        description="Zipf frequency score from corpus data.",
    )


class SolveResponse(BaseModel):
    """Complete response for a solve request."""

    input: str
    execution_ms: float
    total_matches: int
    full_anagram_count: int
    sub_anagram_count: int
    longest_word: str | None
    matches: list[MatchResult]
    mode: SolveMode = SolveMode.STRICT
    filtered_count: int = Field(
        default=0,
        description="Number of candidates rejected by the mode filter.",
    )


class HealthResponse(BaseModel):
    """Health-check response."""

    status: str
    dictionary_size: int
    version: str


class DictionaryStats(BaseModel):
    """Statistics about the loaded dictionary."""

    total_words: int
    min_length: int
    max_length: int
    avg_length: float


class ModeInfo(BaseModel):
    """Metadata about a single solving mode."""

    mode: SolveMode
    description: str
    min_confidence: float
    include_abbreviations: bool
    include_archaic: bool
