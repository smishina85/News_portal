# D4.3
from importlib.resources import _

from django import forms
from django.core.exceptions import ValidationError
from django.forms import Textarea, ModelMultipleChoiceField

from .models import Post, Category


class PostForm(forms.ModelForm):
    title = forms.CharField(label= 'Заголовок', min_length=4)
    post = ModelMultipleChoiceField(label='Категория', queryset=Category.objects.all())

    class Meta:
        model = Post
        fields = [
            'author',
            'charact',
            'title',
            'text',
            'post',
        ]
        labels = {'text': _('Ваш Текст'),}
        widgets={'title': Textarea(attrs={'cols': 128, 'rows': 2}), 'text': Textarea(attrs={'cols': 80, 'row': 10}),
                 'post': Textarea(attrs={'cols': 50}),}

    def clean(self):
        cleaned_data = super().clean()
        title = cleaned_data.get("title")

        if title is not None and len(title) < 4:
            raise ValidationError({
                 "title": "Заголовок не может быть менее 4 смволов"
            })
        return cleaned_data
    #
    def clean_title(self):
        title = self.cleaned_data["title"]
        if title[0].islower():
            raise ValidationError("Заголовок должен начинаться с заглавной буквы")
        return title

