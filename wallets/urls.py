from django.urls import path
from .views import register, user_login, second_page,all_user, user_data_page,update_user_is_active


urlpatterns = [
    path('register/', register, name='register'),
    path('login/', user_login, name='login'),
    # Add other paths as needed
    path('details/', second_page, name='second_page'),
    path('test/', all_user, name='all_user'),
    path('user-data/', user_data_page, name='user_data_page'),
    path('update_user_is_active/', update_user_is_active, name='update_user_is_active'),
]
