"""Jumble/anagram solver engine with NLP validation."""

import logging
import time
from collections import Counter

from app.confidence import ConfidenceScorer
from app.dictionary import DictionaryService
from app.models import MatchResult, MatchType, SolveMode, SolveResponse, WordCategory
from app.solve_mode import MODE_CONFIGS, ModeConfig

logger = logging.getLogger(__name__)


class JumbleSolver:
    """Finds all words that can be formed from a set of input letters.

    Words whose ``Counter`` is a subset of the input ``Counter`` are returned,
    classified as either *full anagram* (same length) or *sub-anagram*.

    Each candidate is then scored for confidence and filtered according to the
    requested :class:`SolveMode`.
    """

    def __init__(
        self,
        dictionary: DictionaryService,
        scorer: ConfidenceScorer,
        default_mode: SolveMode = SolveMode.STRICT,
    ) -> None:
        self._dictionary = dictionary
        self._scorer = scorer
        self._default_mode = default_mode

    # ------------------------------------------------------------------
    # Public API
    # ------------------------------------------------------------------

    def solve(
        self,
        letters: str,
        mode: SolveMode | None = None,
    ) -> SolveResponse:
        """Find all dictionary words formable from *letters*.

        Parameters
        ----------
        letters:
            The scrambled letters (case-insensitive).
        mode:
            Solving mode.  Falls back to the default mode set at init time.

        Returns
        -------
        SolveResponse
            Full result payload including matches, timing, scores, and stats.
        """
        start = time.perf_counter()

        effective_mode = mode or self._default_mode
        mode_config = MODE_CONFIGS[effective_mode]

        normalised = letters.lower()
        input_counter: dict[str, int] = dict(Counter(normalised))
        input_length = len(normalised)

        matches: list[MatchResult] = []
        filtered_count = 0

        # Only check length buckets that could possibly match.
        for length in range(2, input_length + 1):
            bucket = self._dictionary.words_by_length.get(length)
            if bucket is None:
                continue
            for word, word_counter in bucket:
                if not self._is_subset(word_counter, input_counter):
                    continue

                # ── Score & classify ────────────────────────────────
                result = self._scorer.score(word)

                # ── Apply mode filter ───────────────────────────────
                if not self._passes_filter(result.overall, result.category, result.zipf, mode_config):
                    filtered_count += 1
                    continue

                match_type = (
                    MatchType.FULL_ANAGRAM
                    if length == input_length
                    else MatchType.SUB_ANAGRAM
                )
                matches.append(
                    MatchResult(
                        word=word,
                        length=length,
                        type=match_type,
                        confidence=result.overall,
                        category=result.category,
                        zipf_score=result.zipf,
                    )
                )

        # Sort: full anagrams first → confidence desc → length desc → alpha.
        matches.sort(
            key=lambda m: (
                m.type != MatchType.FULL_ANAGRAM,  # False < True
                -m.confidence,
                -m.length,
                m.word,
            )
        )

        full_anagram_count = sum(
            1 for m in matches if m.type == MatchType.FULL_ANAGRAM
        )
        sub_anagram_count = len(matches) - full_anagram_count
        longest_word = matches[0].word if matches else None

        elapsed_ms = (time.perf_counter() - start) * 1000.0

        logger.info(
            "solve | letters=%s | mode=%s | matches=%d | filtered=%d | ms=%.2f",
            normalised,
            effective_mode.value,
            len(matches),
            filtered_count,
            elapsed_ms,
        )

        return SolveResponse(
            input=normalised,
            execution_ms=round(elapsed_ms, 3),
            total_matches=len(matches),
            full_anagram_count=full_anagram_count,
            sub_anagram_count=sub_anagram_count,
            longest_word=longest_word,
            matches=matches,
            mode=effective_mode,
            filtered_count=filtered_count,
        )

    # ------------------------------------------------------------------
    # Internals
    # ------------------------------------------------------------------

    @staticmethod
    def _is_subset(
        word_counter: dict[str, int],
        input_counter: dict[str, int],
    ) -> bool:
        """Return ``True`` if every letter in *word_counter* is available in *input_counter*."""
        return all(
            count <= input_counter.get(ch, 0)
            for ch, count in word_counter.items()
        )

    @staticmethod
    def _passes_filter(
        confidence: float,
        category: WordCategory,
        zipf: float,
        config: ModeConfig,
    ) -> bool:
        """Return ``True`` if a word passes the mode's filter criteria."""
        # Always reject INVALID in non-permissive modes.
        if category == WordCategory.INVALID and config.min_confidence > 0:
            return False

        # Confidence threshold.
        if confidence < config.min_confidence:
            return False

        # Zipf threshold.
        if config.min_zipf is not None and zipf < config.min_zipf:
            return False

        # Category-specific exclusions.
        if category == WordCategory.ABBREVIATION and not config.include_abbreviations:
            return False

        if category == WordCategory.ARCHAIC and not config.include_archaic:
            return False

        return True
