from django.shortcuts import render
from django.shortcuts import redirect

def old_login_redirect(request):
    return redirect('login')
# Create your views here.

def index(request):
    return render(request, 'pages/index.html')
