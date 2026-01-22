from flask import Flask, request, render_template_string

app = Flask(__name__)

# ফারহানা বেগম এর পিডিএফ এর আদলে তৈরি ডিজাইন
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
    <p>Place of Death: {{ place }}</p>
    <p style="font-size: 10px; margin-top: 30px;">This certificate is generated from bdris.gov.bd</p>
</div>
"""

@app.route('/generate')
def generate():
    reg = request.args.get('reg')
    dob = request.args.get('dob')
    
    # এটি উদাহরণ ডেটা, যা পরে আসল ডাটাবেস থেকে আসবে
    data = {
        "office_name": "Sonadia Union Parishad, Hatiya, Noakhali",
        "reg_no": reg,
        "name_bn": "ফারহানা বেগম",
        "name_en": "Farhana Begum",
        "father": "Sayef Uddin",
        "mother": "Jahanara Begum",
        "place": "Noakhali, Bangladesh"
    }
    return render_template_string(CERT_HTML, **data)

if __name__ == "__main__":
    app.run()
