import os
from flask import Flask, jsonify, request
from flask_cors import CORS

app = Flask(__name__)
CORS(app, resources={r"/api/*": {"origins": "*"}})

SUPPORTED_LANGUAGES = ["en", "hi", "te", "ta", "bn", "mr"]

CROP_BASE_YIELD = {
    "wheat": 3.9,
    "maize": 4.8,
    "paddy": 4.3,
    "cotton": 3.2,
    "sugarcane": 6.2,
    "chickpea": 2.2,
    "groundnut": 2.6,
    "millet": 2.1,
    "soybean": 3.0,
    "barley": 3.1,
    "tomato": 3.8,
    "potato": 4.4,
    "mustard": 2.0,
    "sesame": 1.7,
    "sunflower": 2.5,
}

SOIL_MULTIPLIERS = {
    "loam": 1.08,
    "clay": 1.00,
    "sandy": 0.92,
    "silt": 1.05,
}

SEASON_MULTIPLIERS = {
    "monsoon": 1.09,
    "spring": 1.02,
    "summer": 0.96,
    "winter": 1.01,
}

CROP_NAMES = {
    "en": {
        "wheat": "Wheat",
        "maize": "Maize",
        "paddy": "Paddy",
        "cotton": "Cotton",
        "sugarcane": "Sugarcane",
        "chickpea": "Chickpea",
        "groundnut": "Groundnut",
        "millet": "Millet",
        "soybean": "Soybean",
        "barley": "Barley",
        "tomato": "Tomato",
        "potato": "Potato",
        "mustard": "Mustard",
        "sesame": "Sesame",
        "sunflower": "Sunflower",
    },
    "hi": {
        "wheat": "गेहूं",
        "maize": "मक्का",
        "paddy": "धान",
        "cotton": "कपास",
        "sugarcane": "गन्ना",
        "chickpea": "चना",
        "groundnut": "मूंगफली",
        "millet": "बाजरा",
        "soybean": "सोयाबीन",
        "barley": "जौ",
        "tomato": "टमाटर",
        "potato": "आलू",
        "mustard": "सरसों",
        "sesame": "तिल",
        "sunflower": "सूरजमुखी",
    },
    "te": {
        "wheat": "గోధుమ",
        "maize": "మొక్కజొన్న",
        "paddy": "అన్నం",
        "cotton": "పత్తి",
        "sugarcane": "చక్కెరగడ్డి",
        "chickpea": "శనగ",
        "groundnut": "వేరుశెనగ",
        "millet": "బాజ్రా",
        "soybean": "సోయాబీన్",
        "barley": "బార్లీ",
        "tomato": "టమాటా",
        "potato": "ఆలూ",
        "mustard": "ఆవాలు",
        "sesame": "నువ్వులు",
        "sunflower": "సూర్యకాంతి",
    },
    "ta": {
        "wheat": "கோதுமை",
        "maize": "சோளம்",
        "paddy": "நெல்",
        "cotton": "பருத்தி",
        "sugarcane": "கரும்பு",
        "chickpea": "கொள்ளு",
        "groundnut": "வேர்க்கடலை",
        "millet": "கம்பு",
        "soybean": "சோயாபீன்",
        "barley": "பார்லி",
        "tomato": "தக்காளி",
        "potato": "உருளைக்கிழங்கு",
        "mustard": "அவல்",
        "sesame": "எள்",
        "sunflower": "சூரியகாந்தி",
    },
    "bn": {
        "wheat": "গম",
        "maize": "ভুট্টা",
        "paddy": "ধান",
        "cotton": "কাপাস",
        "sugarcane": "আখ",
        "chickpea": "ছোলা",
        "groundnut": "মুট",
        "millet": "বাজরা",
        "soybean": "সয়াবিন",
        "barley": "জাউ",
        "tomato": "টমেটো",
        "potato": "আলু",
        "mustard": "সরিষা",
        "sesame": "তিল",
        "sunflower": "সূর্যমুখী",
    },
    "mr": {
        "wheat": "गहू",
        "maize": "मका",
        "paddy": "धान",
        "cotton": "कापूस",
        "sugarcane": "ऊस",
        "chickpea": "हरभरा",
        "groundnut": "शेंगदाणा",
        "millet": "बाजरी",
        "soybean": "सोयाबीन",
        "barley": "ज्वारी",
        "tomato": "टोमॅटो",
        "potato": "बटाटा",
        "mustard": "मोहरी",
        "sesame": "तिल",
        "sunflower": "सूर्यफुल",
    },
}

