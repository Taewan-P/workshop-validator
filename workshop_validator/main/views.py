from django.shortcuts import render
from django.views.decorators.csrf import ensure_csrf_cookie
from django.forms.models import model_to_dict

from .models import Member
# Create your views here.

def index(request):
    return render(request, 'main/index.html')

@ensure_csrf_cookie
def main_page(request):
    if request.method == "GET":
        return render(request, 'main/one.html')
    elif request.method == "POST":
        username = request.POST.get("username")
        if username:
            try:
                mem_lookup = Member.objects.get(username=username)
            except Member.DoesNotExist:
                new_member = Member(username=username)
                new_member.save()
                return render(request, 'main/two.html')
            
            # Already registered. -> Redirect to unsolved question
            values = model_to_dict(mem_lookup)
            print(values)
            return render(request, 'main/two.html')
        else:
            # 404
            print("INVALID USERNAME")
            return render(request, 'main/404.html')
