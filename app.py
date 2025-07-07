from flask import Flask, render_template, request, send_file
import uuid
import os
import pdfkit

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('form.html')

@app.route('/generate', methods=['POST'])
def generate_invoice():
    data = request.form

    items = []
    for i in range(len(data.getlist('item_name'))):
        items.append({
            'name': data.getlist('item_name')[i],
            'qty': int(data.getlist('item_qty')[i]),
            'price': float(data.getlist('item_price')[i])
        })

    invoice_id = str(uuid.uuid4())

    html = render_template('invoice.html', data=data, items=items, invoice_id=invoice_id)

    if not os.path.exists('invoices'):
        os.makedirs('invoices')

    filepath = f'invoices/invoice_{invoice_id}.pdf'

    pdfkit.from_string(html, filepath)

    return send_file(filepath, as_attachment=True)

if __name__ == '__main__':
    app.run(debug=True)
