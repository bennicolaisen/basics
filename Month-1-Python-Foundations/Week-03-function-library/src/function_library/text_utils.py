"""Pure text-processing functions."""


def word_count(text: str) -> int:
    """Number of whitespace-separated words in `text`.

    `str.split()` with no arguments splits on any run of whitespace and
    discards leading/trailing whitespace, so `"  a  b "` correctly counts
    as 2, not 3 (from an empty leading token) or a crash.
    """
    return len(text.split())


def is_palindrome(s: str, ignore_case: bool = True, ignore_spaces: bool = True) -> bool:
    """Whether `s` reads the same forwards and backwards.

    `ignore_case` and `ignore_spaces` default to True because "is this a
    palindrome" almost always means "ignoring case and spacing" in casual
    use (e.g. "A man a plan a canal Panama"); pass either as False to
    require an exact character-for-character match instead.
    """
    processed = s
    if ignore_spaces:
        processed = "".join(processed.split())
    if ignore_case:
        processed = processed.lower()
    return processed == processed[::-1]
