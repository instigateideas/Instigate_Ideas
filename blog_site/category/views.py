from django.shortcuts import render, get_object_or_404, redirect
from .models import Category


def category_list(request):
    sitename = "Categories"
    cat = Category.objects.all()

    return render(request, 'back/news_category.html', {'sitename': sitename, 'category': cat})


def category_add(request):
    sitename = "Add Category"

    if request.method == 'POST':
        name = request.POST.get('catname')
        if name == "":
            error_msg = "Please enter the Category Name..."
            return render(request, 'back/error.html', {'error': error_msg})
        elif len(Category.objects.filter(cat_name=name)) != 0:
            error_msg = "Category Name Already Exists..."
            return render(request, 'back/error.html', {'error': error_msg})

        a = Category(cat_name=name)
        a.save()

    return render(request, 'back/news_category_add.html', {'sitename': sitename})


def category_delete(request, pk):
    cat = Category.objects.get(pk=pk)
    cat.delete()

    return redirect('category_list')
