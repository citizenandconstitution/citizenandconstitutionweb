from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login as auth_login
from django.contrib.auth.forms import AuthenticationForm
from .forms import UserRegisterForm
from django.core.mail import EmailMultiAlternatives
from django.template.loader import get_template
from django.shortcuts import redirect
from django.contrib.auth import logout
from .models import Law , LegalCase ,Quiz ,Profile
from django.shortcuts import render, get_object_or_404
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import UserChangeForm
from django.contrib.auth.decorators import login_required
from .forms import ProfileUpdateForm

 

def index(request):
    titles = Law.objects.all()
    return render(request, 'ciz/index.html', {'titles': titles})

def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            email = form.cleaned_data.get('email')
            ######################### mail system #################################### 
            htmly = get_template('shop/Email.html')
            d = { 'username': username }
            subject, from_email, to = 'Welcome', 'your_email@gmail.com', email
            html_content = htmly.render(d)
            msg = EmailMultiAlternatives(subject, html_content, from_email, [to])
            msg.attach_alternative(html_content, "text/html")
            msg.send()
            ################################################################## 
            messages.success(request, 'Your account has been created! You are now able to log in.')
            return redirect('login')
    else:
        form = UserRegisterForm()
    return render(request, 'ciz/register.html', {'form': form, 'title': 'Register Here'})
  
################ login forms################################################### 
def Login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            auth_login(request, user)  # Correct function to log in the user
            messages.success(request, f'Welcome {username}!')
            return redirect('index')
        else:
            messages.info(request, 'Account does not exist or password is incorrect.')
    form = AuthenticationForm()
    return render(request, 'ciz/login.html', {'form': form, 'title': 'Log In'})

def custom_logout(request):
    logout(request)  # Log out the user
    messages.success(request, 'You have been logged out successfully.')
    return redirect('index') 
# Create your views here.
def content(request):
    laws = Law.objects.all()
    return render(request, 'ciz/content.html', {'laws': laws})
def content_detail(request, id):
    law = get_object_or_404(Law, id=id)
    return render(request, 'ciz/content_detail.html', {'law': law})
def legal_case_scenario(request, law_id):
    law = get_object_or_404(Law, id=law_id)
    cases = LegalCase.objects.filter(law=law)
    return render(request, 'ciz/judge.html', {'law': law, 'cases': cases})
def user(request):
    return render(request, 'ciz/user.html')

@login_required
def update_profile(request):
    if request.method == 'POST':
        form = UserChangeForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('user_profile')
    else:
        form = UserChangeForm(instance=request.user)
    
    return render(request, 'ciz/user_update.html', {'form': form})

def about_us(request):
    return render(request, 'ciz/aboutus.html')

def quizzes(request, id):
    law = get_object_or_404(Law, id=id)
    quizzes = Quiz.objects.filter(law=law)
    return render(request, 'ciz/quizz.html', {'law': law, 'quizzes': quizzes})


def submit_quiz(request):
    if request.method == 'POST':
        total_points = 0
        total_possible_points = 0
        incorrect_answers = []  # To keep track of incorrect answers and their correct options

        for key, value in request.POST.items():
            if key.startswith('quiz_'):
                try:
                    quiz_id = int(key.split('_')[1])  # Extract the quiz ID
                    quiz = Quiz.objects.get(id=quiz_id)  # Fetch the quiz object
                    
                    total_possible_points += quiz.points  # Increment total possible points
                    
                    # Check if the submitted answer is correct
                    if value == quiz.correct_answer:
                        total_points += quiz.points  # Increment user's points by quiz points
                    else:
                        # Add the question and the correct answer to the incorrect_answers list
                        incorrect_answers.append({
                            'question': quiz.question,
                            'correct_answer': dict(Quiz.OPTION_CHOICES)[quiz.correct_answer]
                        })
                except (Quiz.DoesNotExist, ValueError):
                    # Log or handle the error as needed
                    continue

        # Generate a result message based on the calculated score
        if total_possible_points > 0:
            if total_points == total_possible_points:
                result_message = f"Excellent! You got a perfect score! {total_points} out of {total_possible_points}"
            elif total_points >= total_possible_points * 0.8:
                result_message = f"Great job! You scored {total_points} out of {total_possible_points}."
            else:
                result_message = f"You scored {total_points} out of {total_possible_points}. Better luck next time!"
        else:
            result_message = "No quizzes were answered. Please try again."

        # Fetch the first law related to the quiz for redirecting to content details
        first_quiz = Quiz.objects.first()
        law = get_object_or_404(Law, id=first_quiz.law.id) if first_quiz else None

        return render(request, 'ciz/submit.html', {
            'law': law,
            'result_message': result_message,
            'incorrect_answers': incorrect_answers  # Pass incorrect answers to the template
        })

    # Redirect to the content page if not a POST request
    return redirect('content')

@login_required
def update_Profile(request):
    # Create profile if it does not exist
    if not hasattr(request.user, 'profile'):
        Profile.objects.create(user=request.user)

    if request.method == 'POST':
        form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.profile)
        if form.is_valid():
            form.save()
            return redirect('user')
    else:
        form = ProfileUpdateForm(instance=request.user.profile)
    
    return render(request, 'ciz/update_Profile.html', {'form': form})

# Correct - gettext called within a function
from django.utils.translation import gettext as _

def some_view(request):
    context = {
        'message': _("This is a translatable message"),
    }
    return render(request, 'layout/main.html', context)