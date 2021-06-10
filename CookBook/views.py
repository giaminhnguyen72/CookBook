from flask import Blueprint
from flask import render_template
from flask import request, redirect
from .model.Recipe import Recipe
from flask_login import current_user, login_required
from .app import db
import json
from werkzeug.exceptions import abort
views = Blueprint('views', __name__)

@views.route('/')
def home():
    return render_template("index.html")

@views.route('/dashboard')
@login_required
def dashboard():
    return render_template("dashboard.html", user=current_user)
@views.route('/dashboard/<int:id>')
@login_required
def dashboardView(id):
    recipe = Recipe.query.get_or_404(id)
    return render_template("view.html", user=current_user, recipe=recipe)
@views.route('/dashboard/create', methods=['GET', 'POST'])
@login_required
def create():
    if request.method == 'POST':
        recipeName = request.form.get("recipeName")
        unitSelect = request.form['unit']
        unit = ""
        print(unitSelect)
        if int(unitSelect) == 1:
            unit = " secs"
        elif int(unitSelect) == 2:
            unit = " mins"
        else:
            unit = " hrs"

        cookingTime = request.form.get("cookingTime") + unit
    
        ingredients = request.form.get("ingredient")
        description = request.form.get("description")
        direction = request.form.get("direction")
        newRecipe = Recipe(name=recipeName, cookingTime=cookingTime, ingredient=ingredients, description=description, directions=direction, user_id=current_user.id)
        db.session.add(newRecipe)
        db.session.commit()
        return render_template("dashboard.html", user=current_user)
    else:
        return render_template("create.html", user=current_user)
#@views.route('/login')
#def login():
#    return render_template("login.html")
#@views.route('/signup')

@views.route('/delete/<int:id>', methods=['GET', 'POST'])
@login_required
def deleteRecipe(id):
    recipe = Recipe.query.get_or_404(id)
    try:
        db.session.delete(recipe)
        db.session.commit()
        return redirect('/dashboard')
    except:
        return 'error occurred'

@views.route('/dashboard/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def edit(id):
    recipe = Recipe.query.get_or_404(id)
    if request.method == "POST":
        recipeName = request.form.get("recipeName")
        unitSelect = request.form['unit']
        unit = ""
        print(unitSelect)
        if int(unitSelect) == 1:
            unit = " secs"
        elif int(unitSelect) == 2:
            unit = " mins"
        else:
            unit = " hrs"

        cookingTime = request.form.get("cookingTime") + unit
    
        ingredients = request.form.get("ingredient")
        description = request.form.get("description")
        direction = request.form.get("direction")
        recipe.recipeName = recipeName
        recipe.ingredient = ingredients
        recipe.cookingTime = cookingTime
        recipe.description = description
        recipe.directions = direction
        db.session.commit()
        return render_template('dashboard.html', user=current_user)
    return render_template('edit.html', user=current_user, recipe=recipe)
    
        



