from flask import Flask, render_template_string, request, redirect, session

app = Flask(__name__)
app.secret_key = 'vedant_agro_secret_key'

# Initial Data Storage
stock_list = [{'id': 1, 'item': 'Fertilizer', 'qty': 50, 'price': 500}]
accounts_list = [{'id': 1, 'desc': 'Sales', 'amount': 25000, 'type': 'Income', 'month': 'November', 'year': '2025'}]
staff_list = [{'id': 1, 'name': 'Rakesh', 'position': 'Manager', 'salary': 15000, 'month': 'November', 'year': '2025'}]
custom_tables = {}

@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        if request.form.get('email') in ['Vedantvilask755@gmail.com', 'vedantpersonal755@gmail.com', 'admin@vkagro.com']:
            session['user'] = request.form.get('email')
            return redirect('/dash')
        return '<h3>Access Denied! <a href="/">Back</a></h3>'
    return '''<body style="font-family:Arial;display:flex;justify-content:center;align-items:center;height:100vh;background:#f4f4f9;">
    <div style="background:white;padding:30px;border-radius:8px;text-align:center;box-shadow:0 4px 10px rgba(0,0,0,0.1);">
    <h2 style="color:#2e7d32;">🌱 Vedant Agro</h2>
    <form method="POST"><input type="email" name="email" placeholder="Enter authorized email" required style="width:100%;padding:10px;margin:10px 0;box-sizing:border-box;"><button type="submit" style="background:#2e7d32;color:white;border:none;padding:10px;width:100%;border-radius:4px;">Login</button></form>
    </div></body>'''

