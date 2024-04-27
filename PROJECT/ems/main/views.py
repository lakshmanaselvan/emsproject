from django import forms
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.contrib.auth.hashers import check_password
from django.core.mail import send_mail
from main.models import UserProfile
from .forms import RegistrationForm
from django.conf import settings
from .forms import EventForm
from .models import Event
from datetime import date

# Create your views here.

def home(request):
    return render(request, "home.html", {})

def registration(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            # username = form.cleaned_data['name']
            # email = form.cleaned_data['email']
            # password = form.cleaned_data['password']
            user_profile = form.save(commit=False)
            user_profile.save()
            token = user_profile.token
            domain_name = get_current_site(request).domain
            verified_link = f'http://{domain_name}/verified/{token}'
            send_mail (
                'Email Verification',
                f'Please click this following link to verify your email: {verified_link}',
                settings.EMAIL_HOST_USER,
                [user_profile.email],
                fail_silently =False
            )
            return render(request, 'registrationSuccess.html', {})
    else:
        form = RegistrationForm()
    return render(request, 'registrationForm.html', {'form': form})

def verified(request, token):
    try:
        user = get_object_or_404(UserProfile, token = token)
        if not user.is_verified:
            user.is_verified = True
            user.save()
            return render(request, 'success.html', {})
    except Exception as e:
        msg = str(e)
        return render(request, 'registrationForm.html', {'msg':msg})

def login(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']
        user_profile = UserProfile.objects.get(email=email)
        if check_password(password, user_profile.password):
            if user_profile.is_verified:
                print('Hai')
                request.session['user_id'] = user_profile.id 
                if user_profile.role == 'Student':
                    return redirect(login)
                else:
                    return redirect(create_event)
            else:
                return render(request, 'login.html', {'error_message': 'Your email is not verified yet'})
        else:
            print('Hai')
            return render(request, 'login.html', {'error_message':'Invalid Email or Password'})
    return render(request, 'login.html')

@login_required
def create_event(request):
    if request.method == 'POST':
        form = EventForm(request.POST)
        if form.is_valid():
           user_id = request.session.get('user_id')
           if user_id:
                # Retrieve the user object using the user ID
                user = UserProfile.objects.get(pk=user_id)
                # Associate the user with the event being created
                event = form.save(commit=False)
                event.organizer = user
                event.save()
                subject = 'Event Approval Request'
                html_message = render_to_string('approval_email.html', {'event': event})
                plain_message = strip_tags(html_message)
                from_email =  user.email
                to_email = settings.EMAIL_HOST_USER 
                send_mail(subject, plain_message, from_email, [to_email], html_message=html_message)
                return render(request, 'eventSuccess.html', {})
           else:
                return render(request, 'create_event.html', {'form':form})
    else:
        form = EventForm()
    return render(request, 'create_event.html', {'form':form})


def view_event(request):
    today = date.today()
    event_list = Event.objects.all()
    return render(request, "event_list.html", {'event_list':event_list, 'today': today})

def profile(request):
    user_id = request.session.get('user_id')
    event = Event.objects.filter(organizer=user_id)
    user = UserProfile.objects.get(pk=user_id)
    print(user)
    return render(request, 'profile.html', {'event': event,'current_user':user})

def logout(request):
    request.session.clear()
    return redirect(login)

# def approve_event(request, event_id):
#     event = get_object_or_404(Event, pk=event_id)
#     # Update the approval status of the event to True
#     event.approved = True
#     event.save()
#     # Redirect to a success page or event details page
#     return redirect('event_details', event_id=event_id)

# def event_details(request, event_id):
#     event = get_object_or_404(Event, pk=event_id)
#     return render(request, 'event_details.html', {'event': event})