from flask import Flask, render_template_string, request, redirect, session

app = Flask(__name__)
app.secret_key = 'vedant_key'

@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        if request.form.get('email') in ['Vedantvilask755@gmail.com', 'vedantpersonal755@gmail.com']:
            session['user'] = request.form.get('email')
            return redirect('/dash')
        return '<h3>Access Denied! <a href="/">Try Again</a></h3>'
    return '''<body style="font-family:Arial;text-align:center;padding:50px;">
    <h2>🌱 Vedant Agro Login</h2>
    <form method="POST"><input type="email" name="email" placeholder="Enter Email" required style="padding:10px;width:250px;"><br><br>
    <button type="submit" style="background:green;color:white;padding:10px 20px;">Login</button></form></body>'''

@app.route('/dash')
def dash():
    if 'user' not in session: return redirect('/')
    return '''<body style="font-family:Arial;padding:20px;">
    <h2>🌱 Vedant Agro Dashboard</h2>
    <p>Welcome! Successfully logged in.</p>
    <a href="/">Logout</a></body>'''

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
