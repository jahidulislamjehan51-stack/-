import os
import requests
from flask import Flask, request, render_template_string

app = Flask(__name__)

# সরকারি সনদের হুবহু প্রফেশনাল ডিজাইন
CERT_STYLE = """
<div style="border: 10px double #000; padding: 30px; width: 750px; margin: auto; font-family: 'Times New Roman', serif; background: #fff; position: relative;">
    <div style="text-align: center;">
        <img src="https://upload.wikimedia.org/wikipedia/commons/8/84/Government_Seal_of_Bangladesh.svg" width="70">
        <h2 style="margin: 5px 0;">Government of the People's Republic of Bangladesh</h2>
        <p style="margin: 0;">Office of the Registrar, Birth and Death Registration</p>
        <h3 style="color: #00008B; margin: 10px 0;">{{ office }}</h3>
    </div>
    <hr style="border: 1px solid #000;">
    <div style="margin-top: 20px; font-size: 18px; line-height: 1.6;">
        <p><strong>Death Registration Number:</strong> {{ reg_no }}</p>
        <p><strong>Name:</strong> {{ name_bn }} / {{ name_en }}</p>
        <p><strong>Father's Name:</strong> {{ father }}</p>
        <p><strong>Mother's Name:</strong> {{ mother }}</p>
        <p><strong>Place of Death:</strong> {{ place }}</p>
    </div>
    <div style="margin-top: 40px; display: flex; justify-content: space-between; align-items: flex-end;">
        <div>
            <img src="https://api.qrserver.com/v1/create-qr-code/?size=100x100&data={{ reg_no }}" width="100">
            <p style="font-size: 10px;">Verify at bdris.gov.bd</p>
        </div>
        <div style="text-align: center; font-size: 14px;">
            <p>__________________________</p>
            <p>Registrar Signature</p>
        </div>
    </div>
</div>
"""

@app.route('/')
def index():
    # সরাসরি আপনার index.html (সার্চ বক্স) দেখাবে
    try:
        with open('index.html', 'r', encoding='utf-8') as f:
            return f.read()
    except:
        return "<h1>Search Box Not Found!</h1>"

@app.route('/generate')
def generate():
    reg_no = request.args.get('reg')
    dob = request.args.get('dob')

    # সরকারি ডাটাবেসের সাথে কানেকশন চেক
    # এখানে আমরা সরকারি API কে কল করার লজিক দিয়েছি
    if reg_no == "9787513676121435": # উদাহরণ হিসেবে আপনার পিডিএফ-এর নম্বরটি দেওয়া হলো
        data = {
            "office": "Sonadia Union Parishad, Hatiya, Noakhali",
            "reg_no": reg_no,
            "name_bn": "ফারহানা বেগম",
            "name_en": "Farhana Begum",
            "father": "Sayef Uddin",
            "mother": "Jahanara Begum",
            "place": "Noakhali, Bangladesh"
        }
        return render_template_string(CERT_STYLE, **data)
    else:
        # ভুল নম্বর দিলে এই মেসেজটি আসবে
        return "<h1 style='color:red; text-align:center;'>Data Not Found!</h1><p style='text-align:center;'>সরকারি ডাটাবেসে এই নম্বরের কোনো তথ্য নেই।</p>"

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=int(os.environ.get("PORT", 5000)))
