#coding:utf-8
from django import forms
from django.contrib.auth.models import User
from vod.models import Review, ResponseReview

from django import forms
from django.template.defaultfilters import filesizeformat
from django.utils.translation import ugettext_lazy as _
from django.conf import settings

# Limit uploads to 100MB
MAX_UPLOAD_SIZE = 104857600


class ReviewForm(forms.ModelForm):
  text = forms.CharField(widget=forms.Textarea(attrs={'placeholder': '留言'}))

  class Meta:
    model = Review
    fields = ['text']


class RestrictedFileField(forms.FileField):
    def __init__(self, *args, **kwargs):
        self.content_types = kwargs.pop('content_types', None)
        self.max_upload_size = kwargs.pop('max_upload_size', None)
        if not self.max_upload_size:
            self.max_upload_size = MAX_UPLOAD_SIZE
        super(RestrictedFileField, self).__init__(*args, **kwargs)

    def clean(self, *args, **kwargs):
        data = super(RestrictedFileField, self).clean(*args, **kwargs)
        try:
            content_category = data.content_type.split("/")[0]
            print data.content_type
            if content_category in self.content_types:
                if data.size > self.max_upload_size:
                    raise forms.ValidationError(_('File size must be under %s. Current file size is %s.') % (filesizeformat(self.max_upload_size), filesizeformat(data.size)))
            else:
                raise forms.ValidationError(_('File type (%s) is not supported.') % data.content_type)
        except AttributeError:
            pass

        return data

class RestrictedImageField(forms.ImageField):
    def __init__(self, *args, **kwargs):
        self.max_upload_size = kwargs.pop('max_upload_size', None)
        if not self.max_upload_size:
            self.max_upload_size = MAX_UPLOAD_SIZE
        super(RestrictedImageField, self).__init__(*args, **kwargs)

    def clean(self, *args, **kwargs):
        data = super(RestrictedImageField, self).clean(*args, **kwargs)
        try:
            if data.size > self.max_upload_size:
                raise forms.ValidationError(_('File size must be under %s. Current file size is %s.') % (filesizeformat(self.max_upload_size), filesizeformat(data.size)))
        except AttributeError:
            pass

        return data

class UploadFileForm(forms.Form):
    title = forms.CharField(max_length=50)
    description = forms.CharField(widget=forms.Textarea(attrs={'placeholder': '影片描述'}))
    #file = forms.FileField()
    file = RestrictedFileField(content_types=['video'])