def normalize_language(lang):
    return (lang or "en").lower().strip() if (lang or "en").lower().strip() in SUPPORTED_LANGUAGES else "en"

def normalize_crop(crop):
    crop_key = (crop or "maize").strip().lower()
    return crop_key if crop_key in CROP_BASE_YIELD else "maize"

def build_recommendations(language, crop, rainfall, temperature, humidity, soil_type):
    recs = []
    lang = normalize_language(language)

    if rainfall < 500:
        recs.append(
            {
                "en": "Increase irrigation and use mulch to reduce water loss.",
                "hi": "सिंचाई बढ़ाएं और पानी की हानि कम करने के लिए मल्च का उपयोग करें।",
                "te": "నీటి సరఫరాను పెంచండి మరియు నీటి నష్టాన్ని తగ్గించడానికి మల్చ్ ఉపయోగించండి।",
                "ta": "நீர்ப்பாசனத்தை அதிகரித்து, நீர் இழப்பைக் குறைக்க மல்ச்சைப் பயன்படுத்தவும்.",
                "bn": "সেচ বাড়ান এবং জল ক্ষতি কমাতে মালচ ব্যবহার করুন।",
                "mr": "सिंचन वाढवा आणि पाण्याचे नुकसान कमी करण्यासाठी मल्च वापरा.",
            }[lang]
        )
    elif rainfall > 1000:
        recs.append(
            {
                "en": "Improve drainage and avoid overwatering.",
                "hi": "जल निकासी सुधारें और अधिक पानी न दें।",
                "te": "నీటి నిష్క్రమణను మెరుగుపరచండి మరియు ఎక్కువ నీరు వాడకండి.",
                "ta": "வடிகாலைக் கூட்டி, அதிக தண்ணீர் விடாதீர்கள்.",
                "bn": "নিষ্কাশন উন্নত করুন এবং অতিরিক্ত সেচ দেবেন না।",
                "mr": "निचरा सुधारवा आणि जास्त पाणी देऊ नका.",
            }[lang]
        )
    else:
        recs.append(
            {
                "en": "Maintain balanced moisture and monitor the crop regularly.",
                "hi": "संतुलित नमी बनाए रखें और फसल की नियमित रूप से निगरानी करें।",
                "te": "సంతులిత తేమను కాపాడండి మరియు పంటను క్రమంగా పర్యవేక్షించండి।",
                "ta": "சமநிலையான ஈரப்பதத்தை பராமரித்து, பயிரை தவறாமல் கண்காணியுங்கள்.",
                "bn": "সুষম আর্দ্রতা বজায় রাখুন এবং ফসল নিয়মিত পর্যবেক্ষণ করুন।",
                "mr": "संतुलित ओल राखा आणि पीक नियमितपणे तपासा.",
            }[lang]
        )

    if temperature > 32:
        recs.append(
            {
                "en": "Provide shade or adjust irrigation during heat stress.",
                "hi": "गर्मी की स्थिति में छाया प्रदान करें या सिंचाई समायोजित करें।",
                "te": "ఉష్ణ ఒత్తిడిలో నీరు పెట్టే సమయాన్ని మార్చండి లేదా నీటి వాడకానికి సమన्वయించండి.",
                "ta": "வெப்ப அழுத்தத்தின் போது நிழல் வழங்குங்கள் அல்லது நீர்ப்பாசனத்தை சரிசெய்யவும்.",
                "bn": "তাপ চাপের সময় ছায়া প্রদান করুন বা সেচ সামঞ্জস্য করুন।",
                "mr": "उष्णतेच्या काळात सावली द्या किंवा सिंचन समायोजित करा.",
            }[lang]
        )

    if soil_type.lower() in {"sandy", "clay"}:
        recs.append(
            {
                "en": "Add organic matter to improve soil structure.",
                "hi": "मिट्टी की संरचना सुधारने के लिए जैविक पदार्थ जोड़ें।",
                "te": "మట్టి నిర్మాణాన్ని మెరుగుపరచడానికి జైవ పదార్థాలను జోడించండి.",
                "ta": "மண் அமைப்பை மேம்படுத்த கரிமப் பொருட்களை சேர்க்கவும்.",
                "bn": "মাটির গঠন উন্নত করতে জৈব পদার্থ যোগ করুন।",
                "mr": "मातीची रचना सुधारण्यासाठी सेंद्रिय पदार्थ जोडा.",
            }[lang]
        )

    return recs[:3]

