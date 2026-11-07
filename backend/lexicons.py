"""
Lexicons and reference databases for Verity News Credibility Analyzer.
Includes clickbait lexicons, weasel words, emotional triggers, domain credibility ratings, and fact-check records.
"""

CLICKBAIT_PHRASES = [
    "you won't believe", "you wont believe", "shocking truth", "what happens next",
    "will blow your mind", "the secret they don't want you to know", "miracle cure",
    "doctors hate this", "big pharma hiding", "banned by government", "secret exposed",
    "the real reason why", "bombshell revelation", "mainstream media won't tell you",
    "mainstream media is lying", "everyone is talking about", "this one simple trick",
    "they are lying to you", "unbelievable truth", "exposed once and for all",
    "the terrifying truth", "don't let them fool you", "proof that", "is finally over",
    "destroy the competition", "mind-blowing secret", "the truth about", "wake up people",
    "must see before it's deleted", "viral sensation", "shocking video", "insane discovery"
]

WEASEL_WORDS = [
    "sources claim", "sources say", "many people say", "critics argue",
    "experts warn", "it is widely believed", "some say", "it has been alleged",
    "rumors indicate", "insiders say", "it is said that", "reports suggest",
    "witnesses claim", "anonymous sources", "officials refused to deny",
    "could potentially cause", "might be linked to", "speculation is mounting",
    "growing evidence suggests", "some believe", "questions have been raised"
]

CREDIBLE_ATTRIBUTION_MARKERS = [
    "according to the official report", "peer-reviewed study published in",
    "spokesperson confirmed", "press release issued by", "reuters confirmed",
    "data published by the national", "in a statement released on",
    "verified by independent researchers", "conducting a double-blind trial",
    "statistics released by the department", "filed in federal court",
    "confirmed by the agency", "public records show", "the audit concluded"
]

SENSATIONAL_WORDS = {
    "catastrophic", "unprecedented", "horrifying", "terrifying", "devastating",
    "miracle", "shocking", "insane", "apocalyptic", "traitor", "scandalous",
    "explosive", "jaw-dropping", "outrageous", "furious", "unforgivable",
    "disastrous", "nightmare", "mind-boggling", "mindblowing", "monstrous",
    "lethal", "deadly", "hoax", "conspiracy", "rigged", "censored",
    "unmasked", "venomous", "carnage", "evil", "tyranny", "brainwashed"
}

EMOTIONAL_LEXICON = {
    "fear": {
        "danger", "threat", "lethal", "fatal", "terrifying", "panic", "collapse",
        "crisis", "radiation", "catastrophe", "poison", "toxic", "destroy", "epidemic",
        "deadly", "warning", "emergency", "assault", "dread", "terror", "risk"
    },
    "anger": {
        "outrage", "furious", "disgrace", "betrayal", "corrupt", "tyrant", "scandal",
        "disgusting", "arrogant", "traitor", "conspiracy", "rigged", "steal", "cheat",
        "shameful", "oppression", "hypocrite", "evil", "liar", "vile"
    },
    "trust": {
        "official", "verified", "peer-reviewed", "confirmed", "evidence", "proven",
        "research", "university", "reputable", "independent", "transparent", "audit",
        "consensus", "factual", "authenticated", "spokesperson", "documented"
    },
    "surprise": {
        "shocking", "unbelievable", "unexpected", "astonishing", "unprecedented",
        "jaw-dropping", "sudden", "stunned", "bombshell", "bizarre", "startling"
    }
}

