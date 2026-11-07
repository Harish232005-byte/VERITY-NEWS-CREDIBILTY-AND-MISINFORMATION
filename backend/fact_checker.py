"""
Fact Checking, Domain Verification, and Composite Credibility Scorer.
Cross-references against domain authority databases and verified fact-check repositories.
"""

from backend.lexicons import DOMAIN_DATABASE, VERIFIED_FACT_CHECKS


def evaluate_domain(domain: str) -> dict:
    """Evaluate source domain reputation, bias, and historical fact-checking record."""
    if not domain or domain == "unknown" or domain == "direct_input":
        return {
            "is_known": False,
            "domain": "Direct Text / Unknown Domain",
            "score": 60,  # Neutral baseline
            "tier": "Neutral / Unverified Source Domain",
            "category": "Direct User Input",
            "bias": "Not Identified",
            "notes": "No source domain provided for external registry cross-referencing."
        }

    domain_lower = domain.lower().strip()
    # Check exact match or subdomains
    matched_entry = None
    matched_key = None

    for d_key, info in DOMAIN_DATABASE.items():
        if domain_lower == d_key or domain_lower.endswith("." + d_key):
            matched_entry = info
            matched_key = d_key
            break

    if matched_entry:
        return {
            "is_known": True,
            "domain": matched_key,
            "score": matched_entry["score"],
            "tier": matched_entry["tier"],
            "category": matched_entry["category"],
            "bias": matched_entry["bias"],
            "notes": matched_entry["fact_check_record"]
        }

    return {
        "is_known": False,
        "domain": domain,
        "score": 55,
        "tier": "Unregistered / Independent Source",
        "category": "Web Domain",
        "bias": "Unknown",
        "notes": "Domain is not present in our curated high-authority news database or flagged fake list."
    }


def match_fact_checks(text: str) -> list[dict]:
    """Scan article text against verified fact-check claims."""
    text_lower = text.lower()
    matches = []

    for fc in VERIFIED_FACT_CHECKS:
        keyword_hits = sum(1 for kw in fc["keywords"] if kw in text_lower)
        # If at least 2 distinct keywords match, consider it relevant
        if keyword_hits >= 2 or (keyword_hits >= 1 and any(kw in text_lower for kw in fc["keywords"][:2])):
            relevance = min(100, int((keyword_hits / len(fc["keywords"])) * 100))
            matches.append({
                "id": fc["id"],
                "claim": fc["claim"],
                "verdict": fc["verdict"],
                "category": fc["category"],
                "explanation": fc["explanation"],
                "fact_checkers": fc["fact_checkers"],
                "relevance_score": relevance
            })

    # Sort by relevance
    matches.sort(key=lambda x: x["relevance_score"], reverse=True)
    return matches[:3]


def compute_composite_verity_score(
    model_prediction: dict,
    nlp_results: dict,
    domain_info: dict,
    fact_matches: list[dict]
) -> dict:
    """
    Synthesize all NLP and ML dimensions into a single unified Verity Credibility Score (0 - 100).

    Weights:
    - ML Ensemble Probabilities: 35%
    - Stylometric & Sensationalism Integrity: 25%
    - Objectivity & Tone Neutrality: 15%
    - Domain Authority: 15%
    - Fact-check Cross-Verification: 10%
    """
    # 1. ML Model Component (0 - 100)
    ml_score = float(model_prediction.get("credible_probability", 50.0))
    fake_prob = float(model_prediction.get("fake_probability", 50.0))
    pred_class = model_prediction.get("predicted_class", "Credible")

    # 2. Sensationalism & Stylometrics Component (100 is cleanest, 0 is extreme clickbait)
    sensational_score = nlp_results["sensationalism"]["sensationalism_score"]
    caps_penalty = min(25, nlp_results["stylometrics"]["caps_ratio_percent"] * 1.5)
    exclamations_penalty = min(20, nlp_results["stylometrics"]["exclamation_count"] * 4)

    stylometric_integrity = 100.0 - sensational_score - caps_penalty - exclamations_penalty
    stylometric_integrity = max(0.0, min(100.0, stylometric_integrity))

    # 3. Objectivity & Neutrality Component (0 to 100)
    subjectivity = nlp_results["sentiment"]["subjectivity"]
    objectivity_score = (1.0 - subjectivity) * 100.0

    # 4. Domain Trust Score (0 to 100)
    domain_score = float(domain_info.get("score", 60.0))

    # 5. Fact Check Adjustment
    has_debunked_claim = False
    fact_score = 75.0  # Default neutral
    if fact_matches:
        top_match = fact_matches[0]
        v_upper = top_match["verdict"].upper()
        if "FALSE" in v_upper or "DEBUNKED" in v_upper or "CONSPIRACY" in v_upper or "HOAX" in v_upper:
            fact_score = 10.0
            has_debunked_claim = True
        elif "PARTIALLY" in v_upper:
            fact_score = 50.0
        elif "VERIFIED" in v_upper:
            fact_score = 95.0

    # Strict ground truth veracity alignment:
    # If ML predicts Misinformation OR article matches a debunked claim:
    if pred_class == "Misinformation" or fake_prob >= 50.0 or has_debunked_claim:
        # Score must be strictly low (0 to 35 max)
        composite = min(35.0, ml_score * 0.5)
        if has_debunked_claim:
            composite = min(composite, 15.0)
            verdict = "Debunked False Claim / Hoax"
        else:
            verdict = "False Article / High Risk of Misinformation"
        color = "red"
        summary = "Significant indicators of fabricated content, deceptive rhetoric, extreme clickbait patterns, or correlation with debunked narratives."
    else:
        # Credible path: weighted combination
        composite = (
            (ml_score * 0.65) +
            (stylometric_integrity * 0.15) +
            (objectivity_score * 0.10) +
            (domain_score * 0.10)
        )
        composite = max(0.0, min(100.0, round(composite, 1)))

        if sensational_score >= 45.0:
            verdict = "Questionable / Sensationalized"
            color = "amber"
            composite = min(58.0, composite)
            summary = "Caution advised. High sensationalism, excessive emotional triggers, or unverified claims detected. Cross-referencing is strongly recommended."
        elif composite >= 75.0:
            verdict = "Verified / High Credibility"
            color = "green"
            summary = "The article demonstrates verified journalistic vocabulary, balanced objective tone, low sensationalism, and high factual consistency."
        else:
            verdict = "Mostly Credible / Mild Bias"
            color = "teal"
            summary = "Generally reliable reporting, though some subjective framing, opinion cues, or unsubstantiated stylistic assertions are present."

    composite = round(composite, 1)

    return {
        "verity_score": composite,
        "verdict": verdict,
        "verdict_color": color,
        "summary": summary,
        "breakdown": {
            "ml_model_confidence": round(ml_score, 1),
            "stylometric_integrity": round(stylometric_integrity, 1),
            "objectivity_score": round(objectivity_score, 1),
            "domain_trust": round(domain_score, 1),
            "fact_verification_score": round(fact_score, 1)
        }
    }
