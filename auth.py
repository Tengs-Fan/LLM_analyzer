from user import User
from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_user, logout_user, login_required
 
auth = Blueprint('auth', __name__)

@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        user_id = request.form.get('user_id')
        password = request.form.get('password')
        user = User.get(user_id)
        if user and user.check_password(password):
            login_user(user)
            flash('Logged in successfully.')
            return redirect(url_for('index'))
        else:
            flash('Invalid username or password.')
    return render_template('login.html')

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))


# somewhere to login
# @app.route("/login", methods=["GET", "POST"])
# def login():
#     if request.method == 'POST':
#         username = request.form['username']
#         password = request.form['password']        
#         if password == username + "_secret":
#             id = username.split('user')[1]
#             user = User(id)
#             login_user(user)
#             return redirect(request.args.get("next"))
#         else:
#             return abort(401)
#     else:
#         return Response('''
#         <form action="" method="post">
#             <p><input type=text name=username>
#             <p><input type=password name=password>
#             <p><input type=submit value=Login>
#         </form>
#         ''')
