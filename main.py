
'''
WORK IN PROGRESS: CHANGES ARE BEING MADE
'''

# Flask program to send form data over to database
from flask import Flask, render_template, url_for, request, flash, redirect
from db_handler import MySQLDB

app = Flask(__name__)
app.secret_key = 'beautiful_waste'
db = MySQLDB()

@app.route('/')
def homepage():
    return render_template('home.html')
    
@app.route('/redirect')
def external():
    return redirect( 'http://www.freepik.com/free-photo/high-view-leftover-foodstuff-used-napkins_11067434.htm#query=food%20waste&position=3&from_view=keyword&track=ais&uuid=931e18c3-c297-4493-b94e-100fb249e9c2')
    
@app.route('/about')
def about():
    return render_template('about.html')
    
@app.route('/contact')
def contact():
    return render_template('contact.html')
    
@app.route('/donate', methods=['GET', 'POST'])
def donate(): 
    if request.method == 'POST':
        name  = request.form.get('myname')
        email = request.form.get('myemail')
        pno   = request.form.get('myphone')
        addr  = request.form.get('myaddr')
        type  = request.form.get('myfood')
        qty   = request.form.get('quantity')
        prep  = request.form.get('fooddate')
        
        # string = ' '.join([name, email, pno, addr, type, qty, prep])
        # flash(string)
        
        db.add_request(name, email, pno, addr, type, qty, prep)
    
    return render_template('donate.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        if request.form['account'] == 'Register':
            name  = request.form.get('username');
            email = request.form.get('useremail');
            pwd   = request.form.get('userpwd');
            code  = request.form.get('usercode');
            
            # string = ' '.join([name, email, pwd])
            # flash(string)
            if code == '1001':
                role = 'Admin'
            elif code == '2047':
                role = 'Agent'
            else:
                role = 'Donor'
            db.add_account(name, email, pwd, role)
            id = db.check_account(email, pwd)
            return redirect(url_for(role.lower(), id=id))
            
        elif request.form['account'] == 'SignIn':
            email = request.form.get('useremail');
            pwd   = request.form.get('userpwd');
            
            rec_code = db.check_account(email, pwd)
            # Error 101 - Email doesn't exist
            if rec_code == 'E101':
                flash('There is no account with that email, please register.')
            # Error 210 - Email exists, but password is wrong
            elif rec_code == 'E210':
                flash('The password given is incorrect.')
            else:
                if rec_code[0] == 'D':
                    return redirect(url_for('admin', id=rec_code))
                elif rec_code[0] == 'G':
                    return redirect(url_for('agent', id=rec_code))
                else:
                    return redirect(url_for('donor', id=rec_code))

    return render_template('login.html')
    

@app.route('/donor/<id>')
def donor(id):
    data = db.get_account(id)
    record = {
        'accid': data[0],
        'name': data[1],
        'email': data[2]
    }
    return render_template('donor.html', record=record)

@app.route('/admin/<id>')
def admin(id):
    data = db.get_account(id)
    acclist = db.get_accounts()
    reqlist = db.get_requests()
    record = {
        'accid': data[0],
        'name': data[1],
        'email': data[2]
    }
    return render_template('admin.html', record=record, acclist=acclist, reqlist=reqlist)

@app.route('/admin/<recid>/removing+acc+<id>')
def remove_acc(id):
    db.del_account(id)
    
@app.route('/admin/<recid>/removing+req+<id>')
def remove_req(id):
    db.del_request(id)

@app.route('/agent/<id>')
def agent(id):
    data = db.get_account(id)
    reqlist = db.get_requests()
    record = {
        'accid': data[0],
        'name': data[1],
        'email': data[2]
    }
    return render_template('agent.html', record=record, reqlist=reqlist)

if __name__ == '__main__':
    app.run(debug = True, host='0.0.0.0')