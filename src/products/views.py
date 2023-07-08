import mimetypes

from django.http import FileResponse, HttpResponseBadRequest
from django.shortcuts import render, redirect, get_object_or_404

# Create your views here.
from .models import Product, ProductAttachment
from .forms import ProductForm, ProductUpdateForm, ProductAttachmentInlineFormset

def product_create_view(request):
    context = {}
    form = ProductForm(request.POST or None)
    if form.is_valid():
        obj = form.save(commit=False)
        if request.user.is_authenticated:
            obj.user = request.user
            obj.save()
            return redirect(obj.get_manager_url())
        else:
            form.add_error(None, "You must be logged in to create content")
    context['form'] = form
    return render(request, 'products/create.html', context=context)

def product_list_view(request):
    object_list = Product.objects.all()
    return render(request, 'products/list.html', {"object_list": object_list})

def product_manage_detail_view(request, handle=None):
    obj = get_object_or_404(Product, handle=handle)
    attachments = ProductAttachment.objects.filter(product=obj)
    is_manager = False
    if request.user.is_authenticated:
        is_manager = obj.user == request.user
    context = {"object": obj}
    if not is_manager:
        return HttpResponseBadRequest()
    form = ProductUpdateForm(request.POST or None, request.FILES or None, instance=obj)
    formset = ProductAttachmentInlineFormset(request.POST or None, request.FILES or None, queryset=attachments)
    if form.is_valid() and formset.is_valid():
        instance = form.save(commit=False)
        instance.save()
        formset.save(commit=False)
        for _form in formset:
            attachment_obj = _form.save(commit=False)
            attachment_obj.product = instance
            attachment_obj.save()
        return redirect(obj.get_manage_url())
    context['form'] = form
    context['formset'] = formset
    return render(request, 'products/manager.html', context=context)


def product_detail_view(request, handle=None):
    obj = get_object_or_404(Product, handle=handle) 
    attachments = ProductAttachment.objects.filter(product=obj)
    is_owner = False
    if request.user.is_authenticated:
        is_owner = True
    context = {"object": obj, "is_owner": is_owner,  "attachments": attachments} 
    return render(request, 'products/detail.html', context=context)

def product_attachment_download_view(request, handle=None, pk=None):
    attachment = get_object_or_404(ProductAttachment, product__handle=handle, pk=pk)
    can_download = attachment.is_downloadable or False
    if not request.user.is_authenticated and can_download is False: 
        return HttpResponseBadRequest()
    elif  request.user.is_authenticated:
        can_download = attachment.is_downloadable == True
    file = attachment.file.open(mode='rb')
    filename = attachment.file.name
    content_type, _encoding = mimetypes.guess_type(filename)
    response =  FileResponse(file)
    response['Content-Type'] = content_type or 'application/octet-stream'
    response['Content-Disposition'] = f'attachment;filename={filename}'
    return response