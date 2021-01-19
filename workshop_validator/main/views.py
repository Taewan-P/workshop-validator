import requests, json
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.views.decorators.csrf import ensure_csrf_cookie
from django.forms.models import model_to_dict
from django.contrib import messages
from django.utils import timezone

from .models import Member

sha = ""


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
            return HttpResponseRedirect('/git_workshop/finished/')
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

        # Fail
        print("Q1 Failed. Try Again, {0}".format(username))
        messages.info(request, '검증 실패! 다시 시도해 보세요.')
        return render(request, 'main/question1.html')


def question_two(request):
    """
    Second Question.
    Add a file named `README.md` and write anything in it.
    Then. commit this file with commit message `Add README.md` and push to `main` branch repository.

    *Will Check For...*
    - Whether main branch exists
    - Last commit message of main branch should be equal to the provided text in the problem
    """
    userinfo = request.session.get('userinfo')
    if not userinfo:
        return HttpResponseRedirect('/forbidden/')

    if not (verify_session(userinfo, "q2") and verify_database(userinfo)):
        return HttpResponseRedirect('/forbidden/')

    if request.method == "GET":
        return render(request, 'main/question2.html')
    elif request.method == "POST":
        # Verification
        username = userinfo['username']
        url = "https://api.github.com/repos/{0}/jaram-workshop-2021/branches/main".format(username)
        response = requests.get(url)
        status_code = response.status_code
        response_text = json.loads(response.text)
        if status_code == 200:
            commit = response_text.get("commit")
            if commit:
                msg = commit.get("commit").get("message")
                if msg == "Add README.md":
                    # Success
                    global sha
                    sha = commit.get("sha")
                    result = validate(request, "q2", username)
                    if result:
                        print("Q2 passed. Congrats, {0}".format(username))
                        return HttpResponseRedirect('/git_workshop/question3/')

        # Fail
        print("Q2 Failed. Try Again, {0}".format(username))
        messages.info(request, '검증 실패! 다시 시도해 보세요.')
        return render(request, 'main/question2.html')


def question_three(request):
    """
    Third Question
    Create a branch named `feature`. Publish it.

    *Will Check For...*
    - Whether feature branch exists in the repository.
    """
    userinfo = request.session.get('userinfo')
    if not userinfo:
        return HttpResponseRedirect('/forbidden/')

    if not (verify_session(userinfo, "q3") and verify_database(userinfo)):
        return HttpResponseRedirect('/forbidden/')

    if request.method == "GET":
        return render(request, 'main/question3.html')
    elif request.method == "POST":
        # Verification
        username = userinfo['username']
        url = "https://api.github.com/repos/{0}/jaram-workshop-2021/branches/feature".format(username)
        response = requests.get(url)
        status_code = response.status_code
        if status_code == 200:
            # Success
            result = validate(request, "q3", username)
            if result:
                print("Q3 passed. Congrats, {0}".format(username))
                return HttpResponseRedirect('/git_workshop/question4/')

        # Fail
        print("Q3 Failed. Try Again, {0}".format(username))
        messages.info(request, '검증 실패! 다시 시도해 보세요.')
        return render(request, 'main/question3.html')


def question_four(request):
    """
    Fourth Question.
    Edit README.md in feature branch. Commit and push changes with commit message `Update README.md for Question 4`.

    *Will Check For...*
    - The latest commit message of feature branch should be the provided text in question 4.
    """
    userinfo = request.session.get('userinfo')
    if not userinfo:
        return HttpResponseRedirect('/forbidden/')

    if not (verify_session(userinfo, "q4") and verify_database(userinfo)):
        return HttpResponseRedirect('/forbidden/')

    if request.method == "GET":
        return render(request, 'main/question4.html')
    elif request.method == "POST":
        # Verification
        username = userinfo['username']
        url = "https://api.github.com/repos/{0}/jaram-workshop-2021/branches/feature".format(username)
        response = requests.get(url)
        status_code = response.status_code
        response_text = json.loads(response.text)
        if status_code == 200:
            commit = response_text.get("commit")
            if commit:
                msg = commit.get("commit").get("message")
                if msg == "Update README.md for Question 4":
                    # Success
                    result = validate(request, "q4", username)
                    if result:
                        print("Q4 passed. Congrats, {0}".format(username))
                        return HttpResponseRedirect('/git_workshop/question5/')

        # Fail
        print("Q4 Failed. Try Again, {0}".format(username))
        messages.info(request, '검증 실패! 다시 시도해 보세요.')
        return render(request, 'main/question4.html')


