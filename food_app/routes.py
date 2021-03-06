from flask import render_template, flash, redirect, url_for, request
from flask_login import current_user, login_user, logout_user, login_required
from werkzeug.urls import url_parse

from food_app.forms import LoginForm, RegistrationForm, AddProductForm, AddRecipeForm, NewShoppingListForm, \
    AddPortionsForm, AddProductToListForm, SelectProductToAddForm, AskDeleteShoppingListForm, ChangeQuantityItemForm, \
    AddProductToRecipeForm, ChangeQuantityIngredientForm, AskDeleteRecipeForm, EditDescriptionForm, AddNotesToListForm
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
        # flash('Congratulations, you are now a registered user!')
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
    products = Product.query.order_by(Product.title)  # by ABC order
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
        # flash('New product has been successfully added!')
        return redirect(url_for('product'))
    return render_template('add_product.html', title='Add Product', form=form)


@app.route('/recipe')
@login_required
def recipe():
    return render_template("recipe.html", title='Recipe')


@app.route('/my_recipes', methods=['GET', 'POST'])
@login_required
def my_recipes():
    owner = current_user.id
    my_recipes = Recipe.query.filter_by(owner=owner)
    return render_template(
        'my_recipes.html',
        title='My Recipes',
        owner=owner,
        my_recipes=my_recipes,
    )


@app.route('/all_recipes', methods=['GET', 'POST'])
@login_required
def all_recipes():
    recipes = Recipe.query.all()
    return render_template(
        'all_recipes.html',
        title='All Recipes',
        recipes=recipes,
    )


@app.route('/add_recipe', methods=['GET', 'POST'])
@login_required
def add_recipe():
    form = AddRecipeForm()
    if request.method == 'GET':
        return render_template("add_recipe.html", title='Recipe', form=form)
    if form.validate_on_submit():
        recipe = Recipe(title=form.title.data, owner=current_user.id, description=form.description.data)
        db.session.add(recipe)
        db.session.commit()
        # flash('New recipe has been successfully added!')
        return redirect(url_for('recipe'))
    return render_template('add_recipe.html', title='Recipe', form=form)


@app.route('/delete_recipe/<recipe_id>', methods=['GET', 'POST'])
@login_required
def delete_recipe(recipe_id):
    current_recipe = Recipe.query.filter_by(id=recipe_id).first()
    form = AskDeleteRecipeForm()
    owner = current_user.id
    recipes = Recipe.query.filter_by(owner=owner)

    if request.method == 'GET':
        return render_template("delete_recipe.html", title='Do you want to delete?', current_recipe=current_recipe,
                               form=form)
    if form.validate_on_submit():
        if form.ask.data == 'yes':
            # for item in shopping_list.items:
            filtered_ingredients = list(filter(
            lambda ingredient: current_recipe.id == ingredient.recipe_id,
            current_recipe.ingredients
        ))
            if filtered_ingredients:
                ingredient = filtered_ingredients[0]
                db.session.delete(ingredient)
            db.session.delete(current_recipe)
        db.session.commit()
        return redirect(url_for('my_recipes'))
    else:
        return redirect(url_for('my_recipes'))


@app.route('/add_product_to_recipe/<product_id>', methods=['GET', 'POST'])
@login_required
def add_product_to_recipe(product_id):
    owner = current_user.id
    form = AddProductToRecipeForm()
    current_product = Product.query.filter_by(id=product_id).first()
    current_recipe = form.recipe.data

    if request.method == 'GET':
        return render_template("add_product_to_recipe.html", title='Add Product to Recipe',
                               current_product=current_product, owner=owner, form=form)
    if form.validate_on_submit():
        ingredient = Ingredient(
            recipe_id=current_recipe.id,
            product_id=product_id,
            product=current_product,
            quantity=form.quantity.data,
            unit_of_measure=current_product.unit_of_measure,
        )
        db.session.add(ingredient)
        db.session.commit()
        # flash('New ingredient has been successfully added!')
        return redirect(url_for('all_products'))


@app.route('/all_lists', methods=['GET', 'POST'])
@login_required
def all_lists():
    owner = current_user.id
    shopping_lists = ShoppingList.query.filter_by(owner=owner)
    return render_template('all_lists.html', title='All Shopping Lists', owner=owner, shopping_lists=shopping_lists)


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
        # flash('New shopping list has been successfully created!')
        return redirect(url_for('all_lists'))
    return render_template('new_list.html', title='ShoppingList', form=form)


