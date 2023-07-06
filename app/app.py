from flask import Flask, render_template, request
import ec_europa

app = Flask(__name__)

@app.route("/", methods=['GET','POST'])
def home():
    if request.method == "POST":
        url = request.form['url_source']
        report_type = request.form['report_type']
        return f"<h1>{url}- {report_type}</h1>"
    res = ec_europa.get_bti("https://ec.europa.eu/taxation_customs/dds2/ebti/ebti_consultation.jsp?Lang=en&Lang=en&refcountry=&reference=&valstartdate1=04-07-2023&valstartdate=04%2F07%2F2023&valstartdateto1=&valstartdateto=&valenddate1=&valenddate=&valenddateto1=&valenddateto=&suppldate1=&suppldate=&nomenc=&nomencto=&keywordsearch1=&keywordsearch=&specialkeyword=&keywordmatchrule=OR&excludekeywordsearch1=&excludekeywordsearch=&excludespecialkeyword=&descript=&orderby=0&Expand=true&offset=1&viewVal=&isVisitedRef=false&allRecords=0&showProgressBar=true", True)
    for r in res:
        print(r)
    return render_template('index.html')