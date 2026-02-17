from markupsafe import Markup
import json
import urllib.request
from flask import Flask, request, jsonify, render_template
from datetime import datetime
from dateutil.relativedelta import relativedelta
import jinja2
import pdfkit
import os
import ast

app = Flask(__name__)
# Configuration
OUTPUT_FOLDER = 'HTML_FORM'
os.makedirs(OUTPUT_FOLDER, exist_ok=True)

cf_port = os.getenv("PORT")

@app.route('/printpo', methods=['POST'])
def printpo():
    data = request.get_json()   
    json_string = json.dumps(data)
    json_output = json.loads(json_string) 
    python_list = ast.literal_eval(json_output)
    print(type(python_list))
    print(python_list)
    for item in python_list:
        ponumber = item["ponumber"]
        vendor = item["vendor"]
        addrs = item["addrs"]
        shipto = item["shipto"]
        addr2 = item["addr2"]
        podate = item["podate"]
        currency = item["currency"]
        totamt = item["totamt"]
        subtotal = item["subtotal"]
        tottax = item["tottax"]
        shipcost = item["shipcost"]
        othercost = item["othercost"]
        reqname = item["reqname"]
        incoterms = item["incoterms"]

    context = {
            'ponumber': ponumber,
            'vendor': vendor,
            'addrs': addrs,
            'shipto': shipto,
            'addr2': addr2,
            'podate': podate,
            'currency': currency,
            'totamt': totamt,
            'subtotal': subtotal,
            'tottax': tottax,
            'shipcost': shipcost,
            'othercost': othercost,
            'reqname': reqname,
            'incoterms': incoterms,
            'items': python_list
        }        
    # Render template
    rendered_html = render_template('page.html', **context)  
    # Save to file
    filename = f"page_{datetime.now().strftime('%Y%m%d_%H%M%S')}.html"
    filepath = os.path.join(OUTPUT_FOLDER, filename)      
    with open(filepath, 'w', encoding='utf-8') as f:
         f.write(rendered_html)
        
    return jsonify({
            'success': True,
            'message': 'HTML file generated successfully',
            'filename': filename,
            'path': os.path.abspath(filepath)
        })
    return render_template("index.html", data = json_output)
if __name__ == "__main__":
    app.run()
       