from flask import Flask, render_template, request, flash, redirect, Response
from flask_bootstrap import Bootstrap
from flask_appconfig import AppConfig
from forms import AddForm, RegisterForm, RegisterFormVerify
from data import Data


configfile = None
app = Flask(__name__)
AppConfig(app, configfile)  # Flask-Appconfig is not necessary, but
                            # highly recommend =)
                            # https://github.com/mbr/flask-appconfig
Bootstrap(app)

app.config['SECRET_KEY'] = 'devkey'
app.config['RECAPTCHA_PUBLIC_KEY'] = None


def populate_list(total):
    mylist = []
    counter = 0
    while counter <= total:
        mylist.append((counter, str(counter)))
        counter += 1
    return mylist


def is_valid(invitecode, lastname):
    user = Data()
    lookup = user.getvalue(invitecode)

    # if invitation code does not exist
    if not lookup:
        return False

    if lastname.lower().strip() == lookup['lastname'].lower():
        return True
    else:
        return False


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/report')
def viewreport():
    def report():
        data = Data()
        total = 0
        codes = sorted(data.getallkeys())
        for code in codes:
            invite = data.getvalue(code)
            if 'actual_guests' in invite:
                yield '%s: %s %s '\
                      'attending: %s '\
                      'guests: %s\n' % (code,
                                        invite['firstname'],
                                        invite['lastname'],
                                        invite['attending'],
                                        invite['actual_guests'])
                total += int(invite['actual_guests'])
        yield 'total: %s\n' % total
    return Response(report(),  mimetype='text/plain')


@app.route('/add', methods=['GET', 'POST'])
def add():
    form = AddForm(csrf_enabled=False)
    if request.method == 'POST' and form.validate_on_submit():
        user = Data()
        print form.data
        code = user.add(form.data['firstname'], form.data['lastname'],
                        form.data['number'],
                        middlename=form.data['middlename'])

        return render_template('add.done.html', code=code, data=form.data)
    else:
        return render_template('add.html', form=form)


@app.route('/register/<invitecode>', methods=['GET', 'POST'])
def register_invitecode(invitecode=None):
    user = Data()
    form = RegisterFormVerify(csrf_enabled=False)
    lookup = user.getvalue(invitecode)

    if request.method == 'GET' and lookup['attending'] == 'None':
        form.guests.choices = populate_list(int(lookup['guests']))
        return render_template('register_invitecode.html', lookup=lookup,
                               form=form)

    elif request.method == 'POST':
        if form.data['attending'] == 'False':
            actual_guests = '0'
        else:
            actual_guests = form.data['guests']

        user.update(invitecode, form.data['attending'],
                    actual_guests)

        lookup = user.getvalue(invitecode)
        return render_template('register_done.html', lookup=lookup)

    else:
        return render_template('register_invitecode.html', lookup=lookup,
                               form=form)


@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm(csrf_enabled=False)
    print request.form
    if request.method == 'POST' and form.validate_on_submit():
        invitecode = form.data['invitecode']
        if is_valid(invitecode, form.data['lastname']):
            return redirect('/register/%s' % invitecode)
        else:
        # we can't find you, prompt to try again.
            return render_template('register.html', form=form, found=False)
    else:
        return render_template('register.html', form=form)

if __name__ == '__main__':
        app.run()
