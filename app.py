import os
import requests
from flask import Flask, request, render_template_string, Response

app = Flask(__name__)

# সরকারি সাইট থেকে ক্যাপচা ছবি আপনার সাইটে টেনে আনার জন্য
@app.route('/get_captcha')
def get_captcha():
    captcha_url = "https://bdris.gov.bd/br/captcha"
    try:
        # ব্রাউজার যেন মনে করে এটি সরকারি সাইট থেকেই আসছে
        headers = {'User-Agent': 'Mozilla/5.0'}
        response = requests.get(captcha_url, headers=headers, stream=True, timeout=10)
        return Response(response.content, mimetype='image/png')
    except Exception as e:
        return f"Error: {str(e)}"

# পিডিএফ ডিজাইনের এইচটিএমএল (আপনার পাঠানো ডিজাইনের হুবহু)
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
        <p><strong>Cause of Death:</strong> CARDIO RESPIRATORY FAILURE</p>
    </div>
    <div style="margin-top:40px; display: flex; justify-content: space-between; align-items: flex-end;">
        <div><img src="https://api.qrserver.com/v1/create-qr-code/?size=100x100&data={{ reg_no }}" width="90"></div>
        <div style="text-align: center; font-size: 14px;">_________________<br>Registrar Signature</div>
    </div>
</div>
"""

@app.route('/')
def home():
    try:
        with open('index.html', 'r', encoding='utf-8') as f:
            return f.read()
    except:
        return "index.html ফাইলটি খুঁজে পাওয়া যায়নি!"

@app.route('/generate')
def generate():
    reg = request.args.get('reg')
    # সঠিক নম্বর (৯৭৮৭৫১৩৬৭৬১২১৪৩৫) দিলে আপনার ডাটা আসবে
    if reg == "9787513676121435":
        data = {
            "office": "Sonadia Union Parishad, Hatiya, Noakhali",
            "reg_no": reg,
            "name_bn": "ফারহানা বেগম",
            "name_en": "Farhana Begum",
            "father": "Sayef Uddin",
            "mother": "Jahanara Begum",
            "dod": "2023-10-12"
        }
        return render_template_string(CERT_HTML, **data)
    else:
        # ভুল নম্বর দিলে সরকারি ডাটাবেস এরর আসবে
        return "<h2 style='color:red; text-align:center;'>Data Not Found!</h2><p style='text-align:center;'>সরকারি ডাটাবেসে এই নম্বরের কোনো তথ্য পাওয়া যায়নি।</p>"

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=int(os.environ.get("PORT", 5000)))
