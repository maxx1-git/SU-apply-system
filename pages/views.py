from django.shortcuts import render
from django.shortcuts import redirect
from unit.models import Members ,Classes

def old_login_redirect(request):
    return redirect('login')
# Create your views here.

def index(request):
    members = Members.objects.select_related(
        'class_level'
    ).order_by('class_level__name')
    context = {
        'members': members,
    }
    return render(request, 'pages/index.html', context)
