from flask import Flask, request, render_template, jsonify
import joblib
from utils import extract_features

app = Flask(__name__)
model = joblib.load("phishing_model.pkl")

@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        url = request.form['url']
        features = extract_features(url)

        prediction = model.predict([features])[0]
        probability = model.predict_proba([features])[0][1] * 100

        result = "Phishing 🚨" if prediction == 1 else "Safe ✅"

        analysis = []

        if features[0] > 75:
            analysis.append("🚨 Very long URL detected (high risk)")
        elif features[0] > 50:
            analysis.append("⚠ Moderately long URL (suspicious)")

        if features[1] == 0:
            analysis.append("🚨 No HTTPS (connection not secure)")
        else:
            analysis.append("✅ Uses HTTPS (secure connection)")

        if features[2] > 5:
            analysis.append("⚠ Too many dots (possible subdomain attack)")

        if features[3] > 6:
            analysis.append("⚠ Too many slashes (complex URL structure)")

        if features[4] == 1:
            analysis.append("🚨 IP address used instead of domain")

        if features[5] > 15:
            analysis.append("⚠ Unusually long domain name")

        if len(analysis) <= 1:
            analysis.append("✅ No major phishing indicators detected")

        # 🔥 DYNAMIC AI EXPLANATION
        feature_analysis = [
            {"name": "URL Length", "value": features[0]},
            {"name": "HTTPS", "value": "Yes" if features[1] == 1 else "No"},
            {"name": "Dots Count", "value": features[2]},
            {"name": "Slashes Count", "value": features[3]},
            {"name": "IP Address Used", "value": "Yes" if features[4] == 1 else "No"},
            {"name": "Domain Length", "value": features[5]}
        ]

        return render_template(
            'index.html',
            result=result,
            probability=round(probability, 2),
            analysis=analysis,
            feature_analysis=feature_analysis
        )

    return render_template('index.html', result=None)



@app.route('/chat', methods=['POST'])
def chat():
    user_msg = request.json['message'].lower()

    phishing_info = [
        "Phishing ek cyber attack hai jisme attackers fake websites ya emails bana ke users ka data chura lete hain.",
        "Attackers login pages ya bank pages ka fake version bana dete hain.",
        "Goal hota hai passwords, OTP aur financial info lena."
    ]

    safety_tips = [
        "HTTPS check karo 🔒",
        "Unknown links avoid karo",
        "Domain spelling verify karo",
        "Password kabhi unknown site pe enter mat karo",
        "Urgent messages se bachke raho"
    ]

    risk_signs = [
        "IP address URL me",
        "Long ya random URL",
        "No HTTPS",
        "Too many dots",
        "Suspicious keywords"
    ]

    if "phishing" in user_msg:
        reply = "🚨 " + phishing_info[0] + "\n\n💡 " + phishing_info[1]

    elif "detect" in user_msg:
        reply = "🧠 Phishing detect karne ke liye:\n- " + "\n- ".join(risk_signs)

    elif "safe" in user_msg or "protect" in user_msg:
        reply = "🛡 Safe rehne ke liye:\n- " + "\n- ".join(safety_tips)

    elif "kya karu" in user_msg or "what to do" in user_msg:
        reply = "⚠ Agar phishing site lage:\n1. Info mat daalo\n2. Site band karo\n3. Official site manually open karo\n4. Password change karo"

    elif "risk" in user_msg:
        reply = "🚨 High risk signals:\n- " + "\n- ".join(risk_signs)

    elif "hello" in user_msg or "hi" in user_msg:
        reply = "👋 Hello! Main AI Cyber Assistant hoon. Aap mujhse phishing aur security ke baare me kuch bhi puch sakte ho."

    else:
        reply = (
            "🤖 Main help kar sakta hoon:\n"
            "• Phishing kya hai\n"
            "• Safe kaise rahe\n"
            "• Risk kaise detect kare\n\n"
            "Try asking:\n"
            "👉 how to detect phishing\n"
            "👉 what to do if phishing\n"
            "👉 how to stay safe"
        )

    return jsonify({"reply": reply})


if __name__ == "__main__":
    app.run(debug=True)