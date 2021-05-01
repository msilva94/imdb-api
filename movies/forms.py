from django import forms


class ImportMovieForm(forms.Form):
    external_id = forms.CharField(label='IMDb ID')
