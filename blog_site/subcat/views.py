from django.shortcuts import render, get_object_or_404, redirect
from .models import SubCategory
from category.models import Category


def subcategory_list(request):
    # Login Check
    if not request.user.is_authenticated:
        return redirect('mylogin')

    sitename = "Sub-Categories"
    subcat = SubCategory.objects.all()

    return render(request, 'back/news_subcategory.html', {'sitename': sitename, 'subcat': subcat})


def subcategory_add(request):
    # Login Check
    if not request.user.is_authenticated:
        return redirect('mylogin')

    cat = Category.objects.all()

    sitename = "Add Sub-Category"
    if request.method == 'POST':
        name = request.POST.get('subcatname')
        catid = request.POST.get('newscat')
        if name == "":
            error_msg = "Please enter the Sub-Category Name..."
            return render(request, 'back/error.html', {'error': error_msg})
        elif len(SubCategory.objects.filter(subcat_name=name)) != 0:
            error_msg = "Sub-Category Name Already Exists..."
            return render(request, 'back/error.html', {'error': error_msg})

        catname = cat.get(pk=catid).cat_name
        a = SubCategory(subcat_name=name, catid=catid, catname=catname)
        a.save()
        return redirect('subcategory_list')

    return render(request, 'back/news_subcategory_add.html', {'sitename': sitename, 'cat': cat})


def subcategory_delete(request, pk):
    # Login Check
    if not request.user.is_authenticated:
        return redirect('mylogin')

    subcat = SubCategory.objects.get(pk=pk)
    subcat.delete()

    return redirect('subcategory_list')
