"""Tests for :mod:`app.confidence` – the scoring engine."""

from app.confidence import ConfidenceScorer
from app.models import WordCategory


class TestCommonWords:
    """Common English words should have high confidence."""

    def test_happy_high_confidence(self, scorer: ConfidenceScorer) -> None:
        result = scorer.score("happy")
        assert result.overall >= 0.7
        assert result.category == WordCategory.STANDARD
        assert result.zipf > 3.0

    def test_dog_high_confidence(self, scorer: ConfidenceScorer) -> None:
        result = scorer.score("dog")
        assert result.overall >= 0.6
        assert result.category == WordCategory.STANDARD


class TestInvalidStrings:
    """Non-words should have very low or zero confidence."""

    def test_garbage_low_confidence(self, scorer: ConfidenceScorer) -> None:
        result = scorer.score("pph")
        assert result.overall < 0.2
        assert result.category in (WordCategory.ABBREVIATION, WordCategory.INVALID)

    def test_consonant_soup(self, scorer: ConfidenceScorer) -> None:
        result = scorer.score("pp")
        assert result.overall < 0.35
        assert result.dictionary_score == 0.0


class TestScoringComponents:
    """Verify individual scoring components."""

    def test_dictionary_score_attested(self, scorer: ConfidenceScorer) -> None:
        result = scorer.score("the")
        assert result.dictionary_score == 1.0

    def test_dictionary_score_unattested(self, scorer: ConfidenceScorer) -> None:
        result = scorer.score("pph")
        assert result.dictionary_score == 0.0

    def test_frequency_score_range(self, scorer: ConfidenceScorer) -> None:
        result = scorer.score("happy")
        assert 0.0 <= result.frequency_score <= 1.0


class TestOrdering:
    """Common words should always score higher than rare/invalid ones."""

    def test_common_beats_rare(self, scorer: ConfidenceScorer) -> None:
        common = scorer.score("happy")
        rare = scorer.score("pah")
        assert common.overall > rare.overall

    def test_real_beats_invalid(self, scorer: ConfidenceScorer) -> None:
        real = scorer.score("app")
        invalid = scorer.score("pph")
        assert real.overall > invalid.overall


class TestPrecompute:
    """Verify batch precomputation."""

    def test_precompute_populates_cache(self, scorer: ConfidenceScorer) -> None:
        words = ["alpha", "beta", "gamma"]
        scorer.precompute(words)
        assert scorer.cache_size >= 3

    def test_deterministic(self, scorer: ConfidenceScorer) -> None:
        s1 = scorer.score("hello")
        s2 = scorer.score("hello")
        assert s1.overall == s2.overall
        assert s1.category == s2.category