# Domain Credibility Ratings (Score 0-100, Tier, Category, Notes)
DOMAIN_DATABASE = {
    "reuters.com": {
        "score": 96, "tier": "Tier 1 - Highly Credible", "category": "News Agency",
        "bias": "Center / Neutral", "fact_check_record": "Excellent track record with strict sourcing."
    },
    "apnews.com": {
        "score": 95, "tier": "Tier 1 - Highly Credible", "category": "News Agency",
        "bias": "Center / Neutral", "fact_check_record": "Gold standard news wire service."
    },
    "bbc.com": {
        "score": 92, "tier": "Tier 1 - Highly Credible", "category": "Public Broadcaster",
        "bias": "Center / Neutral", "fact_check_record": "High factual standards and verified reporting."
    },
    "bbc.co.uk": {
        "score": 92, "tier": "Tier 1 - Highly Credible", "category": "Public Broadcaster",
        "bias": "Center / Neutral", "fact_check_record": "High factual standards and verified reporting."
    },
    "nature.com": {
        "score": 98, "tier": "Tier 1 - Highly Credible", "category": "Scientific Journal",
        "bias": "Scientific / Neutral", "fact_check_record": "Rigorous peer-reviewed publications."
    },
    "science.org": {
        "score": 98, "tier": "Tier 1 - Highly Credible", "category": "Scientific Journal",
        "bias": "Scientific / Neutral", "fact_check_record": "American Association for Advancement of Science."
    },
    "who.int": {
        "score": 94, "tier": "Tier 1 - Highly Credible", "category": "Health Authority",
        "bias": "Health / Global", "fact_check_record": "World Health Organization official data."
    },
    "cdc.gov": {
        "score": 94, "tier": "Tier 1 - Highly Credible", "category": "Government Agency",
        "bias": "Public Health", "fact_check_record": "Centers for Disease Control."
    },
    "nytimes.com": {
        "score": 88, "tier": "Tier 1 - High Credibility", "category": "Mainstream Newspaper",
        "bias": "Center-Left", "fact_check_record": "Extensive editorial reviews; occasional opinion controversies."
    },
    "wsj.com": {
        "score": 88, "tier": "Tier 1 - High Credibility", "category": "Business Newspaper",
        "bias": "Center-Right", "fact_check_record": "High factual reporting in news desk; conservative op-eds."
    },
    "theguardian.com": {
        "score": 85, "tier": "Tier 2 - Credible", "category": "Mainstream Newspaper",
        "bias": "Left-Leaning", "fact_check_record": "High factual reporting with progressive editorial stance."
    },
    "washingtonpost.com": {
        "score": 86, "tier": "Tier 2 - Credible", "category": "Mainstream Newspaper",
        "bias": "Center-Left", "fact_check_record": "Robust reporting; strict correction policy."
    },
    "bloomberg.com": {
        "score": 90, "tier": "Tier 1 - High Credibility", "category": "Financial News",
        "bias": "Center", "fact_check_record": "Authoritative financial and economic analysis."
    },
    "dailymail.co.uk": {
        "score": 52, "tier": "Tier 3 - Sensationalist / Mixed", "category": "Tabloid",
        "bias": "Right / Sensationalist", "fact_check_record": "Frequent sensationalism, clickbait, and unverified celebrity claims."
    },
    "nypost.com": {
        "score": 64, "tier": "Tier 3 - Mixed Credibility", "category": "Tabloid / Newspaper",
        "bias": "Right-Leaning", "fact_check_record": "Sensationalist headlines with occasional speculative reporting."
    },
    "thesun.co.uk": {
        "score": 45, "tier": "Tier 4 - Low Credibility", "category": "Tabloid",
        "bias": "Sensationalist", "fact_check_record": "Known for exaggerations, speculative rumors, and clickbait."
    },
    "infowars.com": {
        "score": 10, "tier": "Tier 5 - High Misinformation Risk", "category": "Conspiracy Outlet",
        "bias": "Extreme Far-Right / Conspiracy", "fact_check_record": "Repeatedly debunked for fabricated conspiracy theories."
    },
    "naturalnews.com": {
        "score": 12, "tier": "Tier 5 - High Misinformation Risk", "category": "Pseudoscience",
        "bias": "Conspiracy / Anti-Science", "fact_check_record": "Promotes debunked medical treatments and anti-vaccine myths."
    },
    "theonion.com": {
        "score": 25, "tier": "Satire / Parody", "category": "Satire",
        "bias": "Humor / Parody", "fact_check_record": "Fictional satirical stories written intentionally for comedy."
    },
    "babylonbee.com": {
        "score": 28, "tier": "Satire / Parody", "category": "Satire",
        "bias": "Humor / Conservative Satire", "fact_check_record": "Fictional satirical parody."
    },
    "beforeitsnews.com": {
        "score": 15, "tier": "Tier 5 - High Misinformation Risk", "category": "Unmoderated Blog",
        "bias": "Conspiracy", "fact_check_record": "Unchecked user-submitted claims and fringe conspiracies."
    },
    "worldnewsdailyreport.com": {
        "score": 5, "tier": "Tier 5 - Fabricated News", "category": "Fake News / Hoax",
        "bias": "Hoax", "fact_check_record": "Known fake news generator publishing fabricated sensational hoaxes."
    }
}

