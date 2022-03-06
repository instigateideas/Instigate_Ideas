from django.shortcuts import render, get_object_or_404, redirect
from datetime import datetime
from .models import Manager
from django.contrib.auth.models import User, Group, Permission


def manager_list(request):
    sitename = "Manager List"
    manager = Manager.objects.all()
    for mn in manager:
        print(mn.uname)

    return render(request, 'back/manager_list.html', {'sitename': sitename, 'manager': manager})


def manager_delete(request, pk):

    b = Manager.objects.get(pk=pk)
    user = User.objects.filter(username=b.uname)
    user.delete()
    b.delete()

    return redirect('manager_list')


def manager_group(request):
    # Access Restriction to Admin User
    perm = 0
    for i in request.user.groups.all():
        if i.name == 'masteruser':
            perm = 1
    if perm == 0:
        error_msg = "Access Denied...!!!"
        return render(request, 'back/error.html', {'sitename': "Error", 'error': error_msg})

    sitename = "Group"

    group = Group.objects.all().exclude(name='masteruser')

    return render(request, 'back/manager_group.html', {'sitename': sitename, 'group': group})


def manager_group_add(request):
    # Access Restriction to Admin User
    perm = 0
    for i in request.user.groups.all():
        if i.name == 'masteruser':
            perm = 1
    if perm == 0:
        error_msg = "Access Denied...!!!"
        return render(request, 'back/error.html', {'sitename': "Error", 'error': error_msg})

    if request.method == 'POST':
        name = request.POST.get("name")

        if name != "":
            if len(Group.objects.filter(name=name)) == 0:
                b = Group(name=name)
                b.save()

    return redirect('manager_group')


def manager_group_delete(request, pk):
    group = Group.objects.get(pk=pk)
    group.delete()

    return redirect('manager_group')


def user_groups(request, pk):
    sitename = 'User Groups'

    manager = Manager.objects.get(pk=pk)
    user = User.objects.get(username=manager.uname)
    print(user)

    ugroups = []
    for grp in user.groups.all():
        ugroups.append(grp)
    group = Group.objects.all().exclude(name='masteruser')

    return render(request, 'back/user_groups.html', {'sitename': sitename, 'ugroups': ugroups, 'group': group, 'pk': pk})


def add_user_to_groups(request, pk):
    if request.method == 'POST':
        gname = request.POST.get('gname')

        group = Group.objects.get(name=gname)
        manager = Manager.objects.get(pk=pk)
        user = User.objects.get(username=manager.uname)
        user.groups.add(group)

    return redirect('user_groups', pk=pk)


def delete_user_groups(request, pk, name):

    group = Group.objects.get(name=name)
    manager = Manager.objects.get(pk=pk)
    user = User.objects.get(username=manager.uname)
    user.groups.remove(group)

    return redirect('user_groups', pk=pk)
