from flask import Flask, request, render_template, render_template_string
import os

app = Flask(__name__, template_folder='.')

# আপনার পিডিএফ ডিজাইনের টেমপ্লেট
CERT_HTML = """
<div style="border: 5px double #000; padding: 20px; width: 650px; margin: auto; font-family: Arial;">
    <div style="text-align: center;">
        <h2>Government of the People's Republic of Bangladesh</h2>
        <h3>Office of the Registrar, Birth and Death Registration</h3>
        <h4 style="color: blue;">{{ office_name }}</h4>
    </div>
    <hr>
    <p>Death Registration Number: <strong>{{ reg_no }}</strong></p>
    <p>Name: {{ name_bn }} / {{ name_en }}</p>
    <p>Father: {{ father }} | Mother: {{ mother }}</p>
    <p style="font-size: 10px; margin-top: 30px;">This certificate is generated from bdris.gov.bd</p>
</div>
"""

@app.route('/')
def home():
    # এটি আপনার index.html ফাইলটি দেখাবে (সার্চ বক্স)
    return render_template('index.html')

@app.route('/generate')
def generate():
    reg = request.args.get('reg')
    # এখানে আপনার দেওয়া পিডিএফ অনুযায়ী ডাইনামিক ডেটা সেট করা হয়েছে
    data = {
        "office_name": "Sonadia Union Parishad, Hatiya, Noakhali",
        "reg_no": reg,
        "name_bn": "ফারহানা বেগম",
        "name_en": "Farhana Begum",
        "father": "Sayef Uddin",
        "mother": "Jahanara Begum"
    }
    return render_template_string(CERT_HTML, **data)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
