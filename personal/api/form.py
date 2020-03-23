from django import forms
from blog.models import Blog, References
from communities.models import Communities
from django.forms import modelformset_factory
from dal import autocomplete
from account.models import Account
from django import forms
# from django_select2.forms import ModelSelect2MultipleWidget


class BlogForm(forms.ModelForm):

    class Meta:
        model = Blog
        fields = ['title', 'references', 'description', 'body', 'image', 'community']
        widgets = {
            'references': autocomplete.ModelSelect2Multiple(url="personal:references_autocomplete",
                                                            attrs={
                                                                'data-minimum-input-length': 3,
                                                            }),
        }


class ReferencesForm(forms.ModelForm):
    class Meta:
        model = References
        fields = "__all__"


class CommunityForm(forms.ModelForm):
    class Meta:
        model = Communities
        fields = ['name', 'description', 'backgroundimage', 'avatarimage']


class UserForm(forms.ModelForm):
    class Meta:
        model = Account
        fields = ['mobile_number']
        widgets = {
            'mobile_number': autocomplete.Select2(url="personal:users_autocomplete",
                                                  attrs={
                                                      'data-minimum-input-length': 3,
                                                  }
                                                  ),

            # 'first_name': autocomplete.Select2(url="personal:users_autocomplete")
        }

    def save(self, commit=True):

        super().save(commit)


class ImageSearchForm(forms.Form):
    image = forms.ImageField()


ReferencesModelFormset = modelformset_factory(
    References,
    fields="__all__",
    extra=0,
    max_num=10,
    min_num=1,
)
