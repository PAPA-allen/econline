from flask import Blueprint
from flask import render_template, url_for, redirect, request, jsonify, make_response, flash
from flask_login import login_user, current_user, logout_user, login_required
from econline import bcrypt, db
import logging
from econline.models import Admin, Election
from econline.forms import LoginForm, NewAdminForm, NewElectionForm, EditElectionNameForm, EditElectionDateForm
import datetime


admin = Blueprint('admin', __name__)

@admin.route('/admin/login', methods=['POST', 'GET'])
def admin_login():
    if current_user.is_authenticated:
        return redirect(url_for('admin.admin_landing'))
    
    form = LoginForm()
    if form.validate_on_submit():
        admin = Admin.query.filter_by(email=form.email.data).first()
        if admin and bcrypt.check_password_hash(admin.password, form.password.data):
            login_user(admin)
            return redirect(url_for('admin.admin_landing'))
        else:
            flash('Your email/password don\'t match.', 'danger')
            
    return render_template('admin-login.html', title="Admin Login", form=form)


@login_required
@admin.route('/admin/landing', methods=['POST', 'GET'])
def admin_landing():
    election_form = NewElectionForm()
    if request.method == "POST" and election_form.validate_on_submit():
        # converting dates and times to string then joining them
        start_at = election_form.start_date.data.strftime("%Y-%m-%d")+ " " + election_form.end_time.data.strftime("%H:%M")
        end_at = election_form.end_date.data.strftime("%Y-%m-%d") + " " + election_form.end_time.data.strftime("%H:%M")
        
        #chaging str back to datetime and inserting to db
        new_election = Election(name=election_form.name.data, start_at=datetime.datetime.strptime(start_at, "%Y-%m-%d %H:%M"), end_at=datetime.datetime.strptime(end_at, "%Y-%m-%d %H:%M"))
        db.session.add(new_election)
        db.session.commit()
        
        flash('New Election Added', 'success')
        return redirect(url_for('admin.admin_election', election_id=new_election.id))
    
    election_list = Election.query.all()
    
    return render_template("admin-landing.html", title="EC Landing", election_form=election_form, election_list=election_list)


@login_required
@admin.route('/admin/election', methods=['POST', 'GET'])
@admin.route('/admin/election/<election_id>', methods=['POST', 'GET'])
def admin_election(election_id):
    election = Election.query.filter_by(id=election_id).first()
    
    return render_template('admin-election.html', title=election.name, election=election)


@login_required
@admin.route('/admin/election/settings', methods=['POST', 'GET'])
@admin.route('/admin/election/settings/<election_id>', methods=['POST', 'GET'])
def election_settings(election_id):
    election = Election.query.filter_by(id=election_id).first()
    
    edit_name = EditElectionNameForm()
    if edit_name.submit_name.data and edit_name.validate_on_submit():
        election.name = edit_name.name.data
        db.session.commit()
        flash('Election Name Updated', 'success')
        return redirect(url_for('admin.election_settings', election_id=election.id))
    
    edit_date = EditElectionDateForm()
    if edit_date.submit_date.data and edit_date.validate_on_submit():
        start_at = edit_date.start_date.data.strftime("%Y-%m-%d")+ " " + edit_date.end_time.data.strftime("%H:%M")
        end_at = edit_date.end_date.data.strftime("%Y-%m-%d") + " " + edit_date.end_time.data.strftime("%H:%M")
        
        election.start_at = datetime.datetime.strptime(start_at, "%Y-%m-%d %H:%M")
        election.end_at = datetime.datetime.strptime(end_at, "%Y-%m-%d %H:%M")
        
        db.session.commit()
        flash('Election Date and Time Updated', 'success')
        return redirect(url_for('admin.election_settings', election_id=election.id))
    
    return render_template('election-settings.html', title=election.name, election=election, edit_name=edit_name, edit_date=edit_date)


@login_required
@admin.route('/admin/election/delete', methods=['POST'])
@admin.route('/admin/election/delete/<election_id>', methods=['POST'])
def election_delete(election_id):
    election = Election.query.filter_by(id=election_id).first()
    if election:
        db.session.delete(election)
        db.session.commit()
        flash('Election Deleted', 'info')
        return redirect(url_for('admin.admin_landing'))
    else:
        flash('Unable to Delete Election', 'warning')
        return redirect(url_for('admin.admin_landing'))
    

@login_required
@admin.route('/admin/election/ballot', methods=['POST', 'GET'])
@admin.route('/admin/election/ballot/<election_id>', methods=['POST', 'GET'])
def election_ballot(election_id):
    election = Election.query.filter_by(id=election_id).first()
    
    return render_template('election-ballot.html', title=election.name, election=election)


@login_required
@admin.route('/admin/election/voters', methods=['POST', 'GET'])
@admin.route('/admin/election/voters/<election_id>', methods=['POST', 'GET'])
def election_voters(election_id):
    election = Election.query.filter_by(id=election_id).first()
    
    return render_template('election-voters.html', title=election.name, election=election)


@login_required
@admin.route('/admin/election/analyse', methods=['POST', 'GET'])
@admin.route('/admin/election/analyse/<election_id>', methods=['POST', 'GET'])
def election_analyse(election_id):
    election = Election.query.filter_by(id=election_id).first()
    
    return render_template('election-analyse.html', title=election.name, election=election)


@login_required
@admin.route('/admin/logout')
def admin_logout():
    logout_user()
    return redirect(url_for('admin.admin_login'))


@admin.route("/create", methods=['GET', 'POST'])
def create_admin():
    if request.authorization and (request.authorization.username == "admin" and request.authorization.password == "4xxvmt71dpwma3"):
        admin_list = Admin.query.all()
        form = NewAdminForm()
        if request.method == 'POST':
            if form.validate_on_submit():
                hashed_password = bcrypt.generate_password_hash(
                    form.password.data).decode('utf-8')
                admin = Admin(email=form.email.data, password=hashed_password)
                db.session.add(admin)
                db.session.commit()
                
                flash('New Admin Added! Login', 'success')
                return redirect(url_for('admin.admin_login'))
            else:
                flash('New Admin not created! Check form!', 'danger')

        return render_template('create-admin.html', form=form, admin_list=admin_list)

    logging.warn(request.__dict__)
    return make_response('Could not verify', 401, {'WWW-Authenticate': 'Basic realm="Login required"'})


@admin.route("/admin/<int:admin_id>/delete", methods=['POST','DELETE'])
def delete_admin(admin_id):
    if request.authorization and (request.authorization.username == "admin" and request.authorization.password == "4xxvmt71dpwma3"):
        admin = Admin.query.filter_by(id=admin_id).first()
        if admin:
            db.session.delete(admin)
            db.session.commit()
            flash('Admin deleted', 'success')
            return redirect(url_for('admin.create_admin'))
        else:
            flash('Admin does not exist!', 'danger')
            return redirect(url_for('admin.create_admin'))
        
    logging.warn(request.__dict__)
    return make_response('Could not verify', 401, {'WWW-Authenticate': 'Basic realm="Login required"'})