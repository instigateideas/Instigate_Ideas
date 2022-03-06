from django.shortcuts import render, get_object_or_404, redirect
from .models import Trending
from datetime import datetime


def add_trending(request):
    # Login Check
    if not request.user.is_authenticated:
        return redirect('mylogin')

    sitename = "Trending"
    now = datetime.now()
    today = "{}/{}/{}".format(str(now.day).zfill(2), str(now.month).zfill(2), now.year)
    time = "{}:{}".format(now.hour, now.minute)

    if request.method == "POST":
        msg = request.POST.get("msg")

        if msg == "":
            error_msg = "Trending Message can't be Empty..."
            return render(request, 'back/error.html', {'sitename': "Error", 'error': error_msg})

        b = Trending(date=today, time=time, txt=msg)
        b.save()

    trending_news = Trending.objects.all()

    return render(request, 'back/trending.html', {'sitename': sitename, 'trending': trending_news})

def delete_trending(request, pk):
    sitename = "Delete Trending"
    b = Trending.objects.get(pk=pk)
    b.delete()
    trending_news = Trending.objects.all()

    return render(request, 'back/trending.html', {'sitename': sitename, 'trending': trending_news})

def edit_trending(request, pk):
    if request.method == "POST":
        msg = request.POST.get("msg")

        if msg == "":
            error_msg = "Trending Message can't be Empty..."
            return render(request, 'back/error.html', {'sitename': "Error", 'error': error_msg})

        now = datetime.now()
        today = "{}/{}/{}".format(str(now.day).zfill(2), str(now.month).zfill(2), now.year)
        time = "{}:{}".format(now.hour, now.minute)

        b = Trending.objects.get(pk=pk)
        b.txt = msg
        b.date = today
        b.time = time
        b.save()
        sitename = "Trending"
        trending_news = Trending.objects.all()
        return render(request, 'back/trending.html', {'sitename': sitename, 'trending': trending_news})

    sitename = "Edit Trending"
    edit_trend = Trending.objects.get(pk=pk)

    return render(request, 'back/trending_edit.html', {'sitename': sitename, 'pk': pk, 'edit_trend': edit_trend})
