from django import forms

class NameForm(forms.Form):

    food_item1 = forms.CharField(label='Item 1:')
    food_item2 = forms.CharField(label='Item 2:')
    food_item3 = forms.CharField(label='Item 3:')
    #food_item4 = forms.CharField(label='4.')
    place = forms.CharField(label='Place:')