@app.route('/edit_recipe/<recipe_id>', methods=['GET', 'POST'])
@login_required
def edit_recipe(recipe_id):
    recipe = Recipe.query.filter_by(id=recipe_id).first()
    description = recipe.description
    return render_template('edit_recipe.html', recipe=recipe, description=description)


@app.route('/edit_recipe_description/<recipe_id>/<recipe_description>', methods=['GET', 'POST'])
@login_required
def edit_recipe_description(recipe_id, recipe_description):
    recipe = Recipe.query.filter_by(id=recipe_id).first()
    description = Recipe.query.filter_by(description=recipe_description).first()
    form = EditDescriptionForm()
    if request.method == 'GET':
        return render_template("edit_recipe_description.html", title='Do you want to edit description?', recipe=recipe, description=description,
                               form=form)
    if form.validate_on_submit():
        recipe.description = form.description.data
        db.session.commit()
        return redirect(url_for('edit_recipe', recipe_id=recipe_id, recipe_description=recipe_description))


@app.route('/add_notes_to_list/<shopping_list_id>/<shopping_list_notes>', methods=['GET', 'POST'])
@login_required
def add_notes_to_list(shopping_list_id, shopping_list_notes):
    shopping_list = ShoppingList.query.filter_by(id=shopping_list_id).first()
    notes = ShoppingList.query.filter_by(notes=shopping_list_notes).first()
    form = AddNotesToListForm()
    if request.method == 'GET':
        return render_template("add_notes_to_list.html", title='Do you want to add notes?', shopping_list=shopping_list, notes=notes,
                               form=form)
    if form.validate_on_submit():
        shopping_list.notes = form.notes.data
        db.session.commit()
        return redirect(url_for('edit_shopping_list', shopping_list_id=shopping_list_id, shopping_list_notes=shopping_list_notes))


@app.route('/edit_shopping_list/<shopping_list_id>', methods=['GET', 'POST'])
@login_required
def edit_shopping_list(shopping_list_id):
    shopping_list = ShoppingList.query.filter_by(id=shopping_list_id).first()
    return render_template('edit_shopping_list.html', shopping_list=shopping_list)


@app.route('/change_quantity_ingredient/<recipe_id>/<ingredient_id>', methods=['GET', 'POST'])
@login_required
def change_quantity_ingredient(recipe_id, ingredient_id):
    ingredient = Ingredient.query.filter_by(id=ingredient_id).first()
    form = ChangeQuantityIngredientForm()
    if request.method == 'GET':
        return render_template("change_quantity_ingredient.html", title='Do you want to change quantity?', ingredient=ingredient,
                               form=form)
    if form.validate_on_submit():
        ingredient.quantity = form.quantity.data
        db.session.commit()
        return redirect(url_for('edit_recipe', recipe_id=recipe_id))


@app.route('/change_quantity_item/<shopping_list_id>/<item_id>', methods=['GET', 'POST'])
@login_required
def change_quantity_item(shopping_list_id, item_id):
    item = ShoppingListItem.query.filter_by(id=item_id).first()
    form = ChangeQuantityItemForm()
    if request.method == 'GET':
        return render_template("change_quantity_item.html", title='Do you want to change quantity?', item=item,
                               form=form)
    if form.validate_on_submit():
        item.quantity = form.quantity.data
        db.session.commit()
        return redirect(url_for('edit_shopping_list', shopping_list_id=shopping_list_id))


@app.route('/delete_recipe_ingredient/<recipe_id>/<ingredient_id>', methods=['GET', 'POST'])
@login_required
def delete_recipe_ingredient(recipe_id, ingredient_id):
    ingredient = Ingredient.query.filter_by(id=ingredient_id).first()
    form = AskDeleteRecipeForm()
    if request.method == 'GET':
        return render_template("delete_recipe_ingredient.html", title='Do you want to delete?', ingredient=ingredient, form=form)
    if form.validate_on_submit():
        if form.ask.data == 'yes':
            db.session.delete(ingredient)
            db.session.commit()
            return redirect(url_for('edit_recipe', recipe_id= recipe_id))
        else:
            return redirect(url_for('edit_recipe', recipe_id= recipe_id))


