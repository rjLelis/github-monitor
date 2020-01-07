from django.shortcuts import render, redirect
from auth_access.helpers import login_required


@login_required
def index(request):
    return render(request, 'frontend/index.html')
