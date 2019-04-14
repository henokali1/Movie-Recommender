from flask import Flask, render_template, redirect, url_for, session, request, logging, json
import json


app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
app.config['DEBUG'] = True

#turn the flask app into a socketio app


def del_db_data():
	with open('lp_db.txt', 'w') as outfile:
		json.dump({}, outfile)

def read_db():
    with open('lp_db.txt') as json_file:  
        data = json.load(json_file)
    return data


def save_db(lp_num, ident, city):
    existing_data = read_db()
    existing_data[lp_num] = {'ident':ident, 'city':city}
    with open('lp_db.txt', 'w') as outfile:  
        json.dump(existing_data, outfile)


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        lp_num = request.form.get('lp_num')
        city = request.form.get('city')
        ident = request.form.get('lp_ident')
        print(city, ident)

        save_db(lp_num, ident.upper(), city.upper())
    return render_template('index.html', all_lps=read_db())

# Register
@app.route('/register', methods=['GET', 'POST'])
def register():
    return render_template('register.html')

# Login
@app.route('/login', methods=['GET', 'POST'])
def login():
    return render_template('login.html')


@app.route('/del/<string:id>', methods=['GET', 'POST'])
def del_lp(id):
    all_lps=read_db()
    try:
        del all_lps[id]
        with open('lp_db.txt', 'w') as outfile:  
            json.dump(all_lps, outfile)
        return redirect(url_for('index'))
    except KeyError:
        return redirect(url_for('index'))
    return redirect(url_for('index'))


if __name__ == '__main__':
    app.run(host='0.0.0.0')
