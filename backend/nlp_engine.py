"""
Core NLP Engine for Verity News Credibility and Misinformation Analyzer.
Provides text preprocessing, stylometric analysis, readability indexes,
sentiment & subjectivity, sensationalism scoring, entity extraction, and XAI token attributions.
"""

import re
import math
from collections import Counter
from backend.lexicons import (
    CLICKBAIT_PHRASES, WEASEL_WORDS, CREDIBLE_ATTRIBUTION_MARKERS,
    SENSATIONAL_WORDS, EMOTIONAL_LEXICON
)

# Standard English stop words list (self-contained, no external download needed)
STOPWORDS = {
    "a", "about", "above", "after", "again", "against", "all", "am", "an", "and",
    "any", "are", "aren't", "as", "at", "be", "because", "been", "before", "being",
    "below", "between", "both", "but", "by", "can't", "cannot", "could", "couldn't",
    "did", "didn't", "do", "does", "doesn't", "doing", "don't", "down", "during",
    "each", "few", "for", "from", "further", "had", "hadn't", "has", "hasn't",
    "have", "haven't", "having", "he", "he'd", "he'll", "he's", "her", "here",
    "here's", "hers", "herself", "him", "himself", "his", "how", "how's", "i",
    "i'd", "i'll", "i'm", "i've", "if", "in", "into", "is", "isn't", "it", "it's",
    "its", "itself", "let's", "me", "more", "most", "mustn't", "my", "myself",
    "no", "nor", "not", "of", "off", "on", "once", "only", "or", "other", "ought",
    "our", "ours", "ourselves", "out", "over", "own", "same", "shan't", "she",
    "she'd", "she'll", "she's", "should", "shouldn't", "so", "some", "such",
    "than", "that", "that's", "the", "their", "theirs", "them", "themselves",
    "then", "there", "there's", "these", "they", "they'd", "they'll", "they're",
    "they've", "this", "those", "through", "to", "too", "under", "until", "up",
    "very", "was", "wasn't", "we", "we'd", "we'll", "we're", "we've", "were",
    "weren't", "what", "what's", "when", "when's", "where", "where's", "which",
    "while", "who", "who's", "whom", "why", "why's", "with", "won't", "would",
    "wouldn't", "you", "you'd", "you'll", "you're", "you've", "your", "yours",
    "yourself", "yourselves"
}

# Positive and negative opinion words for Lexicon-based Sentiment & Subjectivity
POSITIVE_WORDS = {
    "good", "great", "excellent", "breakthrough", "promising", "verified", "accurate",
    "successful", "benefit", "advance", "effective", "safe", "reliable", "trustworthy",
    "positive", "progress", "vital", "significant", "superior", "valuable", "genuine"
}
NEGATIVE_WORDS = {
    "bad", "terrible", "awful", "catastrophic", "fail", "failure", "hoax", "corrupt",
    "fake", "disastrous", "destructive", "fraud", "scam", "harmful", "crisis",
    "conspiracy", "scandal", "lie", "deceit", "poison", "deadly", "danger", "evil"
}


def count_syllables(word: str) -> int:
    """Heuristic syllable counter for readability metrics."""
    word = word.lower().strip()
    if not word:
        return 0
    if len(word) <= 3:
        return 1
    # Remove common trailing suffixes that don't add syllables
    word = re.sub(r'(?:[^laeiouy]|ed|es|e)$', '', word)
    word = re.sub(r'^y', '', word)
    vowels = re.findall(r'[aeiouy]{1,2}', word)
    return max(1, len(vowels))


