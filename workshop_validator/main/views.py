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
                # New member
                new_member = Member(username=username)
                new_member.save()
                return render(request, 'main/question1.html', model_to_dict(new_member))
            
            # Already registered. -> Redirect to unsolved question
            values = model_to_dict(mem_lookup)
            steps = ""
            for q in ["q1", "q2", "q3", "q4", "q5", "q6", "q7"]:
                if not values.get(q):
                    # The question user has to solve
                    print("Going to {0}".format(q))
                    return render(request, 'main/{0}uestion{1}.html'.format(q[0], q[1]))

            print(values)
            return render(request, 'main/two.html', values)
        else:
            # 404
            print("INVALID USERNAME")
            return render(request, 'main/404.html')