def question_five(request):
    """
    Fifth Question.
    Create a PR named `My First Pull Request` from feature to main branch

    *Will Check For...*
    - Pull Request named string given above exists
    - Making a Pull Request from feature to main branch
    """
    userinfo = request.session.get('userinfo')
    if not userinfo:
        return HttpResponseRedirect('/forbidden/')

    if not (verify_session(userinfo, "q5") and verify_database(userinfo)):
        return HttpResponseRedirect('/forbidden/')

    if request.method == "GET":
        return render(request, 'main/question5.html')
    elif request.method == "POST":
        username = userinfo['username']
        url = "https://api.github.com/repos/{0}/jaram-workshop-2021/pulls".format(username)
        response = requests.get(url)
        status_code = response.status_code
        if status_code == 200:
            pr_list = json.loads(response.text)
            if pr_list:
                if type(pr_list) is list:
                    for pr_json in pr_list:
                        feature_branch = pr_json.get("head").get("label")
                        main_branch = pr_json.get("base").get("label")
                        title = pr_json.get("title")
                        if feature_branch == "{0}:feature".format(username) and main_branch == "{0}:main".format(
                                username):
                            if title == "My First Pull Request":
                                # Success
                                result = validate(request, "q5", username)
                                if result:
                                    print("Q5 passed. Congrats, {0}".format(username))
                                    return HttpResponseRedirect('/git_workshop/question6/')

        # Fail
        print("Q5 Failed. Try Again, {0}".format(username))
        messages.info(request, '검증 실패! 다시 시도해 보세요.')
        return render(request, 'main/question5.html')


def question_six(request):
    """
    Sixth Question.
    Merge your Pull Request. However, set merge commit message name to `Merge "My First Pull Request" into main`.
    *Will Check For...*
    - Latest commit message should be `Merge "My First Pull Request" into main`.
    - Should include commit `Update README.md for Question 4` in main branch with the merged commit.
    - Main branch should be the default branch.
    """
    userinfo = request.session.get('userinfo')
    if not userinfo:
        return HttpResponseRedirect('/forbidden/')

    if not (verify_session(userinfo, "q6") and verify_database(userinfo)):
        return HttpResponseRedirect('/forbidden/')

    if request.method == "GET":
        return render(request, 'main/question6.html')
    elif request.method == "POST":
        username = userinfo['username']
        url = "https://api.github.com/repos/{0}/jaram-workshop-2021/pulls?state=closed".format(username)
        response = requests.get(url)
        status_code = response.status_code
        if status_code == 200:
            pr_list = json.loads(response.text)
            if pr_list:
                if type(pr_list) is list:
                    for pr_json in pr_list:
                        title = pr_json.get("title")
                        if title == "My First Pull Request":
                            merged = pr_json.get("merged_at") is not None
                            if merged:
                                url = "https://api.github.com/repos/{0}/jaram-workshop-2021/commits".format(username)
                                response = requests.get(url)
                                status_code = response.status_code
                                if status_code == 200:
                                    commit_list = json.loads(response.text)
                                    if commit_list:
                                        if type(commit_list) is list:
                                            bool_a = False
                                            bool_b = False
                                            for commit in commit_list:
                                                c = commit.get("commit").get("message")
                                                if commit:
                                                    msg = commit.get("commit").get("message")
                                                    if msg == "Merge \"My First Pull Request\" into main":
                                                        bool_a = True
                                                    elif msg == "Update README.md for Question 4":
                                                        bool_b = True

                                            if bool_a and bool_b:
                                                # Success
                                                result = validate(request, "q6", username)
                                                if result:
                                                    print("Q6 passed. Congrats, {0}".format(username))
                                                    return HttpResponseRedirect('/git_workshop/question7/')

        # Fail
        print("Q6 Failed. Try Again, {0}".format(username))
        messages.info(request, '검증 실패! 다시 시도해 보세요.')
        return render(request, 'main/question6.html')


def question_seven(request):
    """
    Seventh Question.
    Do a hard reset to your repository. Revert all commits after the Pull Request you've made.

    *Will Check For...*
    - The latest commit should be: `Add README.md`, and the sha value should match. (SHA excluded for now...)
    """
    userinfo = request.session.get('userinfo')
    if not userinfo:
        return HttpResponseRedirect('/forbidden/')

    if not (verify_session(userinfo, "q7") and verify_database(userinfo)):
        return HttpResponseRedirect('/forbidden/')

    if request.method == "GET":
        return render(request, 'main/question7.html')
    elif request.method == "POST":
        # Verification
        username = userinfo['username']
        url = "https://api.github.com/repos/{0}/jaram-workshop-2021/branches/main".format(username)
        response = requests.get(url)
        status_code = response.status_code
        response_text = json.loads(response.text)
        if status_code == 200:
            commit = response_text.get("commit")
            if commit:
                msg = commit.get("commit").get("message")
                # sha_after = commit.get("sha")
                if msg == "Add README.md":
                    # global sha
                    # if sha == sha_after:
                    # Success
                    result = validate(request, "q7", username)
                    if result:
                        print("Q7 passed. Congrats, {0}".format(username))
                        return HttpResponseRedirect('/git_workshop/finished/')

        # Fail
        print("Q7 Failed. Try Again, {0}".format(username))
        messages.info(request, '검증 실패! 다시 시도해 보세요.')
        return render(request, 'main/question7.html')


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


def finished(request):
    userinfo = request.session.get('userinfo')
    if not userinfo:
        return HttpResponseRedirect('/forbidden/')

    if not verify_database(userinfo):
        return HttpResponseRedirect('/forbidden/')

    for q in ["q1", "q2", "q3", "q4", "q5", "q6", "q7"]:
        if not userinfo[q]:
            # Fake Session
            return HttpResponseRedirect('/forbidden/')

    username = userinfo['username']
    now = timezone.localtime()
    datestr = now.strftime("%Y-%m-%d  %H:%M")
    return render(request, 'main/finished.html', {'username': username, 'timestamp': datestr})
