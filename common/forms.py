class StyleFormMixin:
    """Миксин для добавления Bootstrap-классов к полям формы."""
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs.update({'class': 'form-control', 'placeholder': field.label})