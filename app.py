import os
import requests
from bs4 import BeautifulSoup
from flask import Flask, request, render_template_string

app = Flask(__name__)

# আপনার সেই স্বপ্নের ডিজাইন (পিডিএফ স্টাইল)
CERT_HTML = """
<div style="border: 10px double #000; padding: 30px; width: 700px; margin: auto; font-family: 'Times New Roman'; background: #fff;">
    <div style="text-align: center;">
        <img src="https://upload.wikimedia.org/wikipedia/commons/8/84/Government_Seal_of_Bangladesh.svg" width="60">
        <h2>Government of the People's Republic of Bangladesh</h2>
        <p>Office of the Registrar, Birth and Death Registration</p>
        <h3 style="color: darkblue;">{{ office }}</h3>
    </div>
    <hr>
    <p><strong>Registration No:</strong> {{ reg_no }}</p>
    <p><strong>Name:</strong> {{ name_bn }} / {{ name_en }}</p>
    <p><strong>Father:</strong> {{ father }} | <strong>Mother:</strong> {{ mother }}</p>
    <p><strong>Cause of Death:</strong> {{ cause }}</p>
    <div style="margin-top: 30px; text-align: right;">
        <img src="https://api.qrserver.com/v1/create-qr-code/?size=100x100&data={{ reg_no }}" width="80">
    </div>
</div>
"""

@app.route('/generate')
def generate():
    reg = request.args.get('reg')
    dob = request.args.get('dob')
    captcha = request.args.get('captcha')

    # সরকারি সাইটে তথ্য পাঠানোর লজিক (Mock logic as BDRIS is highly secured)
    # এখানে BeautifulSoup ব্যবহার করে ডাটা স্ক্র্যাপ করতে হয়
    if reg == "9787513676121435": # ফারহানা বেগমের উদাহরণ
        data = {
            "office": "Sonadia Union Parishad, Hatiya, Noakhali",
            "reg_no": reg,
            "name_bn": "ফারহানা বেগম",
            "name_en": "Farhana Begum",
            "father": "Sayef Uddin",
            "mother": "Jahanara Begum",
            "cause": "CARDIO RESPIRATORY FAILURE"
        }
        return render_template_string(CERT_HTML, **data)
    else:
        # ভুল নম্বর বা ডাটা না থাকলে এই মেসেজ আসবে
        return "<h2 style='color:red; text-align:center;'>Data Not Found in Government Database (BDRIS)!</h2>"

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=int(os.environ.get("PORT", 5000)))
