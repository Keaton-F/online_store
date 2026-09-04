from django import forms

from .models import BlogPost


class BlogPostForm(forms.ModelForm):
    class Meta:
        model = BlogPost
        fields = [
            "title",
            "content",
            "preview",
            "is_published",
        ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields["title"].widget.attrs.update(
            {"class": "form-control"}
        )
        self.fields["content"].widget.attrs.update(
            {"class": "form-control", "rows": 8}
        )
        self.fields["preview"].widget.attrs.update(
            {"class": "form-control"}
        )
        self.fields["is_published"].widget.attrs.update(
            {"class": "form-check-input"}
        )
