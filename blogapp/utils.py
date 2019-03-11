from django.shortcuts import render, get_object_or_404, redirect
from .models import *


class ObjectDetailMixin:
    model = None
    template = None

    def get(self, request, slug):
        obj = get_object_or_404(self.model, slug__iexact=slug)
        context = {
            self.model.__name__.lower(): obj,
            'admin_object': obj,
            'detail': True
        }
        return render(request, self.template, context)


class ObjectCreateMixin:
    form_model = None
    template = None

    def get(self, request):
        form = self.form_model
        context = {
            'form': form
        }
        return render(request, self.template, context)

    def post(self,request):
        bound_form = self.form_model(request.POST)
        context = {
            'form': bound_form
        }
        if bound_form.is_valid():
            new_obj = bound_form.save()
            return redirect(new_obj)
        return render(request, self.template, context)


class ObjectUpdateMixin:
    model = None
    model_form = None
    template = None

    def get(self, request, slug):
        obj = self.model.objects.get(slug__iexact=slug)
        #створюємо связану форму присвоюємо наш тег з БД
        bound_form = self.model_form(instance=obj)
        context = {
            'form': bound_form,
            self.model.__name__.lower(): obj
        }
        return render(request, self.template, context)

    def post(self, request, slug):
        obj = self.model.objects.get(slug__iexact=slug)
        bound_form = self.model_form(request.POST, instance=obj)
        context = {
            'form': bound_form,
            self.model.__name__.lower() : obj
        }
        if bound_form.is_valid():
            new_obj = bound_form.save()
            return redirect(new_obj)
        return render(request, self.template, context)


class ObjectDeleteMixin:
    model = None
    template = None
    redirect_template = None

    def get(self, request, slug):
        obj = self.model.objects.get(slug__iexact=slug)
        context = {self.model.__name__.lower(): obj}
        return render(request, self.template, context)

    def post(self, request, slug):
        obj = self.model.objects.get(slug__iexact=slug)
        obj.delete()
        return redirect(reverse(self.redirect_template))