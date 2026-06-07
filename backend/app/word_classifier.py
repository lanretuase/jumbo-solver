"""Word classification engine using corpus frequency analysis.

Classifies each word into a :class:`WordCategory` using `wordfreq` Zipf
scores as the primary signal, with heuristic fallbacks for zero-frequency
entries (abbreviation detection, vowel checks, length analysis).
"""

from __future__ import annotations

import logging

from wordfreq import zipf_frequency

from app.models import WordCategory

logger = logging.getLogger(__name__)

_VOWELS = frozenset("aeiouy")


class WordClassifier:
    """Classifies words into categories using corpus frequency data.

    Classification rules (evaluated top-to-bottom):

    ========================  ==============  ==================
    Condition                 Zipf range      Category
    ========================  ==============  ==================
    Corpus-attested, common   ≥ 1.0           STANDARD
    Corpus-attested, rare     (0, 1.0)        ARCHAIC
    No corpus data, no vowel  0, len ≤ 4      ABBREVIATION
    No corpus data, short     0, len ≤ 2      INVALID
    No corpus data, long      0, len ≥ 4      ARCHAIC (benefit of doubt)
    No corpus data, 3-char    0               INVALID
    ========================  ==============  ==================
    """

    def __init__(self, language: str = "en") -> None:
        self._language = language
        self._cache: dict[str, WordCategory] = {}

    # ------------------------------------------------------------------
    # Public API
    # ------------------------------------------------------------------

    def classify(self, word: str) -> WordCategory:
        """Return the category for *word*, with transparent caching."""
        cached = self._cache.get(word)
        if cached is not None:
            return cached
        category = self._classify_impl(word)
        self._cache[word] = category
        return category

    def classify_batch(self, words: list[str]) -> dict[str, WordCategory]:
        """Classify a list of words and return a mapping."""
        return {w: self.classify(w) for w in words}

    def get_zipf(self, word: str) -> float:
        """Return the raw Zipf frequency score for *word*."""
        return zipf_frequency(word.lower(), self._language)

    @property
    def cache_size(self) -> int:
        """Number of words currently cached."""
        return len(self._cache)

    # ------------------------------------------------------------------
    # Internals
    # ------------------------------------------------------------------

    def _classify_impl(self, word: str) -> WordCategory:
        w = word.lower()
        zipf = zipf_frequency(w, self._language)
        has_vowel = self._has_vowel(w)
        length = len(w)

        # ── Abbreviation detection (takes precedence) ───────────────────
        if not has_vowel:
            return WordCategory.ABBREVIATION

        # ── Two-letter words ────────────────────────────────────────────
        if length == 2:
            if w in _VALID_TWO_LETTER_WORDS:
                return WordCategory.STANDARD
            return WordCategory.ABBREVIATION if zipf > 2.0 else WordCategory.INVALID

        # ── High-frequency: definitely a real word ──────────────────────
        # Require higher Zipf for 3-letter words to avoid acronyms (like 'pya')
        # being classified as STANDARD.
        min_standard_zipf = 2.5 if length == 3 else 1.5
        
        if zipf >= min_standard_zipf:
            return WordCategory.STANDARD

        # ── Low-but-nonzero: attested but rare ──────────────────────────
        if zipf > 0:
            return WordCategory.ARCHAIC

        # ── Zero frequency: not in any corpus ───────────────────────────
        if length <= 3:
            return WordCategory.INVALID

        # Longer words get benefit of the doubt — could be valid
        # technical terms not in the wordfreq corpus
        return WordCategory.ARCHAIC

    @staticmethod
    def _has_vowel(word: str) -> bool:
        """Return ``True`` if *word* contains at least one vowel (including y)."""
        return bool(_VOWELS & set(word))

_VALID_TWO_LETTER_WORDS = frozenset([
    "aa", "ab", "ad", "ae", "ag", "ah", "ai", "al", "am", "an", "ar", "as", "at",
    "aw", "ax", "ay", "ba", "be", "bi", "bo", "by", "de", "do", "ed", "ef", "eh",
    "el", "em", "en", "er", "es", "et", "ew", "ex", "fa", "fe", "go", "ha", "he",
    "hi", "hm", "ho", "id", "if", "in", "is", "it", "jo", "ka", "ki", "la", "li",
    "lo", "ma", "me", "mi", "mm", "mo", "mu", "my", "na", "ne", "no", "nu", "od",
    "oe", "of", "oh", "oi", "ok", "om", "on", "op", "or", "os", "ow", "ox", "oy",
    "pa", "pe", "pi", "po", "qi", "re", "sh", "si", "so", "ta", "te", "ti", "to",
    "uh", "um", "un", "up", "us", "ut", "we", "wo", "xi", "xu", "ya", "ye", "yo", "za"
])
