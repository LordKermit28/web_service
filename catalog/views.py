from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin, UserPassesTestMixin
from django.core.mail import send_mail
from django.forms import inlineformset_factory
from django.http import Http404, HttpResponseForbidden
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy, reverse
from django.utils.decorators import method_decorator
from django.utils.text import slugify
from django.views.generic import DetailView, ListView, CreateView, UpdateView, DeleteView

from catalog.forms import ProductForm, VersionForm, BlogForm, StaffProductForm
from catalog.models import Product, Version, Blog


class ProductCreationMixin(UserPassesTestMixin):
    def test_func(self):
        return self.request.user.is_authenticated

class ProductUpdateMixin(UserPassesTestMixin):
    def test_func(self):
        product = self.get_object()
        return self.request.user == product.user or self.request.user.groups.filter(name='moder').exists()


def index(request):
    return render(request, 'catalog/index.html')

def contacts(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        phone = request.POST.get('phone')
        message = request.POST.get('message')

        print(name, phone, message)
    return render(request, 'catalog/contacts.html')

class ProductCreateView(ProductCreationMixin, CreateView):
    model = Product
    form_class = ProductForm
    success_url = reverse_lazy('list_product')
    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        VersionFormset = inlineformset_factory(Product, Version, form=VersionForm, extra=1)
        if self.request.method == 'POST':
            context_data['formset'] = VersionFormset(self.request.POST)
        else:
            context_data['formset'] = VersionFormset()
        return context_data

    def form_valid(self, form):
        formset = self.get_context_data()['formset']

        if formset.is_valid():
            self.object = form.save()
            formset.instance = self.object
            formset.save()
            return super().form_valid(form)



class ProductUpdateView(ProductUpdateMixin, UpdateView):
    model = Product
    form_class = ProductForm
    success_url = reverse_lazy('list_product')

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        VersionFormset = inlineformset_factory(Product, Version, form=VersionForm, extra=1)
        if self.request.method == 'POST':
            context_data['formset'] = VersionFormset(self.request.POST, instance=self.object)
        else:
            context_data['formset'] = VersionFormset(instance=self.object)
        return context_data

    def get_form_class(self):
        if self.request.user.is_staff:
            return StaffProductForm
        return super().get_form_class()

    def form_valid(self, form):
        formset = self.get_context_data()['formset']

        if formset.is_valid():
            self.object = form.save()
            formset.instance = self.object
            formset.save()
            return super().form_valid(form)
        else:
            raise self.form_invalid(form)


class ProductListView(LoginRequiredMixin, ListView):
    model = Product

class ProductDetailView(LoginRequiredMixin, DetailView):
    model = Product

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        product = self.get_object()
        versions = product.version_set.all()

        context['versions'] = versions
        return context

class ProductDeleteView(LoginRequiredMixin, DeleteView):
    model = Product
    success_url = reverse_lazy('list_product')

def switch_status_product(request, pk):
    product = get_object_or_404(Product, pk=pk)
    if product.status:
        product.status = False
    else:
        product.status = True
    product.save()

    return redirect(reverse('list_product'))

class BlogCreateView(LoginRequiredMixin, CreateView):
    model = Blog
    form_class = BlogForm
    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        VersionFormset = inlineformset_factory(Product, Version, form=VersionForm, extra=1)
        if self.request.method == 'POST':
            context_data['formset'] = VersionFormset(self.request.POST, instance=self.object)
        else:
            context_data['formset'] = VersionFormset(instance=self.object)
        return context_data

    def form_valid(self, form):
        if form.is_valid():
            new_mat = form.save(commit=False)
            new_mat.slug = slugify(new_mat.title)
            new_mat.save()
            return super().form_valid(form)
        else:
            return self.form_valid(form)

    def get_success_url(self):
        return reverse_lazy('view_blog', args=[self.object.slug])


class BlogListView(ListView):
    model = Blog

class BlogUpdateView(LoginRequiredMixin, UpdateView):
    model = Blog
    form_class = BlogForm
    def get_success_url(self):
        blog_pk = self.kwargs['pk']
        return reverse('view_blog', kwargs={'pk': blog_pk})

class BlogDetailView(LoginRequiredMixin, DetailView):
    model = Blog
    def get_object(self, queryset=None):
        self.object = super().get_object(queryset)
        self.object.views_count += 1
        self.object.save()

        if self.object.views_count == 100:
            subject = "Поздравление с достижением 100 просмотров"
            message = "Поздравляем! Ваша статья достигла 100 просмотров."
            from_email = "your_email@example.com"
            recipient_list = ["recipient_email@example.com"]
            send_mail(subject, message, from_email, recipient_list)

        return self.object


class BlogDeleteView(DeleteView):
    model = Blog
    success_url = reverse_lazy('list_blog')


def switch_status(request, pk):
    blog = get_object_or_404(Blog, pk=pk)
    if blog.published_status:
        blog.published_status = False
    else:
        blog.published_status = True
    blog.save()

    return redirect(reverse('list_blog'))



