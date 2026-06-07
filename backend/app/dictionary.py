"""Dictionary loading and preprocessing service."""

import logging
from collections import Counter
from pathlib import Path

from app.models import DictionaryStats

logger = logging.getLogger(__name__)

# Pre-computed counter representation: maps each character to its count.
WordCounter = dict[str, int]


class DictionaryService:
    """Loads a word-list file and indexes words by length for fast lookups.

    Each word is stored alongside its pre-computed ``Counter`` so the solver
    never has to recompute letter frequencies at query time.
    """

    def __init__(self, path: str | Path) -> None:
        self._path = Path(path)
        # words_by_length[n] == list of (word, counter_dict) with len(word)==n
        self._words_by_length: dict[int, list[tuple[str, WordCounter]]] = {}
        self._word_count: int = 0
        self._min_length: int = 0
        self._max_length: int = 0
        self._total_length: int = 0
        self._all_words: list[str] = []

    # ------------------------------------------------------------------
    # Public API
    # ------------------------------------------------------------------

    def load(self) -> None:
        """Read the word file, filter, and build the length-bucketed index."""
        path = self._path
        if not path.is_file():
            msg = f"Dictionary file not found: {path.resolve()}"
            logger.error(msg)
            raise FileNotFoundError(msg)

        raw_count = 0
        skipped = 0
        seen: set[str] = set()
        all_words: list[str] = []

        with path.open(encoding="utf-8") as fh:
            for raw_line in fh:
                raw_count += 1
                word = raw_line.strip().lower()

                # Filter: must be purely alphabetic and at least 2 chars.
                if len(word) < 2 or not word.isalpha():
                    skipped += 1
                    continue

                # Deduplicate
                if word in seen:
                    skipped += 1
                    continue
                seen.add(word)

                counter: WordCounter = dict(Counter(word))
                length = len(word)
                self._words_by_length.setdefault(length, []).append(
                    (word, counter)
                )
                all_words.append(word)

        self._all_words = all_words
        self._word_count = len(seen)
        lengths = list(self._words_by_length.keys())
        if lengths:
            self._min_length = min(lengths)
            self._max_length = max(lengths)
        self._total_length = sum(
            length * len(bucket)
            for length, bucket in self._words_by_length.items()
        )

        logger.info(
            "dictionary loaded | path=%s | raw_lines=%d | valid_words=%d | skipped=%d | buckets=%d",
            path,
            raw_count,
            self._word_count,
            skipped,
            len(self._words_by_length),
        )

    # ------------------------------------------------------------------
    # Properties
    # ------------------------------------------------------------------

    @property
    def word_count(self) -> int:
        """Total number of valid words loaded."""
        return self._word_count

    @property
    def words_by_length(
        self,
    ) -> dict[int, list[tuple[str, WordCounter]]]:
        """Words grouped by length, each with its pre-computed counter."""
        return self._words_by_length

    @property
    def all_words(self) -> list[str]:
        """Flat list of every loaded word (for precomputing scores)."""
        return self._all_words

    @property
    def stats(self) -> DictionaryStats:
        """Compute and return dictionary statistics."""
        avg = (
            self._total_length / self._word_count
            if self._word_count
            else 0.0
        )
        return DictionaryStats(
            total_words=self._word_count,
            min_length=self._min_length,
            max_length=self._max_length,
            avg_length=round(avg, 2),
        )
