from django import forms
from blog.models import Blog, References
from communities.models import Communities
from django.forms import modelformset_factory
from dal import autocomplete
from account.models import Account
from django import forms
from blog.validators import image_validator
# from django_select2.forms import ModelSelect2MultipleWidget

IMAGE_SIZE_MAX_BYTES = 1024 * 1024 * 3
MIN_TITLE_LENGTH = 5
MIN_BODY_LENGTH = 50


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

    def clean_image(self):
        image = self.cleaned_data['image']
        image_validator(image)
        return image

    def clean_body(self):
        body = self.cleaned_data['body']
        if len(body) < MIN_BODY_LENGTH:
            raise forms.ValidationError("Enter a body longer than " + str(MIN_BODY_LENGTH) + " characters.")
        return body

    def clean_title(self):
        title = self.cleaned_data['title']
        if len(title) < MIN_TITLE_LENGTH:
            raise forms.ValidationError("Enter a title longer than " + str(MIN_TITLE_LENGTH) + " characters.")
        return title


class ReferencesForm(forms.ModelForm):
    class Meta:
        model = References
        fields = "__all__"


class CommunityForm(forms.ModelForm):
    class Meta:
        model = Communities
        fields = ['name', 'description', 'backgroundimage', 'avatarimage']

    def clean_avatarimage(self):
        image = self.cleaned_data['avatarimage']
        image_validator(image)
        return image

    def clean_backgroundimage(self):
        image = self.cleaned_data['backgroundimage']
        image_validator(image)
        return image


class UserForm(forms.ModelForm):
    class Meta:
        model = Account
        fields = ['mobile_number']
        widgets = {
            'mobile_number': autocomplete.Select2(url="personal:users_autocomplete",
                                                  attrs={
                                                      'data-minimum-input-length': 5,
                                                  }
                                                  ),

            # 'first_name': autocomplete.Select2(url="personal:users_autocomplete")
        }

    def save(self, commit=True):
        super().save(commit)


class ImageSearchForm(forms.Form):
    image = forms.ImageField()


class StaffCreateForm(forms.ModelForm):
    class Meta:
        model = Account
        exclude = ["is_admin", "is_superuser"]


class StaffRemoveForm(forms.ModelForm):
    first_name = forms.CharField(required=False)
    last_name = forms.CharField(required=False)
    mobile_number = forms.CharField(required=False)

    class Meta:
        model = Account
        fields = ['first_name', 'last_name', 'mobile_number']
        # widgets = {
        #     'mobile_number': autocomplete.Select2(url="personal:staff_autocomplete_mobile",
        #                                           # attrs={
        #                                           #     'data-minimum-input-length': 5,
        #                                           # },
        #                                           ),
        #
        #     'first_name': autocomplete.Select2(url="personal:staff_autocomplete_fname",
        #                                        # attrs={
        #                                        #     'data-minimum-input-length': 5,
        #                                        #  }
        #                                        ),
        #     'last_name': autocomplete.Select2(url="personal:staff_autocomplete_lname",
        #                                       # attrs={
        #                                       #     'data-minimum-input-length': 5,
        #                                       #   }
        #                                       )
        # }


ReferencesModelFormset = modelformset_factory(
    References,
    fields="__all__",
    extra=0,
    max_num=10,
    min_num=1,
)
