from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Recipe, Ingredient, Comment


class RegisterForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']


class RecipeForm(forms.ModelForm):
    class Meta:
        model = Recipe
        fields = ['title', 'description']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Recipe title'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 8, 'placeholder': 'Describe the steps to complete this recipe...'}),
        }


class IngredientForm(forms.ModelForm):
    class Meta:
        model = Ingredient
        fields = ['name', 'quantity']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ingredient name'}),
            'quantity': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g. 2 cups'}),
        }


IngredientFormSet = forms.inlineformset_factory(
    Recipe, Ingredient,
    form=IngredientForm,
    extra=3,
    can_delete=True,
    min_num=1,
    validate_min=True,
)


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['content']
        widgets = {
            'content': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Add a comment...'}),
        }
        labels = {'content': ''}
