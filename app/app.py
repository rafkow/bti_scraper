from flask import Flask, render_template, request

app = Flask(__name__)

@app.route("/", methods=['GET','POST'])
def home():
    if request.method == "POST":
        url = request.form['url_source']
        report_type = request.form['report_type']
        return f"<h1>{url}- {report_type}</h1>"
    return render_template('index.html')