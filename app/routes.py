from flask import render_template, request, redirect, url_for, flash, jsonify
from flask_login import login_user, logout_user, login_required, current_user
from . import app, db
from .models import User, Transaction
from .forms import LoginForm, SignupForm, TransactionForm

@app.route('/')
@login_required
def dashboard():
    # Fetch transactions for the current user
    transactions = Transaction.query.filter_by(user_id=current_user.id).all()

    # Calculate total amounts by category
    categories = {}
    for transaction in transactions:
        if transaction.category in categories:
            categories[transaction.category] += transaction.amount
        else:
            categories[transaction.category] = transaction.amount

    return render_template('dashboard.html', transactions=transactions, categories=jsonify(categories), amounts=jsonify(list(categories.values())))

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user and user.check_password(form.password.data):
            login_user(user)
            return redirect(url_for('dashboard'))
        flash('Invalid username or password.')
    return render_template('login.html', form=form)

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    form = SignupForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Account created successfully! Please log in.')
        return redirect(url_for('login'))
    return render_template('signup.html', form=form)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))

@app.route('/add_transaction', methods=['GET', 'POST'])
@login_required
def add_transaction():
    form = TransactionForm()
    if form.validate_on_submit():
        transaction = Transaction(
            amount=form.amount.data,
            category=form.category.data,
            date=form.date.data,
            description=form.description.data,
            user_id=current_user.id
        )
        db.session.add(transaction)
        db.session.commit()
        flash('Transaction added successfully!')
        return redirect(url_for('dashboard'))
    return render_template('add_transaction.html', form=form)

@app.route('/edit_transaction/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_transaction(id):
    transaction = Transaction.query.get_or_404(id)
    form = TransactionForm(obj=transaction)
    if form.validate_on_submit():
        transaction.amount = form.amount.data
        transaction.category = form.category.data
        transaction.date = form.date.data
        transaction.description = form.description.data
        db.session.commit()
        flash('Transaction updated successfully!')
        return redirect(url_for('dashboard'))
    return render_template('edit_transaction.html', form=form)

@app.route('/delete_transaction/<int:id>')
@login_required
def delete_transaction(id):
    transaction = Transaction.query.get_or_404(id)
    db.session.delete(transaction)
    db.session.commit()
    flash('Transaction deleted successfully!')
    return redirect(url_for('dashboard'))