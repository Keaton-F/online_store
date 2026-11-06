from django import forms
from django.core.exceptions import ValidationError
from .models import Product

FORBIDDEN_WORDS = [
    'казино', 'криптовалюта', 'крипта', 'биржа',
    'дешево', 'бесплатно', 'обман', 'полиция', 'радар'
]


class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['name', 'description', 'image', 'category', 'price']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            if isinstance(field.widget, forms.CheckboxInput):
                field.widget.attrs.update({'class': 'form-check-input'})
            else:
                field.widget.attrs.update({'class': 'form-control'})

    def clean_price(self):
        price = self.cleaned_data.get('price')

        if price is not None and price < 0:
            raise ValidationError(
                "Ошибка заполнения формы: Цена продукта не может быть отрицательной. "
                "Пожалуйста, укажите корректную стоимость товара (0 или выше)."
            )

        return price

    def clean(self):
        cleaned_data = super().clean()

        name = cleaned_data.get('name', '')
        description = cleaned_data.get('description', '')

        name_lower = name.lower() if name else ''
        description_lower = description.lower() if description else ''

        for word in FORBIDDEN_WORDS:
            if word in name_lower:
                raise ValidationError(
                    f"Недопустимое название товара. Слово '{word}' запрещено к использованию на нашей платформе."
                )
            if word in description_lower:
                raise ValidationError(
                    f"Недопустимое описание товара. Слово '{word}' запрещено к использованию на нашей платформе."
                )

        return cleaned_data
