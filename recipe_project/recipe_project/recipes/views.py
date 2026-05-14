from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages
from django.db import transaction
from .models import Recipe, Comment
from .forms import RegisterForm, RecipeForm, IngredientFormSet, CommentForm


def recipe_list(request):
    recipes = Recipe.objects.select_related('author').all()
    return render(request, 'recipes/recipe_list.html', {'recipes': recipes})


def recipe_detail(request, pk):
    recipe = get_object_or_404(Recipe.objects.select_related('author').prefetch_related('ingredients', 'comments__author'), pk=pk)
    comment_form = CommentForm()

    if request.method == 'POST':
        if not request.user.is_authenticated:
            messages.error(request, 'You must be logged in to comment.')
            return redirect('login')
        comment_form = CommentForm(request.POST)
        if comment_form.is_valid():
            comment = comment_form.save(commit=False)
            comment.recipe = recipe
            comment.author = request.user
            comment.save()
            messages.success(request, 'Comment added!')
            return redirect('recipe_detail', pk=pk)

    return render(request, 'recipes/recipe_detail.html', {
        'recipe': recipe,
        'comment_form': comment_form,
    })


@login_required
def recipe_create(request):
    if request.method == 'POST':
        form = RecipeForm(request.POST)
        formset = IngredientFormSet(request.POST)
        if form.is_valid() and formset.is_valid():
            with transaction.atomic():
                recipe = form.save(commit=False)
                recipe.author = request.user
                recipe.save()
                formset.instance = recipe
                formset.save()
            messages.success(request, 'Recipe created successfully!')
            return redirect('recipe_detail', pk=recipe.pk)
    else:
        form = RecipeForm()
        formset = IngredientFormSet()
    return render(request, 'recipes/recipe_form.html', {'form': form, 'formset': formset, 'action': 'Create'})


@login_required
def recipe_edit(request, pk):
    recipe = get_object_or_404(Recipe, pk=pk, author=request.user)
    if request.method == 'POST':
        form = RecipeForm(request.POST, instance=recipe)
        formset = IngredientFormSet(request.POST, instance=recipe)
        if form.is_valid() and formset.is_valid():
            with transaction.atomic():
                form.save()
                formset.save()
            messages.success(request, 'Recipe updated!')
            return redirect('recipe_detail', pk=recipe.pk)
    else:
        form = RecipeForm(instance=recipe)
        formset = IngredientFormSet(instance=recipe)
    return render(request, 'recipes/recipe_form.html', {'form': form, 'formset': formset, 'action': 'Edit', 'recipe': recipe})


@login_required
def recipe_delete(request, pk):
    recipe = get_object_or_404(Recipe, pk=pk, author=request.user)
    if request.method == 'POST':
        recipe.delete()
        messages.success(request, 'Recipe deleted.')
        return redirect('recipe_list')
    return render(request, 'recipes/recipe_confirm_delete.html', {'recipe': recipe})


@login_required
def my_recipes(request):
    recipes = Recipe.objects.filter(author=request.user)
    return render(request, 'recipes/my_recipes.html', {'recipes': recipes})


def register_view(request):
    if request.user.is_authenticated:
        return redirect('recipe_list')
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, f'Welcome, {user.username}! Your account was created.')
            return redirect('recipe_list')
    else:
        form = RegisterForm()
    return render(request, 'recipes/register.html', {'form': form})


def login_view(request):
    if request.user.is_authenticated:
        return redirect('recipe_list')
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            messages.success(request, f'Welcome back, {user.username}!')
            return redirect(request.GET.get('next', 'recipe_list'))
    else:
        form = AuthenticationForm()
    return render(request, 'recipes/login.html', {'form': form})


def logout_view(request):
    logout(request)
    messages.info(request, 'You have been logged out.')
    return redirect('recipe_list')
