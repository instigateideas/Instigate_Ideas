from django.shortcuts import render, get_object_or_404, redirect
from .models import Main
from news.models import News
from category.models import Category
from subcat.models import SubCategory
from trending.models import Trending
from django.core.files.storage import FileSystemStorage
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from manager.models import Manager

def home(request):
    news = News.objects.all().order_by('-pk')
    lastnews = News.objects.all().order_by('-pk')[0:3]
    cat = Category.objects.all()
    subcat = SubCategory.objects.all()
    site_info = Main.objects.all().order_by('-pk')[0]
    popnews = News.objects.all().order_by('-views')[0:5]
    popnews2 = News.objects.all().order_by('-views')[0:3]
    trending = Trending.objects.all()

    return render(request, 'front/home.html', {'sitename': site_info, 'news': news, 'cat': cat, 'subcat': subcat,
                                               'lastnews': lastnews, 'siteinfo': site_info,
                                               'popnews': popnews, 'popnews2': popnews2, 'trending': trending})

def about(request):
    news = News.objects.all().order_by('-pk')
    lastnews = News.objects.all().order_by('-pk')[0:3]
    cat = Category.objects.all()
    subcat = SubCategory.objects.all()
    site_info = Main.objects.all().order_by('-pk')[0]
    popnews = News.objects.all().order_by('-views')[0:5]
    popnews2 = News.objects.all().order_by('-views')[0:3]
    trending = Trending.objects.all()

    return render(request, 'front/about.html', {'sitename': site_info, 'news': news, 'cat': cat,
                                                'subcat': subcat, 'lastnews': lastnews,
                                                'siteinfo': site_info, 'popnews': popnews,
                                                'popnews2': popnews2, 'trending': trending})

def admin_panel(request):
    # Login Check
    if not request.user.is_authenticated:
        return redirect('mylogin')

    sitename = "Dashboard"
    return render(request, 'back/admin_panel.html', {'sitename': sitename})

def mylogin(request):
    sitename = "Login"
    if request.method == 'POST':
        usernametxt = request.POST.get('username')
        passwordtxt = request.POST.get('password')

        if usernametxt != '' and passwordtxt != '':
            user = authenticate(username=usernametxt, password=passwordtxt)
            if user != None:
                login(request, user)
                return redirect("admin_panel")

    return render(request, 'front/login.html', {'sitename': sitename})

def contact(request):
    news = News.objects.all().order_by('-pk')
    lastnews = News.objects.all().order_by('-pk')[0:3]
    cat = Category.objects.all()
    subcat = SubCategory.objects.all()
    site_info = Main.objects.all().order_by('-pk')[0]
    popnews = News.objects.all().order_by('-views')[0:5]
    popnews2 = News.objects.all().order_by('-views')[0:3]
    trending = Trending.objects.all()

    return render(request, 'front/contact.html', {'sitename': site_info, 'news': news,
                                                  'cat': cat, 'subcat': subcat, 'lastnews': lastnews,
                                                  'siteinfo': site_info, 'popnews': popnews,
                                                  'popnews2': popnews2, 'trending': trending})

def mysettings(request):
    # Login Check
    if not request.user.is_authenticated:
        return redirect('mylogin')
    sitename = "My Settings"
    if request.method == 'POST':
        site_name = request.POST.get('sitename')
        about = request.POST.get('about')
        abouttxt = request.POST.get('abouttxt')
        facebook = request.POST.get('fb')
        youtube = request.POST.get('yt')
        twitter = request.POST.get('tw')
        pinterest = request.POST.get('pt')
        vimeo = request.POST.get('vm')

        if facebook == "":
            facebook = "#"
        if youtube == "":
            youtube = "#"
        if twitter == "":
            twitter = "#"
        if pinterest == "":
            pinterest = "#"
        if vimeo == "":
            vimeo = "#"

        if site_name == "" or about =="" or abouttxt == "":
            error_msg = "Sitename and About fields can't be Empty..."
            return render(request, 'back/error.html', {'sitename': "Error", 'error': error_msg})

        try:
            myfile = request.FILES['myfile']
            fs = FileSystemStorage()
            filename = fs.save(myfile.name, myfile)
            url = fs.url(filename)
            if str(myfile.content_type).startswith('image'):
                picname1 = filename
                picurl1 = url
            else:
                fs.delete(filename)
                error_msg = "Logo-1 File Format not Supported"
                return render(request, 'back/error.html', {'sitename': "Error", 'error': error_msg})
        except:
            picname1 = "-"
            picurl1 = "-"

        try:
            myfile2 = request.FILES['myfile2']
            fs2 = FileSystemStorage()
            filename2 = fs2.save(myfile2.name, myfile2)
            url2 = fs.url(filename2)
            if str(myfile2.content_type).startswith('image'):
                picname2 = filename2
                picurl2 = url2
            else:
                fs2.delete(filename2)
                error_msg = "Logo-2 File Format not Supported"
                return render(request, 'back/error.html', {'sitename': "Error", 'error': error_msg})
        except:
            picname2 = "-"
            picurl2 = "-"

        s = Main.objects.all().order_by('-pk')[0]
        s.name = site_name
        s.about = about
        s.abouttxt = abouttxt
        s.fb = facebook
        s.yt = youtube
        s.vm = vimeo
        s.tw = twitter
        s.pt = pinterest
        if picname1 != "-":
            s.picname = picname1
            s.picurl = picurl1
        if picname2 != "-":
            s.picname2 = picname2
            s.picurl2 = picurl2
        s.save()

    site_info = Main.objects.all().order_by('-pk')[0]

    return render(request, 'back/settings.html', {'sitename': sitename, 'siteinfo': site_info})