# Fact-Check Knowledge Base (debunked and verified claims for semantic claim matching)
VERIFIED_FACT_CHECKS = [
    {
        "id": "FC-001",
        "claim": "5G mobile networks cause COVID-19 or biological viral mutations.",
        "verdict": "FALSE / DEBUNKED",
        "category": "Technology & Health",
        "keywords": ["5g", "covid", "coronavirus", "radiation", "mutation", "towers"],
        "explanation": "Radiofrequency radiation used in telecommunications is non-ionizing and physically incapable of creating or transmitting biological viruses like SARS-CoV-2.",
        "fact_checkers": ["WHO", "Reuters Fact Check", "Snopes", "PolitiFact"]
    },
    {
        "id": "FC-002",
        "claim": "Microchips or tracking nanoparticles are implanted in mRNA vaccines.",
        "verdict": "FALSE / DEBUNKED",
        "category": "Health & Medicine",
        "keywords": ["microchip", "vaccine", "tracking", "nanoparticle", "gates", "injection"],
        "explanation": "Vaccine formulations are publicly audited and contain lipids, salts, sugars, and mRNA molecules. No electronic tracking components exist in any licensed vaccine.",
        "fact_checkers": ["BBC Reality Check", "FDA", "AP Fact Check"]
    },
    {
        "id": "FC-003",
        "claim": "Drinking lemon and baking soda cures cancer instantly without chemotherapy.",
        "verdict": "FALSE / PSEUDOSCIENCE",
        "category": "Health & Medicine",
        "keywords": ["cure cancer", "baking soda", "lemon", "miracle cure", "alkaline"],
        "explanation": "There is no clinical evidence that alkaline diets or citrus mixtures alter systemic blood pH or cure oncological malignancies.",
        "fact_checkers": ["American Cancer Society", "Cancer Research UK", "Snopes"]
    },
    {
        "id": "FC-004",
        "claim": "NASA discovered a parallel universe where time flows backwards.",
        "verdict": "MISLEADING / DISTORTED",
        "category": "Science & Space",
        "keywords": ["nasa", "parallel universe", "time flows backwards", "anita", "antarctica"],
        "explanation": "The ANITA experiment detected unusual subatomic particle signals in Antarctic ice, but NASA scientists clarified this does not confirm parallel universes or reversed time.",
        "fact_checkers": ["NASA Science", "National Geographic", "Snopes"]
    },
    {
        "id": "FC-005",
        "claim": "Earth is flat and Antarctic ice wall is guarded by military forces.",
        "verdict": "FALSE / CONSPIRACY",
        "category": "Science & Geography",
        "keywords": ["flat earth", "ice wall", "antarctic treaty", "nasa guards", "dome"],
        "explanation": "Centuries of navigational, geodesic, satellite imagery, and celestial physics prove the Earth is an oblate spheroid.",
        "fact_checkers": ["Scientific American", "NASA", "Space.com"]
    },
    {
        "id": "FC-006",
        "claim": "James Webb Space Telescope detected chemical biosignatures on exoplanet K2-18b.",
        "verdict": "PARTIALLY VERIFIED / UNDER INVESTIGATION",
        "category": "Science & Space",
        "keywords": ["james webb", "jwst", "k2-18b", "biosignature", "dimethyl sulfide"],
        "explanation": "JWST detected carbon-bearing molecules like methane and carbon dioxide, and tentative signs of DMS that require further spectroscopic observations to confirm.",
        "fact_checkers": ["NASA Goddard", "Cambridge Institute of Astronomy"]
    },
    {
        "id": "FC-007",
        "claim": "Consuming excessive bleached white refined sugar increases cardiovascular and metabolic risks.",
        "verdict": "VERIFIED / SCIENTIFIC CONSENSUS",
        "category": "Health & Nutrition",
        "keywords": ["sugar", "cardiovascular", "diabetes", "metabolic", "heart disease"],
        "explanation": "Longitudinal peer-reviewed studies published in JAMA and Lancet confirm that chronic excessive added sugar intake correlates with metabolic syndrome and coronary heart disease.",
        "fact_checkers": ["American Heart Association", "Harvard Medical School", "Lancet"]
    },
    {
        "id": "FC-008",
        "claim": "Pope Francis shocks world by endorsing Donald Trump for President.",
        "verdict": "FALSE / FABRICATED HOAX",
        "category": "Politics & Society",
        "keywords": ["pope francis", "endorses", "trump", "vatican", "shocks world", "endorsement"],
        "explanation": "Originating from satirical website WTOE 5 News during the 2016 election, the Vatican explicitly confirmed that the Pope does not endorse political candidates.",
        "fact_checkers": ["Vatican Press Office", "Snopes", "PolitiFact", "BBC Reality Check"]
    },
    {
        "id": "FC-009",
        "claim": "Celebrity or public figure died unexpectedly in tragic accident.",
        "verdict": "FALSE / CELEBRITY DEATH HOAX",
        "category": "Celebrity & Society",
        "keywords": ["died", "tragic accident", "found dead", "rest in peace", "shocking death"],
        "explanation": "Viral death hoaxes frequently spread on social media to generate ad revenue or malicious link clicks without verification from family or legitimate news agencies.",
        "fact_checkers": ["Snopes", "Reuters", "Associated Press"]
    }
]
