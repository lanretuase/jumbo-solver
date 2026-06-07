"""Confidence scoring engine for word validation.

Produces a composite 0.0–1.0 confidence score for each word by combining
three weighted signals:

- **Dictionary score** (40%): 1.0 if the word appears in any corpus, else 0.0.
- **Frequency score** (35%): Normalised Zipf frequency (0–7 scale mapped to 0–1).
- **Category bonus** (25%): Higher for STANDARD words, lower for ARCHAIC/INVALID.
"""

from __future__ import annotations

import logging
from dataclasses import dataclass

from wordfreq import zipf_frequency

from app.models import WordCategory
from app.word_classifier import WordClassifier

logger = logging.getLogger(__name__)

# Maximum practical Zipf score for normalisation.
_ZIPF_MAX = 7.0

# Composite score weights (must sum to 1.0).
_W_DICTIONARY = 0.40
_W_FREQUENCY = 0.35
_W_CATEGORY = 0.25

# Per-category bonus values.
_CATEGORY_BONUSES: dict[WordCategory, float] = {
    WordCategory.STANDARD: 1.0,
    WordCategory.ARCHAIC: 0.35,
    WordCategory.ABBREVIATION: 0.15,
    WordCategory.SLANG: 0.50,
    WordCategory.PROPER_NOUN: 0.30,
    WordCategory.INVALID: 0.0,
}


@dataclass(frozen=True)
class ConfidenceResult:
    """Complete confidence assessment for a single word."""

    overall: float
    dictionary_score: float
    frequency_score: float
    category: WordCategory
    zipf: float


class ConfidenceScorer:
    """Scores words on a 0.0–1.0 confidence scale.

    The scorer maintains an internal cache so that repeated lookups for the
    same word are O(1).  Call :meth:`precompute` at startup to warm the cache
    for the entire dictionary.
    """

    def __init__(self, classifier: WordClassifier, language: str = "en") -> None:
        self._classifier = classifier
        self._language = language
        self._cache: dict[str, ConfidenceResult] = {}

    # ------------------------------------------------------------------
    # Public API
    # ------------------------------------------------------------------

    def score(self, word: str) -> ConfidenceResult:
        """Compute (or retrieve cached) confidence for *word*."""
        cached = self._cache.get(word)
        if cached is not None:
            return cached
        result = self._score_impl(word)
        self._cache[word] = result
        return result

    def score_batch(self, words: list[str]) -> dict[str, ConfidenceResult]:
        """Score a batch of words and return a mapping."""
        return {w: self.score(w) for w in words}

    def precompute(self, words: list[str]) -> None:
        """Pre-warm the cache for *words* (typically the entire dictionary).

        This should be called once at startup so that query-time lookups are
        pure cache hits.
        """
        new_count = 0
        for w in words:
            if w not in self._cache:
                self._cache[w] = self._score_impl(w)
                new_count += 1
        logger.info(
            "precomputed confidence | new=%d | total_cached=%d",
            new_count,
            len(self._cache),
        )

    @property
    def cache_size(self) -> int:
        """Number of words currently cached."""
        return len(self._cache)

    # ------------------------------------------------------------------
    # Internals
    # ------------------------------------------------------------------

    def _score_impl(self, word: str) -> ConfidenceResult:
        w = word.lower()
        category = self._classifier.classify(w)
        zipf = zipf_frequency(w, self._language)

        # Dictionary component: is it a real word?
        is_real_word = category in (
            WordCategory.STANDARD,
            WordCategory.ARCHAIC,
            WordCategory.PROPER_NOUN,
            WordCategory.SLANG,
        )
        dict_score = 1.0 if is_real_word else 0.0

        # Frequency component: normalise Zipf to 0–1.
        freq_score = min(zipf / _ZIPF_MAX, 1.0)

        # Category bonus.
        cat_bonus = _CATEGORY_BONUSES.get(category, 0.0)

        # Weighted composite.
        overall = (
            _W_DICTIONARY * dict_score
            + _W_FREQUENCY * freq_score
            + _W_CATEGORY * cat_bonus
        )
        overall = round(min(overall, 1.0), 4)

        return ConfidenceResult(
            overall=overall,
            dictionary_score=dict_score,
            frequency_score=round(freq_score, 4),
            category=category,
            zipf=round(zipf, 2),
        )
