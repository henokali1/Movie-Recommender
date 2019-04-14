from flask import Flask, render_template, redirect, url_for, session, request, logging, json


app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
app.config['DEBUG'] = True

#turn the flask app into a socketio app


@app.route('/', methods=['GET', 'POST'])
def index():
    return render_template('index.html')

# Register
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        email = request.form.get('user_email')
        psw = request.form.get('user_password')
        print(email, psw)
        return render_template('register.html')
    return render_template('register.html')

# Login
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('user_email')
        psw = request.form.get('user_password')
        print(email, psw)
        return render_template('login.html')
    return render_template('login.html')



if __name__ == '__main__':
    app.run(host='0.0.0.0')
    #app.run()
