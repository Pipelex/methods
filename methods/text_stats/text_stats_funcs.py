"""Deterministic text statistics for the text_stats method.

The single @pipe_func here computes every statistic in pure Python (stdlib only) and renders
them as a Markdown report: no LLM, no network, no randomness. It runs in-process locally and
inside the network-blocked sandbox on hosted deployments.
"""

import re
from collections import Counter

from pipelex.core.memory.working_memory import WorkingMemory
from pipelex.core.stuffs.text_content import TextContent
from pipelex.system.registries.func_registry import pipe_func

WORD_PATTERN = re.compile(r"[^\W_]+(?:['’-][^\W_]+)*", re.UNICODE)
SENTENCE_SPLIT_PATTERN = re.compile(r"(?<=[.!?…])\s+")
PARAGRAPH_SPLIT_PATTERN = re.compile(r"\n\s*\n")

READING_WORDS_PER_MINUTE = 238
SPEAKING_WORDS_PER_MINUTE = 130
TOP_WORDS_LIMIT = 10

STOP_WORDS = frozenset(
    {
        "a", "all", "also", "an", "and", "any", "are", "as", "at", "be", "but", "by", "can",
        "could", "did", "do", "does", "each", "few", "for", "from", "had", "has", "have",
        "he", "her", "his", "how", "i", "if", "in", "into", "is", "it", "its", "just",
        "more", "most", "no", "not", "of", "on", "or", "our", "own", "same", "she", "should",
        "so", "some", "than", "that", "the", "their", "them", "then", "there", "these",
        "they", "this", "to", "too", "very", "was", "we", "were", "what", "when", "where",
        "which", "who", "why", "will", "with", "would", "you", "your",
    }
)


def format_duration(*, seconds: float) -> str:
    """Format a duration in seconds as a compact human-readable string."""
    total_seconds = max(1, round(seconds))
    minutes, remainder_seconds = divmod(total_seconds, 60)
    if minutes == 0:
        return f"{remainder_seconds} s"
    if remainder_seconds == 0:
        return f"{minutes} min"
    return f"{minutes} min {remainder_seconds} s"


@pipe_func()
async def text_stats_report(working_memory: WorkingMemory) -> TextContent:
    """Compute deterministic statistics about the input text and render them as Markdown."""
    text = working_memory.get_stuff_as_str(name="text")

    words = WORD_PATTERN.findall(text)
    lowercased_words = [word.lower() for word in words]
    word_count = len(words)
    unique_word_count = len(set(lowercased_words))

    stripped_text = text.strip()
    sentences = [segment for segment in SENTENCE_SPLIT_PATTERN.split(stripped_text) if WORD_PATTERN.search(segment)] if stripped_text else []
    paragraphs = [segment for segment in PARAGRAPH_SPLIT_PATTERN.split(stripped_text) if WORD_PATTERN.search(segment)] if stripped_text else []

    character_count = len(text)
    character_count_no_spaces = sum(1 for character in text if not character.isspace())

    lines: list[str] = ["# Text statistics", ""]

    lines.append("## Counts")
    lines.append("")
    lines.append("| Metric | Value |")
    lines.append("|---|---|")
    lines.append(f"| Characters (with spaces) | {character_count} |")
    lines.append(f"| Characters (without spaces) | {character_count_no_spaces} |")
    lines.append(f"| Words | {word_count} |")
    lines.append(f"| Unique words | {unique_word_count} |")
    lines.append(f"| Sentences | {len(sentences)} |")
    lines.append(f"| Paragraphs | {len(paragraphs)} |")
    lines.append("")

    lines.append("## Averages")
    lines.append("")
    if word_count > 0:
        average_word_length = sum(len(word) for word in words) / word_count
        lines.append(f"- Average word length: {average_word_length:.1f} characters")
        if sentences:
            lines.append(f"- Average sentence length: {word_count / len(sentences):.1f} words")
        vocabulary_richness = 100.0 * unique_word_count / word_count
        lines.append(f"- Vocabulary richness (unique / total words): {vocabulary_richness:.1f}%")
    else:
        lines.append("- No words found in the input text.")
    lines.append("")

    lines.append("## Estimated times")
    lines.append("")
    if word_count > 0:
        reading_duration = format_duration(seconds=60.0 * word_count / READING_WORDS_PER_MINUTE)
        speaking_duration = format_duration(seconds=60.0 * word_count / SPEAKING_WORDS_PER_MINUTE)
        lines.append(f"- Reading time ({READING_WORDS_PER_MINUTE} wpm): {reading_duration}")
        lines.append(f"- Speaking time ({SPEAKING_WORDS_PER_MINUTE} wpm): {speaking_duration}")
    else:
        lines.append("- Not applicable: no words found.")
    lines.append("")

    lines.append("## Most frequent words")
    lines.append("")
    content_words = [word for word in lowercased_words if len(word) >= 3 and word not in STOP_WORDS]
    if content_words:
        frequencies = Counter(content_words)
        ranked = sorted(frequencies.items(), key=lambda item: (-item[1], item[0]))[:TOP_WORDS_LIMIT]
        for rank, (word, count) in enumerate(ranked, start=1):
            occurrences = "occurrence" if count == 1 else "occurrences"
            lines.append(f"{rank}. `{word}` — {count} {occurrences}")
    else:
        lines.append("- No content words found (after removing stop words).")

    return TextContent(text="\n".join(lines))
