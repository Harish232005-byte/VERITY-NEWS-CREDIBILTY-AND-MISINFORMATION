/**
 * Verity: News Credibility and Misinformation Analyzer
 * Front-end Application Controller & Data Visualization Logic
 */

document.addEventListener("DOMContentLoaded", () => {
  // Global State
  let samplesData = [];
  let emotionChart = null;

  // DOM Elements
  const navTabs = document.querySelectorAll(".nav-tab");
  const tabContents = document.querySelectorAll(".tab-content");

  const sampleChipsContainer = document.getElementById("sample-chips");
  const urlInput = document.getElementById("url-input");
  const btnFetchUrl = document.getElementById("btn-fetch-url");
  const articleTitle = document.getElementById("article-title");
  const articleDomain = document.getElementById("article-domain");
  const articleText = document.getElementById("article-text");
  const charWordCount = document.getElementById("char-word-count");
  const btnClear = document.getElementById("btn-clear");
  const btnAnalyze = document.getElementById("btn-analyze");

  const analysisLoader = document.getElementById("analysis-loader");
  const resultsDashboard = document.getElementById("results-dashboard");

  // Initial Load
  initTabs();
  initTextCounter();
  loadSampleChips();
  loadModelMetrics();
  loadFactCheckLibrary();
  initComparativeDemo();

  /* =========================================================================
     1. TAB NAVIGATION
     ========================================================================= */
  function initTabs() {
    navTabs.forEach((tab) => {
      tab.addEventListener("click", () => {
        const targetId = tab.dataset.tab;
        navTabs.forEach((t) => t.classList.remove("active"));
        tabContents.forEach((c) => c.classList.remove("active"));

        tab.classList.add("active");
        const targetContent = document.getElementById(targetId);
        if (targetContent) {
          targetContent.classList.add("active");
        }
      });
    });
  }

  /* =========================================================================
     2. WORD & CHAR COUNTER
     ========================================================================= */
  function initTextCounter() {
    articleText.addEventListener("input", () => {
      const text = articleText.value.trim();
      const words = text ? text.split(/\s+/).length : 0;
      const chars = text.length;
      charWordCount.textContent = `${words} words | ${chars} characters`;
    });
  }

  /* =========================================================================
     3. LOAD CURATED BENCHMARK SAMPLES
     ========================================================================= */
  async function loadSampleChips() {
    try {
      const res = await fetch("/api/samples");
      const data = await res.json();
      if (data.status === "success" && data.samples) {
        samplesData = data.samples;
        renderSampleChips();
      }
    } catch (err) {
      console.error("Failed to load sample articles:", err);
    }
  }

  function renderSampleChips() {
    sampleChipsContainer.innerHTML = "";
    samplesData.forEach((sample, idx) => {
      const btn = document.createElement("button");
      btn.className = "chip-btn";
      btn.textContent = `${idx + 1}. ${sample.category}`;
      btn.title = sample.title;
      btn.addEventListener("click", () => {
        articleTitle.value = sample.title;
        articleDomain.value = sample.source.includes("reuters")
          ? "reuters.com"
          : sample.source.includes("NASA")
          ? "nature.com"
          : "unverified-source.com";
        articleText.value = sample.text;
        articleText.dispatchEvent(new Event("input"));
        // Smooth scroll to action bar
        articleText.scrollIntoView({ behavior: "smooth", block: "center" });
      });
      sampleChipsContainer.appendChild(btn);
    });
  }

  /* =========================================================================
     4. URL EXTRACTION / SCRAPER
     ========================================================================= */
  btnFetchUrl.addEventListener("click", async () => {
    const url = urlInput.value.trim();
    if (!url) {
      alert("Please paste a valid article URL.");
      return;
    }

    btnFetchUrl.disabled = true;
    btnFetchUrl.innerHTML = `<span class="btn-text">Extracting...</span>`;

    try {
      const res = await fetch("/api/scrape", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ url }),
      });
      const data = await res.json();

      if (data.success) {
        articleTitle.value = data.title || "";
        articleDomain.value = data.domain || "";
        articleText.value = data.body_text || "";
        articleText.dispatchEvent(new Event("input"));
      } else {
        alert(data.error || "Failed to extract article content from URL.");
      }
    } catch (err) {
      alert("Error contacting article extractor service: " + err.message);
    } finally {
      btnFetchUrl.disabled = false;
      btnFetchUrl.innerHTML = `<span class="btn-text">Extract Article</span>`;
    }
  });

  /* =========================================================================
     5. CLEAR BUTTON
     ========================================================================= */
  btnClear.addEventListener("click", () => {
    urlInput.value = "";
    articleTitle.value = "";
    articleDomain.value = "";
    articleText.value = "";
    articleText.dispatchEvent(new Event("input"));
    resultsDashboard.classList.add("hidden");
  });

  /* =========================================================================
     6. ANALYZE BUTTON & API DISPATCH
     ========================================================================= */
  btnAnalyze.addEventListener("click", async () => {
    const text = articleText.value.trim();
    const title = articleTitle.value.trim();
    const domain = articleDomain.value.trim();
    const url = urlInput.value.trim();

    if (!text) {
      alert("Please provide article text or choose a benchmark sample above.");
      articleText.focus();
      return;
    }

    btnAnalyze.disabled = true;
    analysisLoader.classList.remove("hidden");
    resultsDashboard.classList.add("hidden");
    analysisLoader.scrollIntoView({ behavior: "smooth", block: "center" });

    try {
      const res = await fetch("/api/analyze", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ text, title, domain, url }),
      });
      const data = await res.json();

      if (data.status === "success") {
        renderAnalysisResults(data);
        resultsDashboard.classList.remove("hidden");
        resultsDashboard.scrollIntoView({ behavior: "smooth", block: "start" });
      } else {
        alert(data.message || "Analysis failed.");
      }
    } catch (err) {
      alert("Network error executing NLP analysis: " + err.message);
    } finally {
      btnAnalyze.disabled = false;
      analysisLoader.classList.add("hidden");
    }
  });

  /* =========================================================================
     7. RENDER DASHBOARD RESULTS
     ========================================================================= */
  function renderAnalysisResults(data) {
    const evalData = data.verity_evaluation;
    const nlp = data.nlp_results;
    const modelPred = data.model_prediction;
    const domain = data.domain_info;
    const facts = data.fact_matches;

    // 1. Verdict & Gauge
    const score = Math.round(evalData.verity_score);
    document.getElementById("gauge-score-value").textContent = score;

    // Gauge circle stroke calculation (circumference = 2 * PI * 42 ~= 263.89)
    const circumference = 264;
    const offset = circumference - (score / 100) * circumference;
    const gaugeFill = document.getElementById("gauge-circle-fill");
    gaugeFill.style.strokeDashoffset = offset;

    // Color coordination
    let gaugeColor = "#10b981"; // Emerald
    let badgeClass = "badge-green";
    if (score < 40) {
      gaugeColor = "#ef4444"; // Red
      badgeClass = "badge-red";
    } else if (score < 60) {
      gaugeColor = "#f59e0b"; // Amber
      badgeClass = "badge-amber";
    } else if (score < 80) {
      gaugeColor = "#14b8a6"; // Teal
      badgeClass = "badge-teal";
    }
    gaugeFill.style.stroke = gaugeColor;

    const verdictBadge = document.getElementById("verdict-badge");
    verdictBadge.className = `verdict-badge ${badgeClass}`;
    verdictBadge.textContent = evalData.verdict;

    document.getElementById("source-badge").textContent = `Source: ${domain.domain} (${domain.tier})`;
    document.getElementById("verdict-title").textContent = data.title || "Untitled Article";
    document.getElementById("verdict-summary").textContent = evalData.summary;

    // 2. Breakdown Factor Bars
    const bk = evalData.breakdown;
    setFactor("factor-ml", "fill-ml", bk.ml_model_confidence);
    setFactor("factor-stylo", "fill-stylo", bk.stylometric_integrity);
    setFactor("factor-obj", "fill-obj", bk.objectivity_score);
    setFactor("factor-dom", "fill-dom", bk.domain_trust);
    setFactor("factor-fact", "fill-fact", bk.fact_verification_score);

    // 3. Explainable AI (XAI) Tokens
    renderXAITokens(nlp.token_attributions);

    // 4. Readability Metrics
    renderReadability(nlp.readability, nlp.stylometrics);

    // 5. Emotion Radar Chart & Sentiment
    renderEmotionChart(nlp.sentiment);

    // 6. Sensationalism & Weasel Words
    renderSensationalism(nlp.sensationalism);

    // 7. Extracted Entities & Claims
    renderEntitiesAndClaims(nlp.entities_and_claims);

    // 8. Fact-Check Matches
    renderFactMatches(facts);
  }

  function setFactor(textId, fillId, val) {
    const v = Math.round(val);
    document.getElementById(textId).textContent = `${v}%`;
    const fill = document.getElementById(fillId);
    fill.style.width = `${v}%`;
    if (v < 40) fill.style.background = "#ef4444";
    else if (v < 65) fill.style.background = "#f59e0b";
    else fill.style.background = "linear-gradient(90deg, #06b6d4, #10b981)";
  }

  /* =========================================================================
     8. EXPLAINABLE AI TOKEN RENDERER
     ========================================================================= */
  function renderXAITokens(tokens) {
    const container = document.getElementById("xai-container");
    container.innerHTML = "";

    tokens.forEach((t) => {
      if (t.type === "punct") {
        container.appendChild(document.createTextNode(t.token + " "));
        return;
      }

      if (t.type === "neutral") {
        container.appendChild(document.createTextNode(t.token + " "));
        return;
      }

      const span = document.createElement("span");
      span.className = `token-span token-${t.type}`;
      span.textContent = t.token;
      span.setAttribute(
        "data-tooltip",
        `Weight: ${t.weight > 0 ? "+" : ""}${t.weight} | ${t.reason}`
      );
      container.appendChild(span);
      container.appendChild(document.createTextNode(" "));
    });
  }

  /* =========================================================================
     9. READABILITY & STYLOMETRICS TABLE
     ========================================================================= */
  function renderReadability(read, stylo) {
    const list = document.getElementById("readability-list");
    list.innerHTML = `
      <div class="metric-row">
        <span class="metric-title">Flesch Reading Ease (FRE)</span>
        <span class="metric-value">${read.flesch_reading_ease} / 100</span>
      </div>
      <div class="metric-row">
        <span class="metric-title">Flesch-Kincaid Grade Level</span>
        <span class="metric-value">Grade ${read.flesch_kincaid_grade}</span>
      </div>
      <div class="metric-row">
        <span class="metric-title">Coleman-Liau Index</span>
        <span class="metric-value">${read.coleman_liau_index}</span>
      </div>
      <div class="metric-row">
        <span class="metric-title">Gunning Fog Index</span>
        <span class="metric-value">${read.gunning_fog_index}</span>
      </div>
      <div class="metric-row">
        <span class="metric-title">Reading Difficulty Level</span>
        <span class="metric-value text-green">${read.reading_level}</span>
      </div>
      <div class="metric-row">
        <span class="metric-title">Lexical Diversity (Type-Token Ratio)</span>
        <span class="metric-value">${stylo.lexical_diversity_ttr}</span>
      </div>
      <div class="metric-row">
        <span class="metric-title">Hapax Legomena Ratio (Rare words)</span>
        <span class="metric-value">${stylo.hapax_legomena_ratio}</span>
      </div>
      <div class="metric-row">
        <span class="metric-title">Capitalization Density</span>
        <span class="metric-value">${stylo.caps_ratio_percent}%</span>
      </div>
    `;
  }

  /* =========================================================================
     10. EMOTION RADAR CHART & SENTIMENT
     ========================================================================= */
  function renderEmotionChart(sentiment) {
    const ctx = document.getElementById("emotionChart").getContext("2d");
    const emo = sentiment.emotion_radar;

    const data = {
      labels: ["Fear / Threat", "Anger / Outrage", "Trust / Credibility", "Surprise / Shock"],
      datasets: [
        {
          label: "Emotional Intensity",
          data: [emo.fear, emo.anger, emo.trust, emo.surprise],
          backgroundColor: "rgba(6, 182, 212, 0.2)",
          borderColor: "#06b6d4",
          pointBackgroundColor: "#38bdf8",
          pointBorderColor: "#fff",
          borderWidth: 2,
        },
      ],
    };

    if (emotionChart) {
      emotionChart.destroy();
    }

    try {
      emotionChart = new Chart(ctx, {
        type: "radar",
        data: data,
        options: {
          responsive: true,
          maintainAspectRatio: false,
          scales: {
            r: {
              angleLines: { color: "rgba(255, 255, 255, 0.1)" },
              grid: { color: "rgba(255, 255, 255, 0.08)" },
              pointLabels: { color: "#9ca3af", font: { size: 10 } },
              ticks: { display: false, max: 100, min: 0 },
            },
          },
          plugins: {
            legend: { display: false },
          },
        },
      });
    } catch (e) {
      console.warn("Chart.js rendering skipped:", e);
    }

    // Sentiment summary
    const box = document.getElementById("sentiment-summary-box");
    box.innerHTML = `
      <div><strong>Tone Classification:</strong> ${sentiment.overall_tone}</div>
      <div><strong>Sentiment Polarity:</strong> ${sentiment.polarity} (-1.0 negative to +1.0 positive)</div>
      <div><strong>Subjectivity Index:</strong> ${sentiment.subjectivity} (0.0 purely objective, 1.0 purely opinion)</div>
    `;
  }

  /* =========================================================================
     11. SENSATIONALISM BREAKDOWN
     ========================================================================= */
  function renderSensationalism(sens) {
    const container = document.getElementById("sensational-breakdown");

    const clickbaitTags = sens.clickbait_phrases.length
      ? sens.clickbait_phrases.map((p) => `<span class="danger-tag">${p}</span>`).join(" ")
      : `<span class="clean-tag">Zero clickbait phrases detected</span>`;

    const weaselTags = sens.weasel_words.length
      ? sens.weasel_words.map((w) => `<span class="weasel-tag">${w}</span>`).join(" ")
      : `<span class="clean-tag">Clear attribution & sourcing</span>`;

    const loadedWords = sens.sensational_words_found.length
      ? sens.sensational_words_found.map((w) => `<span class="danger-tag">${w}</span>`).join(" ")
      : `<span class="clean-tag">Neutral vocabulary</span>`;

    container.innerHTML = `
      <div>
        <span class="label-text">Sensationalism Score:</span>
        <strong style="color: ${sens.sensationalism_score > 35 ? '#f87171' : '#34d399'}">${sens.sensationalism_score} / 100</strong>
      </div>
      <div>
        <span class="label-text">Detected Clickbait Phrases:</span>
        <div class="tag-cloud">${clickbaitTags}</div>
      </div>
      <div>
        <span class="label-text">Anonymous Attribution / Weasel Words:</span>
        <div class="tag-cloud">${weaselTags}</div>
      </div>
      <div>
        <span class="label-text">Emotionally Charged Superlatives:</span>
        <div class="tag-cloud">${loadedWords}</div>
      </div>
    `;
  }

  /* =========================================================================
     12. EXTRACTED ENTITIES & CLAIMS
     ========================================================================= */
  function renderEntitiesAndClaims(ec) {
    const grid = document.getElementById("claims-grid");

    const entitiesHtml = ec.named_entities.length
      ? ec.named_entities.map((e) => `<li>${e}</li>`).join("")
      : `<li>No complex proper noun sequences found.</li>`;

    const statsHtml = ec.statistical_claims.length
      ? ec.statistical_claims.map((s) => `<li>${s}</li>`).join("")
      : `<li>No prominent numerical claims detected.</li>`;

    const assertionsHtml = ec.key_assertions.length
      ? ec.key_assertions.map((a) => `<li>"${a}"</li>`).join("")
      : `<li>Standard descriptive sentences.</li>`;

    grid.innerHTML = `
      <div class="claim-block">
        <h4>Identified Entities & Organizations</h4>
        <ul class="claims-item-list">${entitiesHtml}</ul>
      </div>
      <div class="claim-block">
        <h4>Statistical & Quantitative Claims</h4>
        <ul class="claims-item-list">${statsHtml}</ul>
      </div>
      <div class="claim-block" style="grid-column: span 2;">
        <h4>Key Factual Assertions & Declarations</h4>
        <ul class="claims-item-list">${assertionsHtml}</ul>
      </div>
    `;
  }

  /* =========================================================================
     13. FACT-CHECK MATCHES
     ========================================================================= */
  function renderFactMatches(facts) {
    const container = document.getElementById("fact-matches-list");
    if (!facts || facts.length === 0) {
      container.innerHTML = `
        <div class="fact-match-item is-verified">
          <div>
            <div class="fact-claim">No Debunked Conspiracy Patterns Detected</div>
            <div class="fact-exp">The article's claims do not match high-frequency debunked misinformation records in the active knowledge base.</div>
          </div>
          <span class="badge badge-accent">Clean Match</span>
        </div>
      `;
      return;
    }

    container.innerHTML = facts
      .map((f) => {
        const isDebunked = f.verdict.includes("FALSE") || f.verdict.includes("DEBUNKED");
        const matchClass = isDebunked ? "is-debunked" : "is-verified";
        const badgeColor = isDebunked ? "badge-red" : "badge-green";

        return `
        <div class="fact-match-item ${matchClass}">
          <div>
            <div class="fact-claim">${f.claim}</div>
            <div class="fact-exp">${f.explanation}</div>
            <div style="margin-top: 0.4rem; font-size: 0.75rem; color: #6b7280;">
              Audited by: ${f.fact_checkers.join(", ")} &bull; Relevance: ${f.relevance_score}%
            </div>
          </div>
          <span class="verdict-badge ${badgeColor}">${f.verdict}</span>
        </div>
      `;
      })
      .join("");
  }

  /* =========================================================================
     14. COMPARATIVE MATRIX EXECUTION
     ========================================================================= */
  function initComparativeDemo() {
    const btnLoad = document.getElementById("btn-load-compare-sample");
    const btnRun = document.getElementById("btn-run-compare");

    if (!btnLoad || !btnRun) return;

    btnLoad.addEventListener("click", () => {
      document.getElementById("cmp-title-a").value = "Reuters: Global Inflation Data Moderates to 2.4%";
      document.getElementById("cmp-text-a").value =
        "Core consumer inflation across major developed economies demonstrated measurable signs of stabilization over the past quarter, according to comprehensive indices released yesterday by international statistical agencies. The harmonized index recorded an annualized expansion rate of 2.4 percent, aligning closely with consensus projections. Central bank spokespersons confirmed monetary policy remains vigilant.";

      document.getElementById("cmp-title-b").value = "Viral Conspiracy Post: The Economic Collapse They Secretly Planned!";
      document.getElementById("cmp-text-b").value =
        "THEY ARE LYING TO YOU! Bombshell classified leaks prove corrupt globalist central bankers are orchestrating the total collapse of all currency tonight! Whistleblower insiders reveal shadow elites will freeze everyone's savings! Wake up people before this gets BANNED forever!";
    });

    btnRun.addEventListener("click", async () => {
      const text_a = document.getElementById("cmp-text-a").value.trim();
      const title_a = document.getElementById("cmp-title-a").value.trim();
      const text_b = document.getElementById("cmp-text-b").value.trim();
      const title_b = document.getElementById("cmp-title-b").value.trim();

      if (!text_a || !text_b) {
        alert("Please ensure both Article A and Article B have content.");
        return;
      }

      btnRun.disabled = true;
      btnRun.textContent = "Comparing...";

      try {
        const res = await fetch("/api/compare", {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({
            text_a,
            title_a,
            domain_a: "reuters.com",
            text_b,
            title_b,
            domain_b: "viral-rumors.net",
          }),
        });
        const data = await res.json();

        if (data.status === "success") {
          renderComparisonResults(data);
        } else {
          alert(data.message || "Comparison failed.");
        }
      } catch (err) {
        alert("Comparison error: " + err.message);
      } finally {
        btnRun.disabled = false;
        btnRun.textContent = "Run Side-by-Side Comparison";
      }
    });
  }

  function renderComparisonResults(data) {
    const container = document.getElementById("compare-results");
    const displayGrid = document.getElementById("comparison-display-grid");
    const delta = data.comparison_delta;
    const a = data.article_a;
    const b = data.article_b;

    document.getElementById("cmp-winner-badge").textContent =
      `${delta.higher_credibility} exhibits superior credibility (Score differential: ${Math.abs(delta.score_diff)} pts)`;

    displayGrid.innerHTML = `
      <div class="compare-card-col">
        <h4 style="color: #38bdf8;">${a.title}</h4>
        <div class="metric-row">
          <span class="metric-title">Verity Index:</span>
          <span class="metric-value text-green">${a.verity.verity_score} / 100</span>
        </div>
        <div class="metric-row">
          <span class="metric-title">Verdict:</span>
          <span class="verdict-badge badge-green">${a.verity.verdict}</span>
        </div>
        <div class="metric-row">
          <span class="metric-title">Sensationalism Score:</span>
          <span class="metric-value">${a.nlp.sensationalism.sensationalism_score} / 100</span>
        </div>
        <div class="metric-row">
          <span class="metric-title">Tone & Polarity:</span>
          <span class="metric-value">${a.nlp.sentiment.overall_tone} (${a.nlp.sentiment.polarity})</span>
        </div>
        <div class="metric-row">
          <span class="metric-title">Subjectivity:</span>
          <span class="metric-value">${a.nlp.sentiment.subjectivity} (Factual)</span>
        </div>
      </div>

      <div class="compare-card-col">
        <h4 style="color: #fbbf24;">${b.title}</h4>
        <div class="metric-row">
          <span class="metric-title">Verity Index:</span>
          <span class="metric-value text-red">${b.verity.verity_score} / 100</span>
        </div>
        <div class="metric-row">
          <span class="metric-title">Verdict:</span>
          <span class="verdict-badge badge-red">${b.verity.verdict}</span>
        </div>
        <div class="metric-row">
          <span class="metric-title">Sensationalism Score:</span>
          <span class="metric-value">${b.nlp.sensationalism.sensationalism_score} / 100</span>
        </div>
        <div class="metric-row">
          <span class="metric-title">Tone & Polarity:</span>
          <span class="metric-value">${b.nlp.sentiment.overall_tone} (${b.nlp.sentiment.polarity})</span>
        </div>
        <div class="metric-row">
          <span class="metric-title">Subjectivity:</span>
          <span class="metric-value">${b.nlp.sentiment.subjectivity} (Extreme)</span>
        </div>
      </div>
    `;

    container.classList.remove("hidden");
    container.scrollIntoView({ behavior: "smooth" });
  }

  /* =========================================================================
     15. MODEL & ACADEMIC NLP METRICS TAB
     ========================================================================= */
  async function loadModelMetrics() {
    try {
      const res = await fetch("/api/model-stats");
      const data = await res.json();
      if (data.status === "success" && data.metrics) {
        const m = data.metrics;
        document.getElementById("metric-accuracy").textContent = `${m.accuracy}%`;
        document.getElementById("metric-precision").textContent = `${m.precision}%`;
        document.getElementById("metric-recall").textContent = `${m.recall}%`;
        document.getElementById("metric-f1").textContent = `${m.f1_score}%`;
        document.getElementById("metric-roc").textContent = `ROC-AUC: ${m.roc_auc}`;

        // Confusion matrix
        const cm = m.confusion_matrix;
        document.getElementById("cm-tn").querySelector(".cell-val").textContent = cm.true_negative;
        document.getElementById("cm-fp").querySelector(".cell-val").textContent = cm.false_positive;
        document.getElementById("cm-fn").querySelector(".cell-val").textContent = cm.false_negative;
        document.getElementById("cm-tp").querySelector(".cell-val").textContent = cm.true_positive;

        // Top Feature Cues
        const fakeList = document.getElementById("top-fake-cues");
        fakeList.innerHTML = m.top_fake_cues
          .map((c) => `<li><span>"${c.feature}"</span><strong>${c.weight}</strong></li>`)
          .join("");

        const credibleList = document.getElementById("top-credible-cues");
        credibleList.innerHTML = m.top_credible_cues
          .map((c) => `<li><span>"${c.feature}"</span><strong>+${c.weight}</strong></li>`)
          .join("");
      }
    } catch (err) {
      console.error("Failed to load model metrics:", err);
    }
  }

  const btnRefreshMetrics = document.getElementById("btn-refresh-metrics");
  if (btnRefreshMetrics) {
    btnRefreshMetrics.addEventListener("click", () => {
      loadModelMetrics();
      alert("Model evaluation metrics refreshed.");
    });
  }

  /* =========================================================================
     16. FACT-CHECK LIBRARY TAB
     ========================================================================= */
  async function loadFactCheckLibrary(query = "") {
    try {
      const url = query ? `/api/fact-checks?q=${encodeURIComponent(query)}` : "/api/fact-checks";
      const res = await fetch(url);
      const data = await res.json();

      if (data.status === "success") {
        renderFactCheckCards(data.fact_checks);
      }
    } catch (err) {
      console.error("Failed to load fact check library:", err);
    }
  }

  function renderFactCheckCards(factChecks) {
    const container = document.getElementById("factcheck-cards-container");
    if (!factChecks || factChecks.length === 0) {
      container.innerHTML = `<p style="color: #9ca3af; grid-column: span 2;">No fact checks match your query.</p>`;
      return;
    }

    container.innerHTML = factChecks
      .map((fc) => {
        const isDebunked = fc.verdict.includes("FALSE") || fc.verdict.includes("DEBUNKED");
        const badgeColor = isDebunked ? "badge-red" : "badge-green";

        return `
        <div class="fact-card-item">
          <div class="fact-card-header">
            <span class="badge badge-accent">${fc.category}</span>
            <span class="verdict-badge ${badgeColor}">${fc.verdict}</span>
          </div>
          <h4 style="font-size: 0.95rem; color: #fff;">${fc.claim}</h4>
          <p style="font-size: 0.85rem; color: #9ca3af; line-height: 1.5;">${fc.explanation}</p>
          <div style="font-size: 0.75rem; color: #6b7280; margin-top: auto;">
            Auditors: ${fc.fact_checkers.join(", ")}
          </div>
        </div>
      `;
      })
      .join("");
  }

  const factSearchInput = document.getElementById("factcheck-search");
  if (factSearchInput) {
    let debounceTimer;
    factSearchInput.addEventListener("input", (e) => {
      clearTimeout(debounceTimer);
      debounceTimer = setTimeout(() => {
        loadFactCheckLibrary(e.target.value.trim());
      }, 300);
    });
  }
});