def mylogout(request):
    logout(request)

    return redirect('mylogin')

def registeruser(request):
    sitename = "Register User"

    if request.method == "POST":
        uname = request.POST.get("username")
        name = request.POST.get("name")
        email = request.POST.get("email")
        password = request.POST.get("pass")
        rep_pass = request.POST.get("rep-pass")

        if rep_pass != password:
            error_msg = "Password didn't match. Please Retry"
            return render(request, 'back/error.html', {'sitename': "Error", 'error': error_msg})
        else:
            if len(password) < 8:
                error_msg = "Password entered should be atleast 8 Character Length"
                return render(request, 'back/error.html', {'sitename': "Error", 'error': error_msg})
            else:
                count1 = 0
                count2 = 0
                count3 = 0
                count4 = 0
                for i in password:
                    if i > "A" or i < "Z":
                        count1 = 1
                    if i > "a" or i < "z":
                        count2 = 1
                    if i > "0" or i < "9":
                        count3 = 1
                    if i > "!" or i < "(":
                        count4 = 1

                if count1 == 1 and count2 == 1 and count3 == 1 and count4 == 1:
                    user = User.objects.create_user(username=uname, password=password, email=email)
                    user.save()
                    b = Manager(name=name, uname=uname, email=email)
                    b.save()
                    return redirect('mylogout')

    return render(request, 'front/register.html', {'sitename': sitename})

def change_password(request):
    # Login Check
    if not request.user.is_authenticated:
        return redirect('mylogin')

    if request.method == "POST":
        oldpass = request.POST.get("oldpass")
        newpass = request.POST.get("newpass")

        if oldpass == "" or newpass == "":
            error_msg = "Password Field can't be Empty"
            return render(request, 'back/error.html', {'sitename': "Error", 'error': error_msg})

        if oldpass != "" or newpass == "":
            user = authenticate(username=request.user, password=oldpass)

            if user != None:
                if len(newpass) < 8:
                    error_msg = "Password entered should be atleast 8 Character Length"
                    return render(request, 'back/error.html', {'sitename': "Error", 'error': error_msg})
                else:
                    count1 = 0
                    count2 = 0
                    count3 = 0
                    count4 = 0
                    for i in newpass:
                        if i > "A" or i < "Z":
                            count1 = 1
                        if i > "a" or i < "z":
                            count2 = 1
                        if i > "0" or i < "9":
                            count3 = 1
                        if i > "!" or i < "(":
                            count4 = 1

                    if count1 == 1 and count2 == 1 and count3 == 1 and count4 == 1:
                        user = User.objects.get(username=request.user)
                        user.set_password(newpass)
                        user.save()
                        return redirect('mylogout')
                    else:
                        error_msg = "Please enter a Strong Password"
                        return render(request, 'back/error.html', {'sitename': "Error", 'error': error_msg})

            else:
                error_msg = "Please enter the Correct Password"
                return render(request, 'back/error.html', {'sitename': "Error", 'error': error_msg})

    sitename = "Change Password"

    return render(request, 'back/change_password.html', {'sitename': sitename})

def forgot_password(request):
    # Login Check
    if not request.user.is_authenticated:
        return redirect('mylogin')

    sitename = "Forgot Password"

    return render(request, 'front/forgot-password.html', {'sitename': sitename})