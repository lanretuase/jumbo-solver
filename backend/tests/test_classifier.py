"""Tests for :mod:`app.word_classifier` – the NLP classification engine."""

from app.models import WordCategory
from app.word_classifier import WordClassifier


class TestStandardWords:
    """Common English words should be classified as STANDARD."""

    def test_common_words(self, classifier: WordClassifier) -> None:
        for word in ("happy", "dog", "cat", "hello", "world", "the"):
            assert classifier.classify(word) == WordCategory.STANDARD, f"{word} should be STANDARD"

    def test_short_common_words(self, classifier: WordClassifier) -> None:
        for word in ("do", "go", "at", "ah", "ha"):
            assert classifier.classify(word) == WordCategory.STANDARD, f"{word} should be STANDARD"


class TestAbbreviations:
    """Consonant-only short strings should be ABBREVIATION."""

    def test_consonant_only_two_chars(self, classifier: WordClassifier) -> None:
        for word in ("hp", "pp", "ph"):
            assert classifier.classify(word) == WordCategory.ABBREVIATION, f"{word} should be ABBREVIATION"

    def test_consonant_only_three_chars(self, classifier: WordClassifier) -> None:
        for word in ("pph", "bcd"):
            assert classifier.classify(word) == WordCategory.ABBREVIATION, f"{word} should be ABBREVIATION"


class TestInvalidStrings:
    """Non-words with vowels but zero frequency should be INVALID."""

    def test_short_zero_freq(self, classifier: WordClassifier) -> None:
        # 3-letter strings with vowels but no corpus attestation
        result = classifier.classify("pya")
        assert result in (WordCategory.INVALID, WordCategory.ARCHAIC)

    def test_two_char_zero_freq(self, classifier: WordClassifier) -> None:
        result = classifier.classify("ap")
        assert result in (WordCategory.INVALID, WordCategory.ABBREVIATION)


class TestCaching:
    """Verify the internal cache works correctly."""

    def test_cache_hit(self, classifier: WordClassifier) -> None:
        cat1 = classifier.classify("dog")
        cat2 = classifier.classify("dog")
        assert cat1 == cat2
        assert classifier.cache_size >= 1

    def test_batch_classification(self, classifier: WordClassifier) -> None:
        results = classifier.classify_batch(["dog", "cat", "hp"])
        assert results["dog"] == WordCategory.STANDARD
        assert results["cat"] == WordCategory.STANDARD
        assert results["hp"] == WordCategory.ABBREVIATION


class TestZipfScores:
    """Verify raw Zipf lookup works."""

    def test_common_word_has_high_zipf(self, classifier: WordClassifier) -> None:
        assert classifier.get_zipf("happy") > 3.0

    def test_garbage_has_zero_zipf(self, classifier: WordClassifier) -> None:
        assert classifier.get_zipf("xyzqw") == 0.0
