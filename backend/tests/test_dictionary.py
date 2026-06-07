"""Tests for :mod:`app.dictionary` – the DictionaryService."""

from pathlib import Path

import pytest

from app.dictionary import DictionaryService


class TestLoadWordCount:
    """Verify the correct number of words are loaded."""

    def test_load_word_count(self, dictionary_service: DictionaryService) -> None:
        # From conftest: dog, god, do, go, dogs, cat, act, tac, at, hello, world = 11
        # "a" is filtered (len < 2), "123" filtered (non-alpha)
        assert dictionary_service.word_count == 11


class TestFiltersShortWords:
    """Single-character words must be excluded."""

    def test_filters_short_words(self, dictionary_service: DictionaryService) -> None:
        all_words = [
            word
            for bucket in dictionary_service.words_by_length.values()
            for word, _ in bucket
        ]
        assert "a" not in all_words


class TestFiltersNonAlpha:
    """Words with digits or symbols must be excluded."""

    def test_filters_non_alpha(self, dictionary_service: DictionaryService) -> None:
        all_words = [
            word
            for bucket in dictionary_service.words_by_length.values()
            for word, _ in bucket
        ]
        assert "123" not in all_words

    def test_filters_mixed(self, tmp_path: Path) -> None:
        word_file = tmp_path / "mixed.txt"
        word_file.write_text("abc\na1b\nhello!\n--\n  \n", encoding="utf-8")
        svc = DictionaryService(word_file)
        svc.load()
        assert svc.word_count == 1  # only "abc"


class TestLowercase:
    """All loaded words must be lowercased."""

    def test_lowercase(self, dictionary_service: DictionaryService) -> None:
        for bucket in dictionary_service.words_by_length.values():
            for word, _ in bucket:
                assert word == word.lower(), f"{word!r} is not lowercase"


class TestStats:
    """Verify DictionaryStats computation."""

    def test_stats(self, dictionary_service: DictionaryService) -> None:
        stats = dictionary_service.stats
        assert stats.total_words == 11
        assert stats.min_length == 2
        assert stats.max_length == 5
        assert stats.avg_length > 0


class TestLengthBuckets:
    """Words should be correctly grouped by length."""

    def test_length_buckets(self, dictionary_service: DictionaryService) -> None:
        for length, bucket in dictionary_service.words_by_length.items():
            for word, _ in bucket:
                assert len(word) == length, (
                    f"Word {word!r} has length {len(word)} but is in bucket {length}"
                )

    def test_expected_buckets(self, dictionary_service: DictionaryService) -> None:
        assert 2 in dictionary_service.words_by_length
        assert 3 in dictionary_service.words_by_length
        assert 4 in dictionary_service.words_by_length
        assert 5 in dictionary_service.words_by_length


class TestFileNotFound:
    """Missing file should raise FileNotFoundError."""

    def test_missing_file(self) -> None:
        svc = DictionaryService("/nonexistent/path/words.txt")
        with pytest.raises(FileNotFoundError):
            svc.load()
