import requests
from django.http import HttpResponseRedirect
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
        return render(request, 'main/get_started.html')
    elif request.method == "POST":
        username = request.POST.get("username")
        if username:
            try:
                mem_lookup = Member.objects.get(username=username)
            except Member.DoesNotExist:
                # New member
                new_member = Member(username=username)
                new_member.save()
                request.session['userinfo'] = model_to_dict(new_member)
                return HttpResponseRedirect('git_workshop/question1')

            # Already registered. -> Redirect to unsolved question
            values = model_to_dict(mem_lookup)
            request.session['userinfo'] = values
            steps = ""
            for q in ["q1", "q2", "q3", "q4", "q5", "q6", "q7"]:
                if not values.get(q):
                    # The question user has to solve
                    print("Going to {0}".format(q))
                    return HttpResponseRedirect('git_workshop/{0}uestion{1}'.format(q[0], q[1]))

            # Solved all questions
            print(values)
            return render(request, 'main/finished.html', values)
        else:
            # 404
            print("INVALID USERNAME")
            return render(request, 'main/404.html')


def question_one(request):
    """
    First Question.
    Create a public repository named `jaram-workshop-2021`.
    Verify!
    """
    userinfo = request.session.get('userinfo')
    print(userinfo)
    if not userinfo:  # Check for forbidden access
        return render(request, 'main/403.html')

    if request.method == "GET":
        return render(request, 'main/question1.html')
    elif request.method == "POST":
        # Verification
        username = userinfo['username']
        URL = "https://api.github.com/repos/{0}/html-scrapper".format(username)
        response = requests.get(URL)
        print(response.status_code)
        print(response.text)


def question_two(request):
    userinfo = request.session.get('userinfo')
    print(userinfo)
    if not userinfo:
        return render(request, 'main/403.html')

    if not userinfo["q1"]:
        return render(request, 'main/403.html')

    if request.method == "GET":
        return render(request, 'main/question2.html')
    elif request.method == "POST":
        pass


def question_three(request):
    userinfo = request.session.get('userinfo')
    print(userinfo)
    if not userinfo:
        return render(request, 'main/403.html')

    if request.method == "GET":
        return render(request, 'main/question3.html')
    elif request.method == "POST":
        pass


def question_four(request):
    userinfo = request.session.get('userinfo')
    print(userinfo)
    if not userinfo:
        return render(request, 'main/403.html')

    if request.method == "GET":
        return render(request, 'main/question4.html')
    elif request.method == "POST":
        pass


def question_five(request):
    userinfo = request.session.get('userinfo')
    print(userinfo)
    if not userinfo:
        return render(request, 'main/403.html')

    if request.method == "GET":
        return render(request, 'main/question5.html')
    elif request.method == "POST":
        pass


def question_six(request):
    userinfo = request.session.get('userinfo')
    print(userinfo)
    if not userinfo:
        return render(request, 'main/403.html')

    if request.method == "GET":
        return render(request, 'main/question6.html')
    elif request.method == "POST":
        pass


def question_seven(request):
    userinfo = request.session.get('userinfo')
    print(userinfo)
    if not userinfo:
        return render(request, 'main/403.html')

    if request.method == "GET":
        return render(request, 'main/question7.html')
    elif request.method == "POST":
        pass


def validate(question) -> bool:
    # Session validation method.
    return False


def verify(request, question) -> None:
    pass