class NLPEngine:
    """Comprehensive Natural Language Processing engine."""

    def __init__(self):
        pass

    def tokenize(self, text: str) -> list[str]:
        """Extract lowercase word tokens."""
        return re.findall(r'\b[a-zA-Z]{2,}\b', text.lower())

    def split_sentences(self, text: str) -> list[str]:
        """Split text into sentences handling common abbreviations."""
        text = re.sub(r'(?i)\b(mr|mrs|ms|dr|prof|sr|jr|u\.s|e\.g|i\.e)\.\s*', r'\1<DOT> ', text)
        sentences = re.split(r'[.!?]+(?:\s+|\n+|$)', text)
        clean_sentences = []
        for s in sentences:
            s = s.replace('<DOT>', '.').strip()
            if len(s) > 3:
                clean_sentences.append(s)
        return clean_sentences if clean_sentences else [text.strip()]

    def analyze_readability(self, text: str, words: list[str], sentences: list[str]) -> dict:
        """Calculate standard linguistic readability and grade indices."""
        total_words = max(1, len(words))
        total_sentences = max(1, len(sentences))
        total_chars = sum(len(w) for w in words)
        total_syllables = sum(count_syllables(w) for w in words)
        complex_words = sum(1 for w in words if count_syllables(w) >= 3)

        words_per_sentence = total_words / total_sentences
        syllables_per_word = total_syllables / total_words

        # 1. Flesch Reading Ease
        # 90-100: Very Easy, 60-70: Plain English, 0-30: Very Difficult/Academic
        fre = 206.835 - (1.015 * words_per_sentence) - (84.6 * syllables_per_word)
        fre = max(0.0, min(100.0, round(fre, 1)))

        # 2. Flesch-Kincaid Grade Level
        fkgl = (0.39 * words_per_sentence) + (11.8 * syllables_per_word) - 15.59
        fkgl = max(1.0, round(fkgl, 1))

        # 3. Coleman-Liau Index
        # L = avg letters per 100 words, S = avg sentences per 100 words
        L = (total_chars / total_words) * 100
        S = (total_sentences / total_words) * 100
        coleman = 0.0588 * L - 0.296 * S - 15.8
        coleman = max(1.0, round(coleman, 1))

        # 4. Gunning Fog Index
        complex_pct = (complex_words / total_words) * 100
        gunning_fog = 0.4 * (words_per_sentence + complex_pct)
        gunning_fog = max(1.0, round(gunning_fog, 1))

        # Interpretability label
        if fre >= 80:
            level = "Elementary (Easy to read)"
        elif fre >= 60:
            level = "Standard / Mass Media"
        elif fre >= 40:
            level = "College / Professional"
        else:
            level = "Advanced / Academic / Complex"

        return {
            "flesch_reading_ease": fre,
            "flesch_kincaid_grade": fkgl,
            "coleman_liau_index": coleman,
            "gunning_fog_index": gunning_fog,
            "reading_level": level,
            "words_per_sentence": round(words_per_sentence, 1),
            "syllables_per_word": round(syllables_per_word, 2),
            "complex_word_percentage": round(complex_pct, 1)
        }

    def analyze_stylometrics(self, text: str, words: list[str], sentences: list[str]) -> dict:
        """Stylometric, lexical diversity, and syntactic indicators."""
        total_words = max(1, len(words))

        # Uppercase ratio (excessive caps indicative of spam/rage clickbait)
        alpha_chars = [c for c in text if c.isalpha()]
        upper_chars = [c for c in alpha_chars if c.isupper()]
        caps_ratio = (len(upper_chars) / len(alpha_chars)) if alpha_chars else 0.0

        # Punctuation anomalies
        exclamations = text.count('!')
        question_marks = text.count('?')
        ellipses = len(re.findall(r'\.{3,}', text))
        quotes_count = text.count('"') + text.count('“') + text.count('”')

        # Lexical Diversity: Type-Token Ratio (TTR)
        unique_tokens = len(set(words))
        ttr = unique_tokens / total_words

        # Hapax Legomena (tokens occurring exactly once, marker of vocabulary richness)
        word_counts = Counter(words)
        hapax_count = sum(1 for _, count in word_counts.items() if count == 1)
        hapax_ratio = hapax_count / total_words

        # Average word length
        avg_word_len = sum(len(w) for w in words) / total_words

        return {
            "total_words": total_words,
            "total_sentences": len(sentences),
            "caps_ratio_percent": round(caps_ratio * 100, 1),
            "exclamation_count": exclamations,
            "question_count": question_marks,
            "quotes_count": quotes_count,
            "ellipses_count": ellipses,
            "lexical_diversity_ttr": round(ttr, 3),
            "hapax_legomena_ratio": round(hapax_ratio, 3),
            "average_word_length": round(avg_word_len, 2)
        }

    def analyze_sensationalism_and_bias(self, text: str, words: list[str]) -> dict:
        """Detect clickbait triggers, sensationalism, weasel words, and attribution."""
        text_lower = text.lower()
        total_words = max(1, len(words))

        # Detect clickbait phrases
        detected_clickbait = []
        for phrase in CLICKBAIT_PHRASES:
            if phrase in text_lower:
                detected_clickbait.append(phrase)

        # Detect weasel phrases (vague anonymous attribution)
        detected_weasels = []
        for weasel in WEASEL_WORDS:
            if weasel in text_lower:
                detected_weasels.append(weasel)

        # Detect credible attribution markers
        detected_credible_markers = []
        for marker in CREDIBLE_ATTRIBUTION_MARKERS:
            if marker in text_lower:
                detected_credible_markers.append(marker)

        # Count sensational words
        sensational_hits = [w for w in words if w in SENSATIONAL_WORDS]
        sensational_density = (len(sensational_hits) / total_words) * 100

        # Calculate Sensationalism Score (0 to 100)
        sensational_score = (
            (len(detected_clickbait) * 18) +
            (len(detected_weasels) * 8) +
            (sensational_density * 8)
        )
        # Attribution dampening
        sensational_score -= (len(detected_credible_markers) * 15)
        sensational_score = max(0.0, min(100.0, round(sensational_score, 1)))

        return {
            "sensationalism_score": sensational_score,
            "sensational_words_found": list(set(sensational_hits))[:10],
            "sensational_word_count": len(sensational_hits),
            "clickbait_phrases": detected_clickbait,
            "weasel_words": detected_weasels,
            "credible_markers": detected_credible_markers
        }

    def analyze_sentiment_and_emotion(self, words: list[str]) -> dict:
        """Compute lexicon-based valence polarity, subjectivity, and emotion radar."""
        total_words = max(1, len(words))
        pos_count = sum(1 for w in words if w in POSITIVE_WORDS)
        neg_count = sum(1 for w in words if w in NEGATIVE_WORDS)

        # Polarity: -1.0 (strongly negative) to +1.0 (strongly positive)
        net_sentiment = pos_count - neg_count
        denom = max(1, pos_count + neg_count)
        polarity = round(net_sentiment / denom, 2) if (pos_count + neg_count) > 0 else 0.0

        # Subjectivity: 0.0 (purely objective/factual) to 1.0 (highly opinionated/subjective)
        opinion_words = pos_count + neg_count
        subjectivity = min(1.0, round((opinion_words * 3.5) / total_words, 2))

        # Emotion radar breakdown (Normalized 0 to 100)
        emotions = {}
        for emo, emo_words in EMOTIONAL_LEXICON.items():
            matches = sum(1 for w in words if w in emo_words)
            intensity = min(100, int((matches / max(2, total_words * 0.04)) * 100))
            emotions[emo] = intensity

        tone = "Neutral / Objective"
        if polarity > 0.35:
            tone = "Positive / Optimistic"
        elif polarity < -0.35:
            tone = "Negative / Critical"
        elif subjectivity > 0.45:
            tone = "Opinionated / Subjective"

        return {
            "polarity": polarity,
            "subjectivity": subjectivity,
            "overall_tone": tone,
            "emotion_radar": emotions
        }

    def extract_entities_and_claims(self, text: str, sentences: list[str]) -> dict:
        """Extract named entities, numerical assertions, and quoted claims."""
        # 1. Statistical/Regex Entity Extraction (Capitalized multi-word noun phrases)
        entity_patterns = re.findall(r'\b[A-Z][a-z]+(?:\s+[A-Z][a-z]+)+\b', text)
        entities = [e for e in set(entity_patterns) if len(e.split()) <= 4]

        # 2. Numerical / Statistical Claims (e.g. 50%, $10 billion, 3.4 million)
        stat_claims = re.findall(r'\b(?:\$\d+(?:\.\d+)?|\d+(?:\.\d+)?%|\d+(?:\.\d+)?\s*(?:million|billion|trillion|patients|deaths|cases|votes))\b', text, re.IGNORECASE)

        # 3. Direct Quotations
        quotes = re.findall(r'["“]([^"”]{10,250})["”]', text)

        # 4. Critical Claims / Assertions (sentences containing causal or dramatic verbs)
        assertion_sentences = []
        assertion_keywords = ["caused", "proves", "discovered", "concluded", "reveals", "confirmed", "linked to", "claims that", "warns"]
        for s in sentences:
            s_lower = s.lower()
            if any(k in s_lower for k in assertion_keywords):
                assertion_sentences.append(s)

        return {
            "named_entities": entities[:8],
            "statistical_claims": list(set(stat_claims))[:8],
            "direct_quotes": quotes[:5],
            "key_assertions": assertion_sentences[:4]
        }

    def generate_token_attributions(self, text: str, words: list[str], model_feature_weights: dict = None) -> list[dict]:
        """
        Explainable AI (XAI) feature attribution generator.
        Assigns each token an attribution tag:
        'credible' (green), 'suspicious' (red), 'sensational' (amber), or 'neutral'.
        """
        tokens = re.findall(r'\b\w+\b|[^\w\s]', text)
        attributions = []

        feature_weights = model_feature_weights or {}

        for token in tokens[:300]:  # Cap at first 300 tokens for smooth DOM rendering
            low = token.lower()
            if not token.isalnum():
                attributions.append({"token": token, "type": "punct", "weight": 0.0, "reason": ""})
                continue

            weight = feature_weights.get(low, 0.0)

            if low in SENSATIONAL_WORDS or low in CLICKBAIT_PHRASES:
                attributions.append({
                    "token": token,
                    "type": "sensational",
                    "weight": round(weight if weight != 0 else 0.75, 2),
                    "reason": "Sensational or emotionally charged terminology"
                })
            elif weight > 0.35:
                attributions.append({
                    "token": token,
                    "type": "credible",
                    "weight": round(weight, 2),
                    "reason": "Features correlating strongly with verified journalistic reporting"
                })
            elif weight < -0.35:
                attributions.append({
                    "token": token,
                    "type": "suspicious",
                    "weight": round(weight, 2),
                    "reason": "Features correlating with unverified or deceptive text patterns"
                })
            elif low in POSITIVE_WORDS or low in EMOTIONAL_LEXICON["trust"]:
                attributions.append({
                    "token": token,
                    "type": "credible",
                    "weight": 0.3,
                    "reason": "Institutional/scientific consensus vocabulary"
                })
            elif low in WEASEL_WORDS:
                attributions.append({
                    "token": token,
                    "type": "suspicious",
                    "weight": -0.4,
                    "reason": "Weasel word / unsubstantiated attribution"
                })
            else:
                attributions.append({
                    "token": token,
                    "type": "neutral",
                    "weight": 0.0,
                    "reason": "Common linguistic context"
                })

        return attributions

    def process_full_nlp_pipeline(self, text: str, model_weights: dict = None) -> dict:
        """Run all NLP stages and combine into a unified feature set."""
        words = self.tokenize(text)
        sentences = self.split_sentences(text)

        readability = self.analyze_readability(text, words, sentences)
        stylometrics = self.analyze_stylometrics(text, words, sentences)
        sensationalism = self.analyze_sensationalism_and_bias(text, words)
        sentiment = self.analyze_sentiment_and_emotion(words)
        entities_and_claims = self.extract_entities_and_claims(text, sentences)
        token_attributions = self.generate_token_attributions(text, words, model_weights)

        return {
            "readability": readability,
            "stylometrics": stylometrics,
            "sensationalism": sensationalism,
            "sentiment": sentiment,
            "entities_and_claims": entities_and_claims,
            "token_attributions": token_attributions
        }
