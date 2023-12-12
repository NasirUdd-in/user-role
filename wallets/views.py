from django.shortcuts import render, get_object_or_404

# Create your views here.
# from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from .forms import RegistrationForm, LoginForm
from django.contrib.auth.decorators import login_required
from .models import UserProfile

from django.contrib.auth.models import User
from django.contrib.auth.decorators import user_passes_test

from django.http import HttpResponseBadRequest
from django.contrib.auth import logout

# from .forms import CustomUserChangeForm

from django.shortcuts import render, get_object_or_404, redirect
from .models import UserProfile
from .forms import UserProfileForm, CustomUserForm

from django.contrib.auth.forms import UserChangeForm
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger


from django.shortcuts import render

from django.db.models import Q 

from django.shortcuts import render, redirect
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType

def home(request):
    return render(request, 'home.html') 

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

@login_required
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

# def all_user(request):
#     user = User.objects.all()
#     return render(request, 'test.html', {'user':user})   

@login_required
def all_userprofile(request):
    userprofile = UserProfile.objects.all()
    return render(request, 'test.html', {'userprofile':userprofile}) 

@login_required
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



@login_required
def single_user(request, user_id):
    user = get_object_or_404(UserProfile, id=user_id)
    return render(request, 'single_user.html', {'user': user})
@login_required
def user_logout(request):
    logout(request)
    return redirect('login') 


# def update_user_profile(request, user_id):
#     user_profile = get_object_or_404(UserProfile, user_id=user_id)

#     if request.method == 'POST':
#         form = UserProfileForm(request.POST, instance=user_profile)
#         if form.is_valid():
#             form.save()
#             return redirect('user_details', user_id=user_id)  # Redirect to the user details page or another appropriate page
#     else:
#         form = UserProfileForm(instance=user_profile)

#     return render(request, 'update_user_profile.html', {'form': form, 'user_id': user_id})

# @login_required
# def single_user(request, user_id):
#     user = get_object_or_404(UserProfile, id=user_id)

#     if request.method == 'POST':
#         form = CustomUserChangeForm(request.POST, instance=user)
#         if form.is_valid():
#             form.save()
#             return redirect('profile')  # Redirect to the user's profile page
#     else:
#         form = CustomUserChangeForm(instance=user)

#     return render(request, 'single_user.html', {'form': form, 'user': user})


# def single_user(request, user_id):
#     user_profile = get_object_or_404(UserProfile, user_id=user_id)

#     if request.method == 'POST':
#         form = UserProfileForm(request.POST, instance=user_profile)
#         if form.is_valid():
#             form.save()
#             return redirect('profile')  # Redirect to the user's profile page
#     else:
#         form = UserProfileForm(instance=user_profile)

#     return render(request, 'single_user.html', {'form': form, 'user_profile': user_profile})

# def single_user(request, user_id):
#     user_profile = get_object_or_404(UserProfile, user_id=user_id)

#     if request.method == 'POST':
#         user_form = UserChangeForm(request.POST, instance=user_profile.user)
#         profile_form = UserProfileForm(request.POST, instance=user_profile)
#         if user_form.is_valid() and profile_form.is_valid():
#             user_form.save()
#             profile_form.save()
#             return redirect('profile')  # Redirect to the user's profile page
#     else:
#         user_form = UserChangeForm(instance=user_profile.user)
#         profile_form = UserProfileForm(instance=user_profile)

#     return render(request, 'single_user.html', {'user_form': user_form, 'profile_form': profile_form, 'user_profile': user_profile})
@login_required
def single_user(request, user_id):
    user_profile = get_object_or_404(UserProfile, user_id=user_id)

    if request.method == 'POST':
        user_form = CustomUserForm(request.POST, instance=user_profile.user)
        profile_form = UserProfileForm(request.POST, instance=user_profile)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            return redirect('user_data_page')  # Redirect to the user's profile page
    else:
        user_form = CustomUserForm(instance=user_profile.user)
        profile_form = UserProfileForm(instance=user_profile)

    return render(request, 'single_user.html', {'user_form': user_form, 'profile_form': profile_form, 'user_profile': user_profile})
@login_required
def search_by_username(request):
    if 'username' in request.GET:
        username = request.GET['username']
        user_profiles = UserProfile.objects.filter(user__username__icontains=username)
        return render(request, 'user_list.html', {'user_profiles': user_profiles, 'query': username})
    else:
        return render(request, 'user_list.html', {})
# def search_by_username(request):
#     template_name = 'user_list.html'
#     page = request.GET.get('page', 1)
#     per_page = 3  # Number of profiles to display per page

#     if 'username' in request.GET:
#         username = request.GET['username']
#         user_profiles = UserProfile.objects.filter(user__username__icontains=username)
        
#         paginator = Paginator(user_profiles, per_page)
#         try:
#             user_profiles = paginator.page(page)
#         except EmptyPage:
#             user_profiles = paginator.page(paginator.num_pages)

#         return render(request, template_name, {'user_profiles': user_profiles, 'query': username})
#     else:
#         return render(request, template_name, {})

# def search_by_username(request):
#     if 'username' in request.GET:
#         username = request.GET['username']
#         user_profiles = UserProfile.objects.filter(user__username__icontains=username)

#         # Pagination
#         page = request.GET.get('page', 1)
#         paginator = Paginator(user_profiles, 3)  # Show 10 profiles per page
#         try:
#             user_profiles = paginator.page(page)
#         except PageNotAnInteger:
#             user_profiles = paginator.page(1)
#         except EmptyPage:
#             user_profiles = paginator.page(paginator.num_pages)

#         return render(request, 'user_list.html', {'user_profiles': user_profiles, 'query': username})
#     else:
#         return render(request, 'user_list.html', {})


def Nasir(request):
    hello = UserProfile.objects.all()
    print(hello)

# def process_permission_form(request):
#     if request.method == 'POST':
#         form = PermissionSelectionForm(request.POST)
#         if form.is_valid():
#             group = form.cleaned_data['group']
#             permissions = form.cleaned_data['permissions']

#             # Assign selected permissions to the group
#             for permission in permissions:
#                 CustomPermission.objects.create(group=group, permission=permission)

#             return redirect('success_page')  # Redirect to a success page
#     else:
#         form = PermissionSelectionForm()

#     return render(request, 'create_group.html', {'form': form})


from django.shortcuts import render, redirect
from .forms import GroupPermissionForm

@login_required
def create_group(request):
    if request.method == 'POST':
        form = GroupPermissionForm(request.POST)
        if form.is_valid():
            group = form.save()
            return redirect('create_group')  # Redirect to a success page
    else:
        form = GroupPermissionForm()

    return render(request, 'create_group.html', {'form': form})



from .models import Product

@login_required
def product_list(request):
    products = Product.objects.all()
    return render(request, 'product_list.html', {'products': products})