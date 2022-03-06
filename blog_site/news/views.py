from django.shortcuts import render, get_object_or_404, redirect
from .models import News
from main.models import Main
from news.models import News
from subcat.models import SubCategory
from category.models import Category
from trending.models import Trending
from django.core.files.storage import FileSystemStorage
from datetime import  datetime


def news_detail(request, word):
    # Login Check
    if not request.user.is_authenticated:
        return redirect('mylogin')

    news = News.objects.all().order_by('-pk')
    lastnews = News.objects.all().order_by('-pk')[0:3]
    cat = Category.objects.all()
    subcat = SubCategory.objects.all()
    site_info = Main.objects.all().order_by('-pk')[0]
    shownews = News.objects.filter(news_title=word)
    popnews = News.objects.all().order_by('-views')[0:5]
    tagname = News.objects.get(news_title=word).tags
    trending = Trending.objects.all()
    tags = tagname.split(",")
    view_counter = News.objects.get(news_title=word)
    view_counter.views = view_counter.views + 1
    view_counter.save()

    return render(request, 'front/news_detail.html', {'sitename': site_info, 'news': news,
                                                      'cat': cat, 'subcat': subcat, 'lastnews': lastnews,
                                                      'siteinfo': site_info, 'shownews': shownews,
                                                      'popnews': popnews, 'tags': tags, 'trending': trending})

def news_list(request):
    # Login Check
    if not request.user.is_authenticated:
        return redirect('mylogin')

    sitename = "List News"
    news = News.objects.all()

    return render(request, 'back/news_list.html', {'news': news, 'sitename': sitename})

def news_add(request):
    # Login Check
    if not request.user.is_authenticated:
        return redirect('mylogin')

    sitename = "Add News"
    print("test post...")

    cat = SubCategory.objects.all()

    now = datetime.now()
    today = "{}/{}/{}".format(str(now.day).zfill(2), str(now.month).zfill(2), now.year)
    time = "{}:{}".format(now.hour, now.minute)

    if request.method == 'POST':
        print("Posted...")
        newstitle = request.POST.get('newstitle')
        print("News Title: ", newstitle)
        newsid = request.POST.get('newscat')
        print("News Sub-Category ID: ", newsid)
        newstxtshort = request.POST.get('newstxtshort')
        print("News Short Text: ", newstxtshort)
        newstxt = request.POST.get('newstxt')
        print("News Text: ", newstxt)
        tags = request.POST.get('tags')


        if (newstitle == "" or newsid == "" or newstxtshort == "" or newstxt == ""):
            error_msg = "Please enter all the fields"
            return render(request, 'back/error.html', {'sitename': "Error", 'error': error_msg})
        try:
            myfile = request.FILES['myfile']
            fs = FileSystemStorage()
            filename = fs.save(myfile.name, myfile)
            url = fs.url(filename)

            if str(myfile.content_type).startswith('image'):

                if myfile.size < 5000000:
                    newscategory = SubCategory.objects.get(pk=newsid).catname
                    ocatid = SubCategory.objects.get(pk=newsid).catid

                    news_article = News(author="-", date=today, picname=filename, picurl=url, news_title=newstitle,
                                        news_text=newstxt, cat_name=newscategory, catid=newsid, short_text=newstxtshort,
                                        ocatid=ocatid, tags=tags)
                    news_article.save()

                    count = len(News.objects.filter(ocatid=ocatid))

                    b = Category.objects.get(pk=ocatid)
                    b.count = count
                    b.save()
                else:
                    error_msg = "Image Size should be less than 5MB"
                    return render(request, 'back/error.html', {'sitename': "Error", 'error': error_msg})
            else:
                fs = FileSystemStorage()
                fs.delete(filename)
                error_msg = "File Format not Supported"
                return render(request, 'back/error.html', {'sitename': "Error", 'error': error_msg})
        except:
            error_msg = "Please attach Image to the News Article"
            return render(request, 'back/error.html', {'sitename': "Error", 'error': error_msg})

    return render(request, 'back/news_add.html', {'sitename': sitename, 'cat': cat})

def error_news(request):
    sitename = "Error"
    error_msg = "All Fields are Required"

    return render(request, 'back/error.html', {'sitename': sitename, 'error': error_msg})


def delete_news(request, pk):
    # Login Check
    if not request.user.is_authenticated:
        return redirect('mylogin')

    try:
        news_obj = News.objects.get(pk=pk)
        ocatid = News.objects.get(pk=pk).ocatid
        fs = FileSystemStorage()
        fs.delete(news_obj.picname)
        # Get the category id before deleting the article
        news_obj.delete()

        count = len(News.objects.filter(ocatid=ocatid))
        print("------------")
        print(count)
        m = Category.objects.get(pk=ocatid)
        m.count = count
        m.save()
    except:
        '''Handle Exception if file deleted manually by user'''
        error_msg = "Something went Wrong..."
        return render(request, 'back/error.html', {'sitename': "Error", 'error': error_msg})

    return redirect('news_list')

def news_edit(request, pk):
    # Login Check
    if not request.user.is_authenticated:
        return redirect('mylogin')

    sitename = "Edit News"

    if len(News.objects.filter(pk=pk)) == 0:
        error_msg = "News not Found"
        return render(request, 'back/error.html', {'sitename': "Error", 'error': error_msg})

    news = News.objects.get(pk=pk)
    cat = SubCategory.objects.all()

    if request.method == 'POST':
        newstitle = request.POST.get('newstitle')
        newsid = request.POST.get('newscat')
        newstxtshort = request.POST.get('newstxtshort')
        newstxt = request.POST.get('newstxt')
        tags = request.POST.get('tags')

        if (newstitle == "" or newsid == "" or newstxtshort == "" or newstxt == ""):
            error_msg = "Please enter all the fields"
            print(error_msg)
            return render(request, 'back/error.html', {'sitename': "Error", 'error': error_msg})
        try:
            myfile = request.FILES['myfile']
            fs = FileSystemStorage()
            filename = fs.save(myfile.name, myfile)
            url = fs.url(filename)

            if str(myfile.content_type).startswith('image'):

                if myfile.size < 5000000:

                    newscategory = SubCategory.objects.get(pk=newsid).catname

                    b = News.objects.get(pk=pk)
                    fss = FileSystemStorage()
                    fss.delete(b.picname)

                    b.picname = filename
                    b.picurl = url
                    b.news_title = newstitle
                    b.news_text = newstxt
                    b.cat_name = newscategory
                    b.cat_id = newsid
                    b.short_text = newstxtshort
                    b.tags = tags
                    b.save()

                    return redirect('news_list')

                else:
                    error_msg = "Image Size should be less than 5MB"
                    return render(request, 'back/error.html', {'sitename': "Error", 'error': error_msg})
            else:
                fs = FileSystemStorage()
                fs.delete(filename)
                error_msg = "File Format not Supported"
                return render(request, 'back/error.html', {'sitename': "Error", 'error': error_msg})
        except:
            b = News.objects.get(pk=pk)
            print("----------------")
            newscategory = SubCategory.objects.get(pk=newsid).catname
            b.news_title = newstitle
            b.news_text = newstxt
            b.cat_name = newscategory
            b.cat_id = newsid
            b.short_text = newstxtshort
            b.tags = tags
            b.save()

            return redirect('news_list')

    return render(request, 'back/news_edit.html', {'sitename': sitename,'pk': pk, 'news': news, 'cat': cat})
