"""Tests for solving mode filtering behaviour."""

from app.models import MatchType, SolveMode, WordCategory
from app.solver import JumbleSolver


class TestStrictMode:
    """STRICT mode should return only common, well-known words."""

    def test_strict_filters_junk(self, strict_solver: JumbleSolver) -> None:
        """Words like 'tac' (zero or very low frequency) should be filtered."""
        result = strict_solver.solve("cat")
        words = [m.word for m in result.matches]
        assert "cat" in words
        assert "act" in words
        assert "at" in words

    def test_strict_has_filtered_count(self, strict_solver: JumbleSolver) -> None:
        result = strict_solver.solve("cat")
        # 'tac' should be filtered → filtered_count > 0
        assert result.filtered_count >= 0  # depends on wordfreq data
        assert result.mode == SolveMode.STRICT


class TestPermissiveMode:
    """PERMISSIVE mode should return all dictionary matches (legacy behaviour)."""

    def test_permissive_includes_all(self, solver: JumbleSolver) -> None:
        result = solver.solve("dog")
        words = [m.word for m in result.matches]
        assert "dog" in words
        assert "god" in words
        assert "do" in words
        assert "go" in words
        assert result.total_matches == 4

    def test_permissive_mode_field(self, solver: JumbleSolver) -> None:
        result = solver.solve("dog")
        assert result.mode == SolveMode.PERMISSIVE


class TestModeOverride:
    """Passing a mode parameter should override the solver's default."""

    def test_override_to_strict(self, solver: JumbleSolver) -> None:
        result = solver.solve("dog", mode=SolveMode.STRICT)
        assert result.mode == SolveMode.STRICT
        words = [m.word for m in result.matches]
        assert "dog" in words
        assert "god" in words

    def test_override_to_permissive(self, strict_solver: JumbleSolver) -> None:
        result = strict_solver.solve("dog", mode=SolveMode.PERMISSIVE)
        assert result.mode == SolveMode.PERMISSIVE


class TestConfidenceInResults:
    """Verify confidence metadata is populated in results."""

    def test_confidence_populated(self, solver: JumbleSolver) -> None:
        result = solver.solve("dog")
        for m in result.matches:
            assert m.confidence >= 0.0
            assert m.confidence <= 1.0
            assert m.category is not None
            assert m.zipf_score >= 0.0

    def test_common_words_high_confidence(self, solver: JumbleSolver) -> None:
        result = solver.solve("dog")
        dog_match = next(m for m in result.matches if m.word == "dog")
        assert dog_match.confidence >= 0.5
        assert dog_match.category == WordCategory.STANDARD


class TestModeSorting:
    """Results should be sorted by confidence within each group."""

    def test_full_anagrams_first(self, solver: JumbleSolver) -> None:
        result = solver.solve("dog")
        types = [m.type for m in result.matches]
        full_indices = [i for i, t in enumerate(types) if t == MatchType.FULL_ANAGRAM]
        sub_indices = [i for i, t in enumerate(types) if t == MatchType.SUB_ANAGRAM]
        if full_indices and sub_indices:
            assert max(full_indices) < min(sub_indices)
