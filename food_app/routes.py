from flask import render_template, flash, redirect, url_for, request, render_template_string
from flask_login import current_user, login_user, logout_user, login_required
from werkzeug.urls import url_parse

from food_app.forms import LoginForm, RegistrationForm, AddProductForm, AddRecipeForm, NewShoppingListForm, \
    AddPortionsForm, AddProductToListForm, SelectProductToAddForm
from food_app.models import User, Product, Recipe, ShoppingList, Ingredient, ShoppingListItem
from .app_factory import app, db


@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Congratulations, you are now a registered user!')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)


@app.route('/')
@app.route('/index')
@login_required
def index():
    user = {'username': 'Bob'}  # is it necessary?
    posts = [
        {
            'author': {'username': 'John'},
            'body': 'Beautiful day in Portland!'
        },
        {
            'author': {'username': 'Susan'},
            'body': 'The Avengers movie was so cool!'
        }
    ]
    return render_template("index.html", title='Home Page', posts=posts)


@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('login'))
        login_user(user, remember=form.remember_me.data)
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('index')
        return redirect(next_page)
    return render_template('login.html', title='Sign In', form=form)


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))


@app.route('/product')
@login_required
def product():
    return render_template("product.html", title='Product')


@app.route('/all_products', methods=['GET', 'POST'])
@login_required
def all_products():
    products = Product.query.order_by(Product.title).all()  # by ABC order
    return render_template('all_products.html', title='All Products', products=products)


@app.route('/add_product', methods=['GET', 'POST'])
@login_required
def add_product():
    form = AddProductForm()
    if request.method == 'GET':
        return render_template("add_product.html", title='Add Product', form=form)
    if form.validate_on_submit():
        product = Product(title=form.title.data, type_of_product=form.type_of_product.data,
                          unit_of_measure=form.unit_of_measure.data)
        db.session.add(product)
        db.session.commit()
        flash('New product has been successfully added!!')
        return redirect(url_for('product'))
    return render_template('add_product.html', title='Add Product', form=form)


@app.route('/recipe')
@login_required
def recipe():
    return render_template("recipe.html", title='Recipe')


@app.route('/all_recipes', methods=['GET', 'POST'])
@login_required
def all_recipes():
    recipes = Recipe.query.all()
    # shopping_lists = ShoppingList.query.filter(ShoppingList.owner == current_user).all()
    return render_template(
        'all_recipes.html',
        title='All Recipes',
        recipes=recipes,
        # shopping_lists=shopping_lists
    )

@app.route('/add_recipe', methods=['GET', 'POST'])
@login_required
def add_recipe():
    form = AddRecipeForm()
    if request.method == 'GET':
        return render_template("add_recipe.html", title='Recipe', form=form)
    if form.validate_on_submit():
        recipe = Recipe(title=form.title.data, ingredients=form.ingredients.data, description=form.description.data)
        db.session.add(recipe)
        db.session.commit()
        flash('New recipe has been successfully added!')
        return redirect(url_for('recipe'))
    return render_template('add_recipe.html', title='Recipe', form=form)






@app.route('/all_lists', methods=['GET', 'POST'])
@login_required
def all_lists():
    owner = current_user.id
    shopping_lists = ShoppingList.query.filter_by(owner=owner).all()
    return render_template('all_lists.html', title='All Shopping Lists', owner=owner, shopping_lists=shopping_lists)
    # order_by(ShoppingList.owner).all() # by user


@app.route('/new_list', methods=['GET', 'POST'])
@login_required
def new_list():
    form = NewShoppingListForm()
    if request.method == 'GET':
        return render_template("new_list.html", title='Shopping List', form=form)
    if form.validate_on_submit():
        shopping_list = ShoppingList(title=form.title.data, owner=current_user.id, notes=form.notes.data)
        db.session.add(shopping_list)
        db.session.commit()
        flash('New shopping list has been successfully created!')
        return redirect(url_for('shopping_list'))
    return render_template('new_list.html', title='ShoppingList', form=form)


@app.route('/shopping_list', methods=['GET', 'POST'])
@login_required
def shopping_list():       # former def select_product_to_add()
    form = SelectProductToAddForm()
    if request.method == 'GET':
        return render_template("shopping_list.html", title='Select Product', form=form)


@app.route('/add_product_to_shopping_list/<id>', methods=['GET', 'POST'])
@login_required
def add_product_to_list(id):
    current_product = Product.query.filter_by(id=id).first()
    form = AddProductToListForm()
    if request.method == 'GET':
        return render_template("add_product_to_list.html", title='Shopping List', current_product=current_product, form=form)
    # if form.validate_on_submit():
    #     items = ShoppingList.query.filter_by(title=form.title_list.data.title).items
    #     # current_product = Product.query.filter_by(title=form.product.data.title).first().id
    #     # product = form.product.data
    #     if product in items:
    #         return redirect(url_for('shopping_list'))
    #     else:
    #         shopping_list_item = ShoppingListItem(
    #             shopping_list_id=form.title_list.data.id,
    #             product_id=Product.query.filter_by(title=product).first().id,
    #             product=form.product.data,    # Product.query.filter_by(product_id=current_product).first().product,
    #             quantity=form.quantity.data,
    #             unit_of_measure=form.unit_of_measure.data,
    #             is_buyed=False)
    #     db.session.add(shopping_list_item)
    #     db.session.commit()
    #     flash('New items have been successfully added!')
    #     return redirect(url_for('shopping_list'))





@app.route('/add_recipe_to_shopping_list/<recipe_id>', methods=['GET', 'POST'])
@login_required
def add_portions(recipe_id):
    current_recipe = Recipe.query.filter_by(id=recipe_id).first()
    form = AddPortionsForm()
    if request.method == 'GET':
        return render_template("add_portions.html", title='Shopping List', current_recipe=current_recipe, form=form)
    if form.validate_on_submit():
        # for shopping_list_item in form.title_list.data.items:
        shopping_list_item = ShoppingListItem(
            shopping_list_id=form.title_list.data.id,
            product_id=Ingredient.query.filter_by(recipe_id=recipe_id).first().product_id,
            product=Ingredient.query.filter_by(recipe_id=recipe_id).first().product,
            quantity=Ingredient.query.filter_by(recipe_id=recipe_id).first().quantity * int(form.number_of_portions.data),
            unit_of_measure=Ingredient.query.filter_by(recipe_id=recipe_id).first().unit_of_measure,
            is_buyed=False)
        db.session.add(shopping_list_item)
        db.session.commit()
        flash('New items have been successfully added!')
        items = ShoppingList.query.filter_by(title=form.title_list.data.title).first().items
        if product in items:
            return redirect(url_for('shopping_list'))
        else:
            shopping_list_item = ShoppingListItem(
                shopping_list_id=form.title_list.data.id,
                product_id=Ingredient.query.filter_by(recipe_id=recipe_id).first().product_id,
                product=Ingredient.query.filter_by(recipe_id=recipe_id).first().product,
                quantity=Ingredient.query.filter_by(recipe_id=recipe_id).first().quantity * int(
                    form.number_of_portions.data),
                unit_of_measure=Ingredient.query.filter_by(recipe_id=recipe_id).first().unit_of_measure,
                is_buyed=False)
            db.session.add(shopping_list_item)
            db.session.commit()
            return redirect(url_for('shopping_list'))


    # return render_template('add_portions.html', title=f'Shopping List', current_recipe=current_recipe, form=form)


# owner = current_user.id









# def show_user(username):
#     user = User.query.filter_by(username=username).first_or_404()
#     return render_template('show_user.html', user=user)
