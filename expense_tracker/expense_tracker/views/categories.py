from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import ListView

from ..forms import *


class ShowCategories(LoginRequiredMixin, ListView):
    paginate_by = 10
    model = Category
    context_object_name = 'categories'
    template_name = 'expense_tracker/category_list.html'

    def get_queryset(self):
        category = cache.get('category')
        if category is None:
            category = Category.objects.filter(user=self.request.user)
            cache.set('category', category)
        return category

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Категории'
        return context


@login_required
def add_category(request):
    if request.method == 'POST':
        form = AddCategoryForm(request.POST)
        if form.is_valid():
            try:
                category = form.save(commit=False)
                category.user = request.user
                category.save()
                return redirect('categories')
            except: #bare_except
                form.add_error(None, 'Ошибка добавления категории')
    else:
        form = AddCategoryForm()

    context = {
        'form': form,
        'title': 'Добавить категорию',
        'button': 'Добавить'
    }

    return render(request, 'expense_tracker/category_form.html', context)


@login_required
def edit_category(request, pk):
    category = get_object_or_404(Category, pk=pk)
    if request.method == 'POST':
        form = AddCategoryForm(request.POST, instance=category)
        if form.is_valid():
            try:
                category = form.save(commit=False)
                category.user = request.user
                category.save()
                return redirect('categories')
            except: #bare except
                form.add_error(None, 'Ошибка редактирования категории')
    else:
        form = AddCategoryForm(instance=category)

    context = {
        'form': form,
        'title': 'Редактировать категорию',
        'button': 'Изменить'
    }

    return render(request, 'expense_tracker/category_form.html', context)


@login_required
def delete_category(request, pk):
    category = get_object_or_404(Category, pk=pk)
    expenses = Expense.objects.filter(category=category)

    if expenses.exists():
        messages.warning(request, f'Категория {category.name} содержит расходы')
    else:
        messages.info(request, f'Категория {category.name} пуста')

    if request.method == 'POST':
        category.delete()
        return redirect('categories')

    context = {
        'title': 'Удаление категории',
        'category': category.name,
        'category_pk': category.pk,
        'expenses': expenses
    }

    return render(request, 'expense_tracker/delete_category.html', context)
