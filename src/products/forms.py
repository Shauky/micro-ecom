from django import forms
from django.forms import modelformset_factory, inlineformset_factory
from .models import Product, ProductAttachment


# look into input css classes, adding tailwind classes into django templates
# right now this class is loaded into tailwind, letting it call back to review
# any css class changes inside form control. The orginal settins for this are inside tailwind-input css 
# class and watched with rav watch

input_css_class = "form-control"

class ProductForm(forms.ModelForm):
    # name = forms.CharField(widget=forms.TextInput(attrs={"class":"form-control"}))

    class Meta:
        model = Product
        fields = ['name', 'handle', 'price', 'description']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # change the variables for any given html attributes
        for field in self.fields:
            self.fields[field].widget.attrs['class'] =  input_css_class

class ProductUpdateForm(forms.ModelForm):
    # name = forms.CharField(widget=forms.TextInput(attrs={"class":"form-control"}))

    class Meta:
        model = Product
        fields = ['image','name', 'handle', 'price', 'description']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # change the variables for any given html attributes
        for field in self.fields:
            self.fields[field].widget.attrs['class'] =  input_css_class


class ProductAttachmentForm(forms.ModelForm):
    # name = forms.CharField(widget=forms.TextInput(attrs={"class":"form-control"}))

    class Meta:
        model = ProductAttachment
        fields = ['file','name', 'is_downloadable', 'active']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # change the variables for any given html attributes
        for field in self.fields:
            if field in ['is_downloadable', 'active']:
                continue
            self.fields[field].widget.attrs['class'] =  input_css_class


ProductAttachmentModelFormset = modelformset_factory(
    ProductAttachment,
    form = ProductAttachmentForm,
    fields = ['file', 'name', 'is_downloadable', 'active'],
    extra=0,
    can_delete=False
)

ProductAttachmentInlineFormset = inlineformset_factory(
    Product,
    ProductAttachment,
    form = ProductAttachmentForm, 
    formset = ProductAttachmentModelFormset,
    fields = ['file', 'name', 'is_downloadable', 'active'],
    extra=0,
    can_delete=False
)