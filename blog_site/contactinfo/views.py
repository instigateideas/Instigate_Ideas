from django.shortcuts import render, get_object_or_404, redirect
from .models import ContactInfo
from datetime import datetime

# Create your views here.
def contact_add(request):
    if request.method == 'POST':
        name = request.POST.get("name")
        email = request.POST.get("email")
        msg = request.POST.get("msg")

        if name == "" or email == "" or msg == "":
            error_msg = "Please enter all the fields"
            return render(request, 'back/error.html', {'sitename': "Error", 'error': error_msg})

        now = datetime.now()
        today = "{}/{}/{}".format(str(now.day).zfill(2), str(now.month).zfill(2), now.year)
        time = "{}:{}".format(now.hour, now.minute)

        b = ContactInfo(name=name, email=email, msg=msg, date=today, time=time)
        b.save()

    return render(request, 'front/msgbox.html', {'sitename': "Message", "msg": "Message has been Posted Successfully"})

def contact_list(request):
    # Login Check
    if not request.user.is_authenticated:
        return redirect('mylogin')
    sitename = "Contact List"

    contact = ContactInfo.objects.all()

    return render(request, 'back/contact_list.html', {'sitename': sitename, 'contacts': contact})

def delete_contact(request, pk):
    # Login Check
    if not request.user.is_authenticated:
        return redirect('mylogin')

    contact = ContactInfo.objects.get(pk=pk)
    contact.delete()

    return redirect('contact_list')

