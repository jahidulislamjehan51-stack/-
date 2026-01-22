import os
import requests
from flask import Flask, request, render_template_string, Response

app = Flask(__name__)

# সরকারি সাইট থেকে ক্যাপচা ছবি প্রক্সি করা (প্রশ্নবোধক চিহ্ন ঠিক করতে)
@app.route('/get_captcha')
def get_captcha():
    captcha_url = "https://bdris.gov.bd/br/captcha"
    try:
        response = requests.get(captcha_url, stream=True, timeout=5)
        return Response(response.content, mimetype='image/png')
    except:
        return ""

# আপনার পিডিএফ ডিজাইনের এইচটিএমএল (পুরোটা এখানে দেওয়া হলো)
CERT_HTML = """
<div style="border: 10px double #000; padding: 40px; width: 750px; margin: auto; font-family: 'Times New Roman'; background: #fff; position: relative;">
    <div style="text-align: center;">
        <img src="https://upload.wikimedia.org/wikipedia/commons/8/84/Government_Seal_of_Bangladesh.svg" width="70">
        <h2 style="margin:5px;">Government of the People's Republic of Bangladesh</h2>
        <p>Office of the Registrar, Birth and Death Registration</p>
        <h3 style="color: darkblue;">{{ office }}</h3>
    </div>
    <hr style="border: 1px solid #000;">
    <div style="margin-top:20px; font-size: 18px; line-height: 1.6;">
        <p><strong>Death Registration Number:</strong> {{ reg_no }}</p>
        <p><strong>Name:</strong> {{ name_bn }} / {{ name_en }}</p>
        <p><strong>Father:</strong> {{ father }} | <strong>Mother:</strong> {{ mother }}</p>
        <p><strong>Date of Death:</strong> {{ dod }}</p>
        <p><strong>Cause of Death:</strong> {{ cause }}</p>
    </div>
    <div style="margin-top:40px; display: flex; justify-content: space-between; align-items: flex-end;">
        <div><img src="https://api.qrserver.com/v1/create-qr-code/?size=100x100&data={{ reg_no }}" width="90"></div>
        <div style="text-align: center;">_________________<br>Registrar Signature</div>
    </div>
</div>
"""

@app.route('/')
def home():
    # সরাসরি আপনার ইনডেক্স পেজ
    try:
        with open('index.html', 'r', encoding='utf-8') as f:
            return f.read()
    except:
        return "<h1>সার্চ বক্স পাওয়া যায়নি (index.html missing)</h1>"

@app.route('/generate')
def generate():
    reg = request.args.get('reg')
    dob = request.args.get('dob')
    captcha = request.args.get('captcha')

    # আপনার পিডিএফ-এর তথ্যগুলো এখানে থাকবে (ফারহানা বেগমের জন্য)
    if reg == "9787513676121435":
        data = {
            "office": "Sonadia Union Parishad, Hatiya, Noakhali",
            "reg_no": reg,
            "name_bn": "ফারহানা বেগম",
            "name_en": "Farhana Begum",
            "father": "Sayef Uddin",
            "mother": "Jahanara Begum",
            "dod": "2023-10-12",
            "cause": "CARDIO RESPIRATORY FAILURE"
        }
        return render_template_string(CERT_HTML, **data)
    else:
        return "<h2 style='color:red; text-align:center;'>Data Not Found!</h2>"

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=int(os.environ.get("PORT", 5000)))