@app.route('/dash', methods=['GET', 'POST'])
def dash():
    if 'user' not in session: return redirect('/')
    global stock_list, accounts_list, staff_list, custom_tables
    
    m = request.form.get('filter_month', 'November')
    y = request.form.get('filter_year', '2025')
    
    if request.method == 'POST':
        act = request.form.get('action')
        
        # Working AI Command Parser
        if act == 'ai_command':
            cmd = request.form.get('ai_text', '').strip()
            try:
                if "add table" in cmd.lower():
                    # Format: Add Table: Fertilizer Stock | Columns: Item, Qty, Rate
                    parts = cmd.split('|')
                    t_name = parts[0].split(':')[1].strip()
                    cols = ['Item', 'Quantity', 'Price']
                    if len(parts) > 1 and 'column' in parts[1].lower():
                        cols = [c.strip() for c in parts[1].split(':')[1].split(',')]
                    t_id = 't_' + str(len(custom_tables) + 1)
                    custom_tables[t_id] = {'name': t_name, 'columns': cols, 'rows': []}
                elif "add row" in cmd.lower():
                    # Format: Add Row: t_1 | Urea, 50, 350
                    parts = cmd.split('|')
                    t_id = parts[0].split(':')[1].strip()
                    row_data = [d.strip() for d in parts[1].split(',')]
                    if t_id in custom_tables:
                        r_id = len(custom_tables[t_id]['rows']) + 1
                        custom_tables[t_id]['rows'].append({'id': r_id, 'data': row_data})
            except Exception as e:
                print("AI Command Error:", e)

        elif act == 'create_custom_table':
            t_name = request.form.get('table_name', 'My Table')
            cols = [c.strip() for c in request.form.get('table_cols', 'Item, Quantity, Price').split(',')]
            t_id = 't_' + str(len(custom_tables) + 1)
            custom_tables[t_id] = {'name': t_name, 'columns': cols, 'rows': []}
        elif act == 'add_custom_row':
            t_id = request.form.get('table_id')
            if t_id in custom_tables:
                col_count = len(custom_tables[t_id]['columns'])
                row_data = [request.form.get(f'col_{i}', '') for i in range(col_count)]
                r_id = len(custom_tables[t_id]['rows']) + 1
                custom_tables[t_id]['rows'].append({'id': r_id, 'data': row_data})
        elif act == 'delete_custom_table':
            t_id = request.form.get('table_id')
            if t_id in custom_tables: del custom_tables[t_id]
        elif act == 'delete_custom_row':
            t_id = request.form.get('table_id')
            r_id = int(request.form.get('row_id'))
            if t_id in custom_tables:
                custom_tables[t_id]['rows'] = [r for r in custom_tables[t_id]['rows'] if r['id'] != r_id]

        # Standard Management Actions
        elif act == 'add_staff':
            staff_list.append({'id': len(staff_list)+1, 'name': request.form.get('name'), 'position': request.form.get('position'), 'salary': float(request.form.get('salary')), 'month': m, 'year': y})
        elif act == 'del_staff':
            staff_list = [s for s in staff_list if s['id'] != int(request.form.get('id'))]
        elif act == 'add_stock':
            stock_list.append({'id': len(stock_list)+1, 'item': request.form.get('item'), 'qty': int(request.form.get('qty')), 'price': float(request.form.get('price'))})
        elif act == 'del_stock':
            stock_list = [st for st in stock_list if st['id'] != int(request.form.get('id'))]
        elif act == 'add_acc':
            accounts_list.append({'id': len(accounts_list)+1, 'desc': request.form.get('desc'), 'amount': float(request.form.get('amount')), 'type': request.form.get('type'), 'month': m, 'year': y})
        elif act == 'del_acc':
            accounts_list = [acc for acc in accounts_list if acc['id'] != int(request.form.get('id'))]

    # Filtered Data
    f_stf = [s for s in staff_list if s.get('month', 'November') == m and s.get('year', '2025') == y]
    f_acc = [a for a in accounts_list if a.get('month', 'November') == m and a.get('year', '2025') == y]
    
    inc = sum(a['amount'] for a in f_acc if a['type'] == 'Income')
    exp = sum(a['amount'] for a in f_acc if a['type'] == 'Expense')
    sal = sum(s['salary'] for s in f_stf)
    net = inc - (exp + sal)

    months = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December']
    years = ['2024', '2025', '2026', '2027']

    html = '''
    <body style="font-family:Arial;background:#f4f4f9;padding:15px;margin:0;">
    <div style="background:#2e7d32;color:white;padding:15px;border-radius:8px;display:flex;justify-content:space-between;align-items:center;">
    <h2>🌱 Vedant Agro</h2><div><span>{{user}}</span> | <a href="/logout" style="color:white;background:#d32f2f;padding:5px 10px;text-decoration:none;border-radius:4px;">Logout</a></div></div>

    <!-- AI & Custom Table Creator Box -->
    <div style="background:#e8f5e9;padding:15px;margin-top:15px;border-radius:8px;box-shadow:0 2px 5px rgba(0,0,0,0.1);border-left:5px solid #2e7d32;">
    <h3>🤖 AI Assistant & Dynamic Table Builder</h3>
    <p style="font-size:13px;color:#555;">
        <b>AI Command Examples:</b><br>
        • Create Table: <code>Add Table: Fertilizer Stock | Columns: Item, Qty, Rate</code><br>
        • Add Row: <code>Add Row: t_1 | Urea, 50, 350</code>
    </p>
    <form method="POST">
    <input type="hidden" name="action" value="ai_command">
    <input type="text" name="ai_text" placeholder="Type AI command here..." required style="padding:10px;width:100%;margin:5px 0;box-sizing:border-box;border:1px solid #c8e6c9;border-radius:4px;">
    <button type="submit" style="background:#2e7d32;color:white;border:none;padding:10px;border-radius:4px;width:100%;">Run AI Command</button>
    </form>
    <hr style="margin:15px 0;border:0;border-top:1px solid #c8e6c9;">
    <h4>Manual Table Creator</h4>
    <form method="POST">
    <input type="hidden" name="action" value="create_custom_table">
    <input type="text" name="table_name" placeholder="Table Name (e.g. Daily Expenses)" required style="padding:8px;width:100%;margin:5px 0;box-sizing:border-box;">
    <input type="text" name="table_cols" placeholder="Columns by comma (e.g. Item, Qty, Price)" required style="padding:8px;width:100%;margin:5px 0;box-sizing:border-box;">
    <button type="submit" style="background:#1565c0;color:white;border:none;padding:10px;border-radius:4px;width:100%;">Create Blank Table</button>
    </form>
    </div>

    <!-- Render Custom Tables -->
    {% for t_id, t_data in custom_tables.items() %}
    <div style="background:white;padding:15px;margin-top:15px;border-radius:8px;box-shadow:0 2px 5px rgba(0,0,0,0.1);">
    <div style="display:flex;justify-content:space-between;align-items:center;">
    <h3 style="color:#1565c0;margin:0;">📋 {{ t_data.name }} <span style="font-size:12px;color:#888;">(Table ID: {{ t_id }})</span></h3>
    <form method="POST" style="margin:0;"><input type="hidden" name="action" value="delete_custom_table"><input type="hidden" name="table_id" value="{{ t_id }}"><button type="submit" style="background:#d32f2f;color:white;border:none;padding:5px 10px;border-radius:4px;font-size:12px;">Delete Table</button></form>
    </div>
    <table border="1" style="width:100%;border-collapse:collapse;font-size:14px;margin-top:10px;">
    <tr>{% for col in t_data.columns %}<th>{{ col }}</th>{% endfor %}<th>Action</th></tr>
    {% for row in t_data.rows %}
    <tr>{% for val in row.data %}<td>{{ val }}</td>{% endfor %}
    <td><form method="POST" style="margin:0;"><input type="hidden" name="action" value="delete_custom_row"><input type="hidden" name="table_id" value="{{ t_id }}"><input type="hidden" name="row_id" value="{{ row.id }}"><button type="submit" style="background:#d32f2f;color:white;border:none;padding:3px 6px;border-radius:4px;font-size:11px;">Delete</button></form></td></tr>
    {% endfor %}
    </table>
    <form method="POST" style="margin-top:15px;background:#f9f9f9;padding:10px;border-radius:6px;">
    <input type="hidden" name="action" value="add_custom_row"><input type="hidden" name="table_id" value="{{ t_id }}">
    <p style="margin:0 0 5px 0;font-size:13px;font-weight:bold;">Add Row Data:</p>
    <div style="display:flex;gap:5px;flex-wrap:wrap;">
    {% for col in t_data.columns %}
    <input type="text" name="col_{{ loop.index0 }}" placeholder="{{ col }}" required style="padding:8px;flex:1;min-width:100px;box-sizing:border-box;">
    {% endfor %}
    </div>
    <button type="submit" style="background:#2e7d32;color:white;border:none;padding:8px;border-radius:4px;width:100%;margin-top:8px;">Add Row</button>
    </form>
    </div>
    {% endfor %}

    <!-- Global Month & Year Filter -->
    <div style="background:white;padding:15px;margin-top:15px;border-radius:8px;">
    <h3>🔍 Filter Month & Year</h3>
    <form method="POST" style="display:flex;gap:10px;">
    <select name="filter_month" style="padding:8px;width:100%;"><option value="{{m}}">{{m}}</option>{% for mo in months %}<option value="{{mo}}">{{mo}}</option>{% endfor %}</select>
    <select name="filter_year" style="padding:8px;width:100%;"><option value="{{y}}">{{y}}</option>{% for yr in years %}<option value="{{yr}}">{{yr}}</option>{% endfor %}</select>
    <button type="submit" style="background:#2e7d32;color:white;border:none;padding:8px 15px;border-radius:4px;">Filter</button>
    </form></div>

    <!-- Summary -->
    <div style="background:white;padding:15px;margin-top:15px;border-radius:8px;">
    <h3>📊 Summary for {{m}} {{y}}</h3>
    <p><b>Income:</b> ₹{{inc}} | <b>Expenses:</b> ₹{{exp}} | <b>Salaries:</b> ₹{{sal}}</p>
    <p><b>Net Profit/Loss:</b> <span style="color:{% if net >= 0 %}green{% else %}red{% endif %};font-weight:bold;">₹{{net}}</span></p></div>

    <!-- Staff Section -->
    <div style="background:white;padding:15px;margin-top:15px;border-radius:8px;">
    <h3>👥 Staff Management</h3>
    <table border="1" style="width:100%;border-collapse:collapse;font-size:14px;"><tr><th>Name</th><th>Position</th><th>Salary</th><th>Action</th></tr>
    {% for s in staff %}<tr><td>{{s.name}}</td><td>{{s.position}}</td><td>₹{{s.salary}}</td><td>
    <form method="POST" style="margin:0;"><input type="hidden" name="action" value="del_staff"><input type="hidden" name="id" value="{{s.id}}"><button type="submit" style="background:#d32f2f;color:white;border:none;padding:4px 8px;">Delete</button></form>
    </td></tr>{% endfor %}</table>
    <form method="POST" style="margin-top:10px;"><input type="hidden" name="action" value="add_staff">
    <input type="text" name="name" placeholder="Name" required style="padding:8px;width:100%;margin:5px 0;">
    <input type="text" name="position" placeholder="Position" required style="padding:8px;width:100%;margin:5px 0;">
    <input type="number" name="salary" placeholder="Salary" required style="padding:8px;width:100%;margin:5px 0;">
    <button type="submit" style="background:#2e7d32;color:white;border:none;padding:10px;width:100%;">Add Staff</button></form></div>

    <!-- Stock Section -->
    <div style="background:white;padding:15px;margin-top:15px;border-radius:8px;">
    <h3>📦 Stock Management</h3>
    <table border="1" style="width:100%;border-collapse:collapse;font-size:14px;"><tr><th>Item</th><th>Qty</th><th>Price</th><th>Action</th></tr>
    {% for st in stock %}<tr><td>{{st.item}}</td><td>{{st.qty}}</td><td>₹{{st.price}}</td><td>
    <form method="POST" style="margin:0;"><input type="hidden" name="action" value="del_stock"><input type="hidden" name="id" value="{{st.id}}"><button type="submit" style="background:#d32f2f;color:white;border:none;padding:4px 8px;">Delete</button></form>
    </td></tr>{% endfor %}</table>
    <form method="POST" style="margin-top:10px;"><input type="hidden" name="action" value="add_stock">
    <input type="text" name="item" placeholder="Item Name" required style="padding:8px;width:100%;margin:5px 0;">
    <input type="number" name="qty" placeholder="Quantity" required style="padding:8px;width:100%;margin:5px 0;">
    <input type="number" step="0.01" name="price" placeholder="Price" required style="padding:8px;width:100%;margin:5px 0;">
    <button type="submit" style="background:#2e7d32;color:white;border:none;padding:10px;width:100%;">Add Stock</button></form></div>

    <!-- Accounts Section -->
    <div style="background:white;padding:15px;margin-top:15px;border-radius:8px;">
    <h3>💰 Accounts / Transactions</h3>
    <table border="1" style="width:100%;border-collapse:collapse;font-size:14px;"><tr><th>Desc</th><th>Amount</th><th>Type</th><th>Action</th></tr>
    {% for acc in accounts %}<tr><td>{{acc.desc}}</td><td>₹{{acc.amount}}</td><td>{{acc.type}}</td><td>
    <form method="POST" style="margin:0;"><input type="hidden" name="action" value="del_acc"><input type="hidden" name="id" value="{{acc.id}}"><button type="submit" style="background:#d32f2f;color:white;border:none;padding:4px 8px;">Delete</button></form>
    </td></tr>{% endfor %}</table>
    <form method="POST" style="margin-top:10px;"><input type="hidden" name="action" value="add_acc">
    <input type="text" name="desc" placeholder="Description" required style="padding:8px;width:100%;margin:5px 0;">
    <input type="number" step="0.01" name="amount" placeholder="Amount" required style="padding:8px;width:100%;margin:5px 0;">
    <select name="type" style="padding:8px;width:100%;margin:5px 0;"><option value="Income">Income</option><option value="Expense">Expense</option></select>
    <button type="submit" style="background:#2e7d32;color:white;border:none;padding:10px;width:100%;">Add Transaction</button></form></div>
    </body>
    '''
    return render_template_string(html, user=session['user'], staff=f_stf, stock=stock_list, accounts=f_acc, m=m, y=y, months=months, years=years, inc=inc, exp=exp, sal=sal, net=net, custom_tables=custom_tables)

@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)
