from flask import render_template,redirect,request,url_for,flash
from flask_login import login_user,logout_user,login_required,current_user
from . import auth
from ..models import User,Role,Post,Permission
from .forms import LoginForm,RegistrationForm,ChangePasswordForm
from .. import db
#from decorators import admin_required, permission_required
#from .models import Permission

@auth.before_app_request
def before_request():
    if current_user.is_authenticated:
        current_user.ping()
    

@auth.route('/login',methods=['GET','POST'])
def login():
    form=LoginForm()
    if form.validate_on_submit():
        user=User.query.filter_by(email=form.email.data).first()
        if user is not None and user.verify_password(form.password.data):
            #login_user把用户标记为已经登陆
            #login_user(user,form.remember_me.data)
            login_user(user,False) #不让下次登录记住用户
            return redirect(request.args.get('next') or url_for('main.index'))
        flash('Invalid username or password.')
    return render_template('auth/login.html',form=form)

@auth.route('/logout')
@login_required
def logout():
    #删除并重设用户会话
    logout_user()
    flash('您已经退出登陆.')
    return redirect(url_for('main.index'))

@auth.route('/register',methods=['GET','POST'])
def register():
    form=RegistrationForm()
    if form.validate_on_submit():
        user=User(email=form.email.data,username=form.username.data,password=form.password.data)
        db.session.add(user)
        flash('You can now login.')
        return redirect(url_for('auth.login'))
    return render_template('auth/register.html', form=form)

@auth.route('/change-password',methods=['GET','POST'])
@login_required
def change_password():
    form = ChangePasswordForm()
    if form.validate_on_submit():
        if current_user.verify_password(form.old_password.data):
            current_user.password = form.password.data
            db.session.add(current_user)
            flash('Your password has been updated.')
            return redirect(url_for('main.index'))
        else:
            flash('Invalid password.')
    return render_template('auth/change_password.html',form=form)