@app.route('/delete_list_item/<shopping_list_id>/<item_id>', methods=['GET', 'POST'])
@login_required
def delete_shopping_list_item(shopping_list_id, item_id):
    item = ShoppingListItem.query.filter_by(id=item_id).first()
    form = AskDeleteShoppingListForm()
    if request.method == 'GET':
        return render_template("delete_list_item.html", title='Do you want to delete?', item=item, form=form)
    if form.validate_on_submit():
        if form.ask.data == 'yes':
            db.session.delete(item)
            db.session.commit()
            return redirect(url_for('edit_shopping_list', shopping_list_id=shopping_list_id))
        else:
            return redirect(url_for('edit_shopping_list', shopping_list_id=shopping_list_id))


@app.route('/delete_shopping_list/<shopping_list_id>', methods=['GET', 'POST'])
@login_required
def delete_shopping_list(shopping_list_id):
    shopping_list = ShoppingList.query.filter_by(id=shopping_list_id).first()
    form = AskDeleteShoppingListForm()
    owner = current_user.id
    shopping_lists = ShoppingList.query.filter_by(owner=owner)

    if request.method == 'GET':
        return render_template("delete_shopping_list.html", title='Do you want to delete?', shopping_list=shopping_list,
                               form=form)
    if form.validate_on_submit():
        if form.ask.data == 'yes':
            # for item in shopping_list.items:
            filtered_items = list(filter(
            lambda item: shopping_list.id == item.shopping_list_id,
            shopping_list.items))
            if filtered_items:
                item = filtered_items[0]
                db.session.delete(item)
            db.session.delete(shopping_list)
        db.session.commit()
        return render_template('all_lists.html', title='All Shopping Lists', shopping_lists=shopping_lists)
    else:
        return render_template('all_lists.html', title='All Shopping Lists', shopping_lists=shopping_lists)


@app.route('/shopping_list', methods=['GET', 'POST'])
@login_required
def shopping_list():
    form = SelectProductToAddForm()
    if request.method == 'GET':
        return render_template("shopping_list.html", title='Select Product', form=form)


@app.route('/add_product_to_shopping_list/<product_id>', methods=['GET', 'POST'])
@login_required
def add_product_to_list(product_id):
    current_product = Product.query.filter_by(id=product_id).first()
    form = AddProductToListForm()

    if not form.validate_on_submit():
        return render_template(
            "add_product_to_list.html", title='Shopping List', current_product=current_product, form=form
        )

    shopping_list: ShoppingList = form.shopping_list.data

    filtered_items = list(filter(lambda item: item.product.id == current_product.id, shopping_list.items))
    if filtered_items:
               item = filtered_items[0]
    else:
        # Create new ShoppingListItem.
        #   Then, add it to ShoppingList. Add to field, which related by ForeignKey. We can add item as to list.
        item = ShoppingListItem(product_id=current_product.id, unit_of_measure=current_product.unit_of_measure,
                                quantity=0)
        shopping_list.items.append(item)

    item.quantity += form.quantity.data
    db.session.commit()

    # flash('Item have been successfully added!')

    return redirect(url_for('all_lists'))


@app.route('/add_recipe_to_shopping_list/<recipe_id>', methods=['GET', 'POST'])
@login_required
def add_portions(recipe_id):
    current_recipe = Recipe.query.filter_by(id=recipe_id).first()
    form = AddPortionsForm()

    if not form.validate_on_submit():
        return render_template(
            "add_portions.html", title='Shopping List', current_recipe=current_recipe, form=form)

    shopping_list = form.title_list.data

    for ingredient in current_recipe.ingredients:

        if ingredient is None:
            return render_template(
                "add_portions.html", title='Shopping List', current_recipe=current_recipe, form=form)

        else:
            filtered_items = list(filter(
                lambda item: ingredient.product_id == item.product_id,
                shopping_list.items
            ))

            if filtered_items:
                item = filtered_items[0]
            else:
                item = ShoppingListItem(product_id=ingredient.product_id,
                                        unit_of_measure=ingredient.unit_of_measure,
                                        quantity=0)
                shopping_list.items.append(item)

            item.quantity += ingredient.quantity * int(form.number_of_portions.data)

            db.session.commit()
    return redirect(url_for('all_lists'))












# def show_user(username):
#     user = User.query.filter_by(username=username).first_or_404()
#     return render_template('show_user.html', user=user)