@app.route("/health", methods=["GET"])
@app.route("/api/health", methods=["GET"])
def health():
    return jsonify({"success": True, "status": "ok"})

@app.route("/api/predict", methods=["POST"])
def predict():
    data = request.get_json(silent=True) or {}

    crop_key = normalize_crop(data.get("crop_type") or data.get("crop"))
    season = str(data.get("season") or "monsoon").strip().lower()
    soil_type = str(data.get("soil_type") or "loam").strip().lower()
    language = normalize_language(data.get("language"))

    rainfall = float(data.get("rainfall", 650) or 650)
    temperature = float(data.get("temperature", 27) or 27)
    humidity = float(data.get("humidity", 70) or 70)
    nitrogen = float(data.get("nitrogen", 110) or 110)
    phosphorus = float(data.get("phosphorus", 45) or 45)
    potassium = float(data.get("potassium", 40) or 40)

    base_yield = CROP_BASE_YIELD.get(crop_key, 3.8)
    season_mult = SEASON_MULTIPLIERS.get(season, 1.0)
    soil_mult = SOIL_MULTIPLIERS.get(soil_type, 1.0)

    yield_value = base_yield * season_mult * soil_mult
    yield_value += rainfall / 400.0
    yield_value += humidity / 100.0 * 0.12
    yield_value += nitrogen / 1000.0 * 0.35
    yield_value += phosphorus / 1000.0 * 0.22
    yield_value += potassium / 1000.0 * 0.18
    yield_value -= max(0, temperature - 32) * 0.03
    if rainfall < 500:
        yield_value -= 0.25
    if rainfall > 1100:
        yield_value -= 0.12

    yield_value = round(max(0.8, yield_value), 2)

    confidence = round(
        min(96.0, 78 + (rainfall / 1200) * 10 + (humidity / 100) * 5 + (soil_mult - 1) * 8),
        1,
    )

    recommendations = build_recommendations(language, crop_key, rainfall, temperature, humidity, soil_type)

    return jsonify({
        "success": True,
        "yield_ton_per_ha": yield_value,
        "confidence_score": confidence,
        "model_type": "Rule-based agronomy model",
        "model_breakdown": {
            "Crop base": round(CROP_BASE_YIELD.get(crop_key, 3.8), 2),
            "Season effect": round(season_mult, 2),
            "Soil effect": round(soil_mult, 2),
            "Weather effect": round((rainfall / 400.0 + humidity / 100.0 * 0.12), 2),
        },
        "recommendations": recommendations,
        "crop_display_name": CROP_NAMES.get(language, CROP_NAMES["en"]).get(crop_key, crop_key),
        "crop_name": crop_key,
    })

