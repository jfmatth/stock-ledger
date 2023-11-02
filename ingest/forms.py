from django.forms import ModelForm

class PartialAuthorForm(ModelForm):
    class Meta:
        model = ingest
