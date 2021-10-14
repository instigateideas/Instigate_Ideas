from django.shortcuts import render

# Create your views here.
def home_view(request, *args, **kwargs):
	context = {}
	context["name"] = "Arunachalam"
	return render(request, 'personal/home.html', context)