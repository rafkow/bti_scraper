from bs4 import BeautifulSoup
import requests
from math import ceil
import re
import time


def get_bti_full(bti_reference, headers):
    url_bti_full = f'https://ec.europa.eu/taxation_customs/dds2/ebti/ebti_details.jsp?reference={bti_reference}&excludekeywordsearch=&orderby=0&excludespecialkeyword=%22'
    result = requests.get(url_bti_full, headers=headers)
    doc = BeautifulSoup(result.text, "html.parser")
    tables = doc.find_all("table")
    rows = tables[1].find_all("tr", class_="ecl-table__row")[1:]
    justification = rows[5].find_all("td")[1].text.strip().replace('\n', '').replace(';', ' ')
    description = rows[10].find_all("td")[1].text.strip().replace('\n', '').replace(';', ' ')
    return [justification, description]


def get_bti(url_address, full_report, window = None):
    url_login = "https://ec.europa.eu/taxation_customs/dds2/ebti/ebti_consultation.jsp"
    result = requests.get(url_login)
    headers = result.headers
    headers['Cookie'] = result.headers['Set-Cookie'].split(';')[0]

    start_date = re.search('&valstartdate=([^&]*)&', url_address).group(1)
    end_date = re.search('&valenddate=([^&]*)&', url_address).group(1)
    offset = 1
    url_bti_list = f'https://ec.europa.eu/taxation_customs/dds2/ebti/ebti_list.jsp?offset={offset}&allRecords=1&valstartdate={start_date}&valenddate={end_date}'
    result = requests.get(url_bti_list, headers=headers)
    doc = BeautifulSoup(result.text, "html.parser")

    record_counter = int(doc.p.text.strip()) if doc.p.text.strip().isdecimal() else None
    page_counter = ceil(record_counter / 25)
    current_record = 1

    start_time = time.time()

    try:
        with open(f'{start_date.lower().replace("%2f","-")}_{end_date.lower().replace("%2f","-")}.csv', 'w', encoding="utf-8") as csv:
            column_header = ['BTI Reference', 'Nomenclature Code', 'Start date of validity', 'End date of validity',
                             'Number of images', 'Justification', 'Description']
            if full_report:
                csv.write(f'{";".join(column_header)}\n')
            else:
                csv.write(f'{";".join(column_header[:4])}\n')

            for offset in range(1, page_counter+1):
                url_bti_list = f'https://ec.europa.eu/taxation_customs/dds2/ebti/ebti_list.jsp?offset={offset}&allRecords=1&valstartdate={start_date}&valenddate={end_date}'
                result = requests.get(url_bti_list, headers=headers)
                doc = BeautifulSoup(result.text, "html.parser")
                if result.status_code == 200:
                    tbody = doc.find('tbody')
                    for tr in tbody.find_all('tr', class_='ecl-table__row'):
                        values = [td.text.strip() for td in tr.find_all('td')]
                        if full_report:
                            try:
                                values.extend(get_bti_full(values[0], headers))
                            except Exception:
                                pass
                        try:
                            csv.write(f'{";".join(values)}\n')
                        except UnicodeEncodeError:
                            csv.write(f'{values[0]};')
                        if window:
                            window.bar['value'] = current_record / record_counter * 100
                            window.infoLabel.config(text=f"Collecting data: {current_record}/{record_counter} records time:{time.time() - start_time:.2f}s")
                            window.update_idletasks()
                        current_record += 1
    except PermissionError:
        if window:
            window.infoLabel.config(text=f"I cant replace result file, probably is open on your computer")


def generate_bti(url_address, full_report):
    url_login = "https://ec.europa.eu/taxation_customs/dds2/ebti/ebti_consultation.jsp"
    result = requests.get(url_login)
    headers = result.headers
    headers['Cookie'] = result.headers['Set-Cookie'].split(';')[0]

    start_date = re.search('&valstartdate=([^&]*)&', url_address).group(1)
    end_date = re.search('&valenddate=([^&]*)&', url_address).group(1)
    offset = 1
    url_bti_list = f'https://ec.europa.eu/taxation_customs/dds2/ebti/ebti_list.jsp?offset={offset}&allRecords=1&valstartdate={start_date}&valenddate={end_date}'
    result = requests.get(url_bti_list, headers=headers)
    doc = BeautifulSoup(result.text, "html.parser")

    record_counter = int(doc.p.text.strip()) if doc.p.text.strip().isdecimal() else None
    page_counter = ceil(record_counter / 25)
    current_record = 1
    data = []

    column_header = ['BTI Reference', 'Nomenclature Code', 'Start date of validity', 'End date of validity',
                             'Number of images', 'Justification', 'Description']
    if full_report:
        yield  f'{";".join(column_header)}\n'
    else:
        yield f'{";".join(column_header[:4])}\n'

    for offset in range(1, page_counter+1):
        url_bti_list = f'https://ec.europa.eu/taxation_customs/dds2/ebti/ebti_list.jsp?offset={offset}&allRecords=1&valstartdate={start_date}&valenddate={end_date}'
        result = requests.get(url_bti_list, headers=headers)
        doc = BeautifulSoup(result.text, "html.parser")
        if result.status_code == 200:
            tbody = doc.find('tbody')
            for tr in tbody.find_all('tr', class_='ecl-table__row'):
                values = [td.text.strip() for td in tr.find_all('td')]
                if full_report:
                    try:
                        values.extend(get_bti_full(values[0], headers))
                    except Exception:
                        pass
                current_record += 1
                yield f'{";".join(values)}\n'
                
