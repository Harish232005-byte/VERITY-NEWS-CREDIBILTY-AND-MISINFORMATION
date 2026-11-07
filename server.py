"""
Flask Web Application Server for Verity: News Credibility and Misinformation Analyzer.
Provides full REST APIs and serves the front-end dashboard.
"""

import os
import json
from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS

from backend.nlp_engine import NLPEngine
from backend.model_trainer import NewsCredibilityModel
from backend.url_scraper import scrape_article_from_url, extract_domain
from backend.fact_checker import (
    evaluate_domain, match_fact_checks, compute_composite_verity_score
)
from backend.samples import SAMPLE_ARTICLES
from backend.lexicons import DOMAIN_DATABASE, VERIFIED_FACT_CHECKS

app = Flask(__name__, static_folder="static", static_url_path="")
CORS(app)

# Initialize NLP Engine and ML Model
nlp_engine = NLPEngine()
model = NewsCredibilityModel()

print("Initializing Verity ML Classifier & Pre-training...")
model_metrics = model.train_or_load()
print(f"Model ready! Vocabulary: {model_metrics.get('vocab_size', 0)} terms | Accuracy: {model_metrics.get('accuracy', 0)}%")


@app.route("/")
def index():
    """Serve main web dashboard."""
    return send_from_directory("static", "index.html")


@app.route("/api/samples", methods=["GET"])
def get_samples():
    """Retrieve curated sample news articles for quick testing."""
    return jsonify({
        "status": "success",
        "samples": SAMPLE_ARTICLES
    })


@app.route("/api/scrape", methods=["POST"])
def scrape_url():
    """Extract news article body and metadata from URL."""
    data = request.get_json(force=True) or {}
    url = data.get("url", "").strip()

    if not url:
        return jsonify({"success": False, "error": "URL parameter is required"}), 400

    result = scrape_article_from_url(url)
    return jsonify(result)


@app.route("/api/analyze", methods=["POST"])
def analyze_article():
    """Full NLP & ML Credibility analysis pipeline."""
    data = request.get_json(force=True) or {}
    text = data.get("text", "").strip()
    title = data.get("title", "").strip()
    domain = data.get("domain", "").strip()
    url = data.get("url", "").strip()

    if url and not domain:
        domain = extract_domain(url)

    if not text:
        return jsonify({"status": "error", "message": "Text content is required for analysis."}), 400

    # Combine title into text analysis if provided
    full_text = f"{title}. {text}" if title else text

    # 1. ML Model Prediction
    model_prediction = model.predict(full_text)

    # 2. NLP Pipeline (Readability, Stylometrics, Sensationalism, Sentiment, Entities, XAI Tokens)
    nlp_results = nlp_engine.process_full_nlp_pipeline(full_text, model.feature_weights)

    # 3. Domain Evaluation
    domain_info = evaluate_domain(domain)

    # 4. Fact Check Knowledge Base Scan
    fact_matches = match_fact_checks(full_text)

    # 5. Composite Verity Score Synthesis
    verity_evaluation = compute_composite_verity_score(
        model_prediction, nlp_results, domain_info, fact_matches
    )

    return jsonify({
        "status": "success",
        "title": title or "Analyzed Article",
        "verity_evaluation": verity_evaluation,
        "model_prediction": model_prediction,
        "nlp_results": nlp_results,
        "domain_info": domain_info,
        "fact_matches": fact_matches
    })


@app.route("/api/compare", methods=["POST"])
def compare_articles():
    """Side-by-side comparative analysis of two articles."""
    data = request.get_json(force=True) or {}
    text_a = data.get("text_a", "").strip()
    title_a = data.get("title_a", "Article A").strip()
    domain_a = data.get("domain_a", "").strip()

    text_b = data.get("text_b", "").strip()
    title_b = data.get("title_b", "Article B").strip()
    domain_b = data.get("domain_b", "").strip()

    if not text_a or not text_b:
        return jsonify({"status": "error", "message": "Both text_a and text_b are required for comparison."}), 400

    def analyze_single(text, title, domain):
        full = f"{title}. {text}" if title else text
        pred = model.predict(full)
        nlp = nlp_engine.process_full_nlp_pipeline(full, model.feature_weights)
        dom = evaluate_domain(domain)
        facts = match_fact_checks(full)
        verity = compute_composite_verity_score(pred, nlp, dom, facts)
        return {
            "title": title,
            "verity": verity,
            "prediction": pred,
            "nlp": nlp,
            "domain": dom,
            "facts": facts
        }

    res_a = analyze_single(text_a, title_a, domain_a)
    res_b = analyze_single(text_b, title_b, domain_b)

    # Compute comparative delta
    score_diff = round(res_a["verity"]["verity_score"] - res_b["verity"]["verity_score"], 1)
    polarity_diff = round(res_a["nlp"]["sentiment"]["polarity"] - res_b["nlp"]["sentiment"]["polarity"], 2)
    subjectivity_diff = round(res_a["nlp"]["sentiment"]["subjectivity"] - res_b["nlp"]["sentiment"]["subjectivity"], 2)

    return jsonify({
        "status": "success",
        "article_a": res_a,
        "article_b": res_b,
        "comparison_delta": {
            "score_diff": score_diff,
            "polarity_diff": polarity_diff,
            "subjectivity_diff": subjectivity_diff,
            "higher_credibility": "Article A" if score_diff > 0 else ("Article B" if score_diff < 0 else "Equal")
        }
    })


@app.route("/api/model-stats", methods=["GET"])
def get_model_stats():
    """Return academic NLP training metrics, ROC-AUC, confusion matrix, and feature cues."""
    return jsonify({
        "status": "success",
        "metrics": model.metrics
    })


@app.route("/api/fact-checks", methods=["GET"])
def list_fact_checks():
    """List fact-check database with search query."""
    q = request.args.get("q", "").lower().strip()
    if not q:
        return jsonify({"status": "success", "fact_checks": VERIFIED_FACT_CHECKS})

    filtered = [
        fc for fc in VERIFIED_FACT_CHECKS
        if q in fc["claim"].lower() or q in fc["category"].lower() or any(q in kw for kw in fc["keywords"])
    ]
    return jsonify({"status": "success", "fact_checks": filtered})


@app.route("/api/domains", methods=["GET"])
def list_domains():
    """Return rated domains database."""
    return jsonify({
        "status": "success",
        "domains": DOMAIN_DATABASE
    })


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5050))
    print(f"\n=======================================================")
    print(f"  Verity: News Credibility and Misinformation Analyzer")
    print(f"  Running locally on http://127.0.0.1:{port}")
    print(f"=======================================================\n")
    app.run(host="0.0.0.0", port=port, debug=False)