@app.route("/api/chat", methods=["POST"])
def chat():
    data = request.get_json(silent=True) or {}
    message = (data.get("message") or "").strip()
    language = normalize_language(data.get("language"))

    if not message:
        return jsonify({"success": False, "error": "Message is required"})

    message_lower = message.lower()

    if any(word in message_lower for word in ["fertilizer", "nutrient", "nitrogen", "phosphorus", "potassium"]):
        reply = {
            "en": "Use split fertilizer applications and test soil before the next dose.",
            "hi": "खत को अलग-अलग खुराक में लगाएं और अगली बार लगाने से पहले मिट्टी का परीक्षण करें।",
            "te": "ఎరువును భాగాలుగా వాడండి మరియు తదుపరి వాడకానికి ముందు మట్టిని పరీక్ష చేయండి.",
            "ta": "உரத்தை பிரிக்கப்பட்ட அளவில் பயன்படுத்துங்கள் மற்றும் அடுத்த பயன்பாட்டுக்கு முன் மண்ணைச் சோதிக்கவும்.",
            "bn": "সারকে ভাগে ভাগে ব্যবহার করুন এবং পরের প্রয়োগের আগে মাটি পরীক্ষা করুন।",
            "mr": "खत भागातून देणं चांगलं आहे आणि पुढील वापरापूर्वी मातीची चाचणी घ्या.",
        }[language]
    elif any(word in message_lower for word in ["water", "irrigation", "rain"]):
        reply = {
            "en": "Water early in the morning and check soil moisture before watering again.",
            "hi": "सुबह जल्दी पानी दें और फिर से पानी देने से पहले मिट्टी की नमी की जांच करें।",
            "te": "ప్రారంభంలో తెల్లవారుజామంలో నీరు వదలండి మరియు మళ్లీ నీరు పెట్టే ముందు మట్టిలో తేమను తనిఖీ చేయండి.",
            "ta": "காலை நேரத்தில் தண்ணீர் விடுங்கள் மற்றும் மீண்டும் தண்ணீர் விடுவதற்கு முன் மண் ஈரப்பதத்தை சரிபார்க்கவும்.",
            "bn": "সকালে জল দিন এবং আবার জল দেওয়ার আগে মাটির আর্দ্রতা পরীক্ষা করুন।",
            "mr": "सकाळी पाणी द्या आणि पुन्हा पाणी देण्यापूर्वी मातीची ओल तपासा.",
        }[language]
    elif any(word in message_lower for word in ["soil", "pest", "disease", "weed"]):
        reply = {
            "en": "Inspect the field weekly and remove weeds early to limit pest pressure.",
            "hi": "हफ्ते में एक बार खेत की जांच करें और कीटों के दबाव को कम करने के लिए खरपतवारों को जल्दी हटाएं।",
            "te": "వారానికి ఒకసారి పొలాన్ని పరిశీలించి, కీటకాల ఒత్తిడిని తగ్గించడానికి గడ్డిని ముందుగానే తొలగించండి.",
            "ta": "வாரந்தோறும் வயலை ஆய்வு செய்து, பூச்சி அழுத்தத்தைக் குறைக்க களைகளை சீக்கிரம் அகற்றவும்.",
            "bn": "সাপ্তাহিকভাবে খেত পরিদর্শন করুন এবং কীট চাপ কমাতে আগেই আগাছা অপসারণ করুন।",
            "mr": "आठवड्याला एकदा शेत तपासा आणि कीटक दाब कमी करण्यासाठी उगवणाऱ्या घास frühen काढा.",
        }[language]
    else:
        reply = {
            "en": "I can help with irrigation, fertilizer timing, soil care, and crop planning.",
            "hi": "मैं सिंचाई, उर्वरक समय, मिट्टी की देखभाल और फसल योजना में मदद कर सकता/सकती हूँ।",
            "te": "నేను నీటి నిర్వహణ, ఎరువుల సమయం, మట్టి పరిరక్షణ మరియు పంట అభివృద్ధిలో సహాయం చేయగలను.",
            "ta": "நீர்ப்பாசனம், உர நேரம், மண் பராமரிப்பு மற்றும் பயிர் திட்டமிடலில் நான் உதவ முடியும்.",
            "bn": "আমি সেচ, সার সময়, মাটি রক্ষণাবেক্ষণ এবং ফসল পরিকল্পনায় সহায়তা করতে পারি।",
            "mr": "मी सिंचन, खतांचा वेळ, मातीची काळजी आणि पीक नियोजनात मदत करू शकतो.",
        }[language]

    return jsonify({"success": True, "reply": reply})

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=True)