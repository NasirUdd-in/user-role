from django.shortcuts import render, get_object_or_404

# Create your views here.
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from .forms import RegistrationForm, LoginForm
from django.contrib.auth.decorators import login_required
from .models import UserProfile

from django.contrib.auth.models import User
from django.contrib.auth.decorators import user_passes_test

from django.http import HttpResponseBadRequest

def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            user.is_active = False  # Move this line here
            user.save()
            login(request, user)
            return redirect('/details/')  # Change 'home' to your home page URL
    else:
        form = RegistrationForm()
    return render(request, 'register.html', {'form': form})

def user_login(request):
    if request.method == 'POST':
        form = LoginForm(request, request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('/details/')  
    else:
        form = LoginForm()
    return render(request, 'login.html', {'form': form})


@login_required
def second_page(request):
    try:
        user_details = UserProfile.objects.get(user=request.user)
        
    except UserProfile.DoesNotExist:
        # Handle the case where the user profile does not exist
        user_details = None
    context = {'user_details': user_details}
    return render(request, 'details.html', context)

@user_passes_test(lambda u: u.is_superuser)
def user_data_page(request):
    try:
        user_profiles = UserProfile.objects.all()
        print(user_profiles)
        return render(request, 'user_list.html', {'user_profiles': user_profiles})
    except Exception as e:
        print(f"An error occurred: {e}")
        # Handle the error or log it as needed
        return render(request, 'user_list.html', {'error_message': str(e)})

@login_required
def toggle_account_status(request):
    if request.method == 'POST':
        user = request.user
        user.is_active = not user.is_active
        user.save()
        return redirect('profile')  # Redirect to the user's profile page or another appropriate page

    return render(request, 'toggle_account_status.html')

def all_user(request):
    user = User.objects.all()
    return render(request, 'test.html', {'user':user})    


def update_user_is_active(request):
    if request.method == 'POST':
        user_ids = request.POST.getlist('user_ids')

        try:
            # Update the is_active status for the UserProfile associated with each selected user
            for user_id in user_ids:
                profile = UserProfile.objects.get(user_id=user_id)
                profile.user.is_active = not profile.user.is_active
                profile.user.save()

            return redirect('user_data_page')  # Redirect to the user list page after updating
        except Exception as e:
            return HttpResponseBadRequest(f"Error updating user status: {str(e)}")

    return HttpResponseBadRequest("Invalid request method")