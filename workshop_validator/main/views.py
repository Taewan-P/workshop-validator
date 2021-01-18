import requests, json
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.views.decorators.csrf import ensure_csrf_cookie
from django.forms.models import model_to_dict
from django.contrib import messages

from .models import Member


# Create your views here.
def forbidden(request, *args, **argv):
    res = render(request, "main/403.html")
    res.status_code = 403
    return res


def not_found(request, exception):
    res = render(request, "main/404.html")
    res.status_code = 404
    return res


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
                return HttpResponseRedirect('question1/')

            # Already registered. -> Redirect to unsolved question
            values = model_to_dict(mem_lookup)
            request.session['userinfo'] = values
            steps = ""
            for q in ["q1", "q2", "q3", "q4", "q5", "q6", "q7"]:
                if not values.get(q):
                    # The question user has to solve
                    print("Going to {0}".format(q))
                    return HttpResponseRedirect('{0}uestion{1}/'.format(q[0], q[1]))

            # Solved all questions
            print(values)
            return render(request, 'main/finished.html', values)
        else:
            # 404
            print("INVALID USERNAME")
            return HttpResponseRedirect('/404-not-found/')


def question_one(request):
    """
    First Question.
    Create a public repository named `jaram-workshop-2021`.
    Verify! - Will only check for public repository named `jaram-workshop-2021` with provided GitHub username.
    """
    userinfo = request.session.get('userinfo')
    if not userinfo:  # Check for forbidden access
        return HttpResponseRedirect('/forbidden/')

    if request.method == "GET":
        return render(request, 'main/question1.html')
    elif request.method == "POST":
        # Verification
        username = userinfo['username']
        url = "https://api.github.com/repos/{0}/jaram-workshop-2021".format(username)
        response = requests.get(url)
        print(response.status_code)
        if response.status_code == 200:
            # Validate that this user have solved the question
            result = validate(request, "q1", username)
            if result:
                print("Q1 passed. Congrats, {0}".format(username))
                return HttpResponseRedirect('/git_workshop/question2/')
            else:
                print("Q1 Failed. Try Again, {0}".format(username))
                messages.info(request, '검증 실패! 다시 시도해 보세요.')
                return render(request, 'main/question1.html')
        else:
            # Fail
            print("Q1 Failed. Try Again, {0}".format(username))
            messages.info(request, '검증 실패! 다시 시도해 보세요.')
            return render(request, 'main/question1.html')


def question_two(request):
    """
    Second Question.
    Add a file named `README.md` and write anything in it.
    Then. commit this file with commit message `Add README.md` and push to `main` branch repository.
    """
    userinfo = request.session.get('userinfo')
    if not userinfo:
        return HttpResponseRedirect('/forbidden/')

    if not (verify_session(userinfo, "q2") and verify_database(userinfo)):
        return HttpResponseRedirect('/forbidden/')

    if request.method == "GET":
        return render(request, 'main/question2.html')
    elif request.method == "POST":
        pass


def question_three(request):
    userinfo = request.session.get('userinfo')
    if not userinfo:
        return HttpResponseRedirect('/forbidden/')

    if not (verify_session(userinfo, "q3") and verify_database(userinfo)):
        return HttpResponseRedirect('/forbidden/')

    if request.method == "GET":
        return render(request, 'main/question3.html')
    elif request.method == "POST":
        pass


def question_four(request):
    userinfo = request.session.get('userinfo')
    if not userinfo:
        return HttpResponseRedirect('/forbidden/')

    if not (verify_session(userinfo, "q4") and verify_database(userinfo)):
        return HttpResponseRedirect('/forbidden/')

    if request.method == "GET":
        return render(request, 'main/question4.html')
    elif request.method == "POST":
        pass


def question_five(request):
    userinfo = request.session.get('userinfo')
    if not userinfo:
        return HttpResponseRedirect('/forbidden/')

    if not (verify_session(userinfo, "q5") and verify_database(userinfo)):
        return HttpResponseRedirect('/forbidden/')

    if request.method == "GET":
        return render(request, 'main/question5.html')
    elif request.method == "POST":
        pass


def question_six(request):
    userinfo = request.session.get('userinfo')
    if not userinfo:
        return HttpResponseRedirect('/forbidden/')

    if not (verify_session(userinfo, "q6") and verify_database(userinfo)):
        return HttpResponseRedirect('/forbidden/')

    if request.method == "GET":
        return render(request, 'main/question6.html')
    elif request.method == "POST":
        pass


def question_seven(request):
    userinfo = request.session.get('userinfo')
    if not userinfo:
        return HttpResponseRedirect('/forbidden/')

    if not (verify_session(userinfo, "q7") and verify_database(userinfo)):
        return HttpResponseRedirect('/forbidden/')

    if request.method == "GET":
        return render(request, 'main/question7.html')
    elif request.method == "POST":
        pass


def validate(request, question, username) -> bool:
    user = Member.objects.get(username=username)
    userinfo = request.session.get('userinfo')

    if not (verify_session(userinfo, question) and verify_database(userinfo)):
        return False

    if question == "q1":
        user.q1 = True
    elif question == "q2":
        user.q2 = True
    elif question == "q3":
        user.q3 = True
    elif question == "q4":
        user.q4 = True
    elif question == "q5":
        user.q5 = True
    elif question == "q6":
        user.q6 = True
    elif question == "q7":
        user.q7 = True

    user.save()
    userinfo[question] = True
    request.session['userinfo'] = userinfo
    print("Validation complete at {0} for {1}".format(question, userinfo['username']))
    return True


def verify_session(userinfo, question) -> bool:
    for q in ["q1", "q2", "q3", "q4", "q5", "q6", "q7"]:
        if q == question:
            return True

        if userinfo[q]:
            continue
        else:
            return False


def verify_database(userinfo) -> bool:
    user = Member.objects.get(username=userinfo["username"])
    value = model_to_dict(user)
    return value == userinfo
