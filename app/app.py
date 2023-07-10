from flask import Flask, render_template, request, Response, make_response
import csv
from .ec_europa import generate_bti

app = Flask(__name__)


def iter_csv(data):
    writer = csv.writer(data)
    for csv_line in data:
        writer.writerow(csv_line)
        yield data.read()


@app.route("/", methods=['GET','POST'])
def home():
    if request.method == "POST":

        url = request.form['url_source']
        download_full_report = True if request.form['report_type'] == 'full' else False
        # url = "https://ec.europa.eu/taxation_customs/dds2/ebti/ebti_consultation.jsp?Lang=en&Lang=en&refcountry=&reference=&valstartdate1=10-07-2023&valstartdate=10%2F07%2F2023&valstartdateto1=&valstartdateto=&valenddate1=&valenddate=&valenddateto1=&valenddateto=&suppldate1=&suppldate=&nomenc=&nomencto=&keywordsearch1=&keywordsearch=&specialkeyword=&keywordmatchrule=OR&excludekeywordsearch1=&excludekeywordsearch=&excludespecialkeyword=&descript=&orderby=0&Expand=true&offset=1&viewVal=&isVisitedRef=true&allRecords=0&showProgressBar=true"

        response = Response(generate_bti(url, download_full_report), mimetype='text/csv' )
        response.headers['Content-Disposition'] = 'attachment; filename=report.csv'
        return response

    return render_template('index.html')

