from django.shortcuts import render_to_response
from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.template import RequestContext
from short_answer.forms import UserForm, UserProfileForm
from django.contrib.auth import logout
from short_answer.models import UserProfile
import knn
import CosineDistance



def index(request):
    return render(request, 'short_answer/index.html')


def register(request):
    context = RequestContext(request)

    registered = False

    if request.method == 'POST':
        user_form = UserForm(data=request.POST)
        profile_form = UserProfileForm(data=request.POST)

        if user_form.is_valid() and profile_form.is_valid():
            user = user_form.save()

            user.set_password(user.password)
            user.save()

            profile = profile_form.save(commit=False)
            profile.user = user
            profile.save()
            registered = True

        else:
            print user_form.errors, profile_form.errors

    else:
        user_form = UserForm()
        profile_form = UserProfileForm()

    # Render the template depending on the context.
    return render_to_response(
            'short_answer/register.html',
            {'user_form': user_form, 'profile_form': profile_form, 'registered': registered},
            context)

def user_login(request):
    context = RequestContext(request)
    if request.method == 'POST':
          username = request.POST['username']
          password = request.POST['password']
          role = request.POST.get('isStudent')

          if role == "Teacher":
              isStudent = False

          elif role == None:
              print  "invalid login details " + username + " " + password
              return render_to_response('short_answer/index.html', {}, context)
          else:
              isStudent = True

          user = authenticate(username=username, password=password)


          if user is not None:
              user2 = UserProfile.objects.get(user=user)
              # Student Account

              if user2.isStudent and isStudent and user.is_active:
                  login(request, user)
                  return HttpResponseRedirect('/short_answer/shome/')
              elif user2.isStudent == False and isStudent:
                  return HttpResponse("INVALID LOGIN ATTEMPT!")
              elif user2.isStudent == True and isStudent == False:
                      return HttpResponse("INVALID LOGIN ATTEMPT!")

              elif user2.isStudent == False and isStudent == False and user.is_active:
                  login(request, user)
                  return HttpResponseRedirect('/short_answer/thome/')


          else:
              # Return an 'invalid login' error message.
              print  "invalid login details " + username + " " + password
              return render_to_response('short_answer/index.html', {}, context)
    else:
        # the login is a  GET request, so just show the user the login form.
        return render_to_response('short_answer/index.html', {}, context)

def shome(request):
            return render(request, 'short_answer/home.html')
def thome(request):
            return render(request, 'short_answer/CreateTest.html')
def test(request):
            return render(request, 'short_answer/sample_test.html')
def question(request):
            return render(request, 'short_answer/question.html')
def addqs(request):
            return render(request, 'short_answer/addqs.html')

def viewscore(request):
            stud_ans = request.POST.get('ans1')
            return HttpResponse(CosineDistance.main(stud_ans))


@login_required
def user_logout(request):
    # Since we know the user is logged in, we can now just log them out.
    logout(request)

    # Take the user back to the homepage.
    return HttpResponseRedirect('/short_answer/')
