```python
from flask import Flask, render_template, request, redirect, url_for
import json
import os

app = Flask(__name__)
DATA_FILE = 'shipments.json'

def load_shipments():
    if not os.path.exists(DATA_FILE):
        with open(DATA_FILE, 'w') as f:
            json.dump([], f)
    with open(DATA_FILE, 'r') as f:
        return json.load(f)

def save_shipments(data):
    with open(DATA_FILE, 'w') as f:
        json.dump(data, f, indent=4)

@app.route('/')
def index():
    shipments = load_shipments()
    return render_template('index.html', shipments=shipments)

@app.route('/add', methods=['GET', 'POST'])
def add_shipment():
    if request.method == 'POST':
        shipments = load_shipments()
        new_shipment = {
            "id": len(shipments) + 1,
            "client": request.form['client'],
            "address": request.form['address'],
            "status": request.form['status']
        }
        shipments.append(new_shipment)
        save_shipments(shipments)
        return redirect(url_for('index'))
    return render_template('add.html')

@app.route('/delete/<int:id>')
def delete_shipment(id):
    shipments = load_shipments()
    shipments = [s for s in shipments if s['id']!= id]
    save_shipments(shipments)
    return redirect(url_for('index'))

@app.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit_shipment(id):
    shipments = load_shipments()
    shipment = next((s for s in shipments if s['id'] == id), None)
    if request.method == 'POST':
        shipment['client'] = request.form['client']
        shipment['address'] = request.form['address']
        shipment['status'] = request.form['status']
        save_shipments(shipments)
        return redirect(url_for('index'))
    return render_template('edit.html', shipment=shipment)

if __name__ == '__main__':
    app.run(debug=True)
```
