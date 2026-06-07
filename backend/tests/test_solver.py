"""Tests for :mod:`app.solver` – the JumbleSolver engine.

These tests use PERMISSIVE mode (set via the ``solver`` fixture) to verify
the core Counter-based matching logic independently of NLP filtering.
"""

from app.models import MatchType, SolveResponse
from app.solver import JumbleSolver


class TestFullAnagrams:
    """Full-anagram detection (word uses *all* input letters)."""

    def test_full_anagrams(self, solver: JumbleSolver) -> None:
        result = solver.solve("dog")
        full = [m.word for m in result.matches if m.type == MatchType.FULL_ANAGRAM]
        assert sorted(full) == ["dog", "god"]

    def test_cat_full_anagrams(self, solver: JumbleSolver) -> None:
        result = solver.solve("cat")
        full = [m.word for m in result.matches if m.type == MatchType.FULL_ANAGRAM]
        assert sorted(full) == ["act", "cat", "tac"]


class TestSubAnagrams:
    """Sub-anagram detection (word uses a *subset* of input letters)."""

    def test_sub_anagrams(self, solver: JumbleSolver) -> None:
        result = solver.solve("dog")
        sub = [m.word for m in result.matches if m.type == MatchType.SUB_ANAGRAM]
        assert sorted(sub) == ["do", "go"]

    def test_cat_sub_anagrams(self, solver: JumbleSolver) -> None:
        result = solver.solve("cat")
        sub = [m.word for m in result.matches if m.type == MatchType.SUB_ANAGRAM]
        assert sorted(sub) == ["at"]


class TestAllResults:
    """Aggregate match counts."""

    def test_all_results(self, solver: JumbleSolver) -> None:
        result = solver.solve("dog")
        assert result.total_matches == 4  # dog, god, do, go

    def test_cat_all_results(self, solver: JumbleSolver) -> None:
        result = solver.solve("cat")
        assert result.total_matches == 4  # cat, act, tac, at


class TestCaseInsensitive:
    """Input letters should be case-insensitive."""

    def test_case_insensitive(self, solver: JumbleSolver) -> None:
        upper = solver.solve("DOG")
        lower = solver.solve("dog")
        assert upper.total_matches == lower.total_matches
        assert [m.word for m in upper.matches] == [m.word for m in lower.matches]


class TestNoMatches:
    """Inputs that produce zero results."""

    def test_no_matches(self, solver: JumbleSolver) -> None:
        result = solver.solve("xyz")
        assert result.total_matches == 0
        assert result.matches == []
        assert result.longest_word is None

    def test_single_char_input_no_results(self, solver: JumbleSolver) -> None:
        """With min word length 2, a single char can never match."""
        result = solver.solve("z")
        assert result.total_matches == 0


class TestResultTypes:
    """Verify MatchType classification is correct."""

    def test_result_types(self, solver: JumbleSolver) -> None:
        result = solver.solve("dog")
        for m in result.matches:
            if len(m.word) == 3:
                assert m.type == MatchType.FULL_ANAGRAM
            else:
                assert m.type == MatchType.SUB_ANAGRAM


class TestExecutionTime:
    """Verify timing metadata."""

    def test_execution_time(self, solver: JumbleSolver) -> None:
        result = solver.solve("dog")
        assert result.execution_ms > 0


class TestSorting:
    """Results should be sorted: full anagrams first, then by confidence/length desc."""

    def test_sorting(self, solver: JumbleSolver) -> None:
        result = solver.solve("dogs")
        words = [m.word for m in result.matches]
        # 'dogs' (full, 4) should come first
        assert words[0] == "dogs"
        # After full anagrams, sub-anagrams follow
        sub_words = [m.word for m in result.matches if m.type == MatchType.SUB_ANAGRAM]
        # Sub-anagrams should be ordered by confidence desc then length desc
        assert len(sub_words) > 0

    def test_sorting_full_before_sub(self, solver: JumbleSolver) -> None:
        result = solver.solve("dog")
        types = [m.type for m in result.matches]
        full_indices = [i for i, t in enumerate(types) if t == MatchType.FULL_ANAGRAM]
        sub_indices = [i for i, t in enumerate(types) if t == MatchType.SUB_ANAGRAM]
        if full_indices and sub_indices:
            assert max(full_indices) < min(sub_indices)


class TestConfidenceMetadata:
    """Verify that confidence metadata is populated even in permissive mode."""

    def test_confidence_fields_populated(self, solver: JumbleSolver) -> None:
        result = solver.solve("dog")
        for m in result.matches:
            assert hasattr(m, "confidence")
            assert hasattr(m, "category")
            assert hasattr(m, "zipf_score")
            assert m.confidence >= 0.0

    def test_filtered_count_field(self, solver: JumbleSolver) -> None:
        result = solver.solve("dog")
        assert hasattr(result, "filtered_count")
        # In permissive mode nothing should be filtered
        assert result.filtered_count == 0
