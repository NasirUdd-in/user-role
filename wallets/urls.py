from django.urls import path
from .views import product_list,create_group,register, user_login, second_page,all_userprofile, user_data_page,update_user_is_active, user_logout, single_user, home,search_by_username, module_list,activate_product, chart_view


urlpatterns = [
    path('', home, name='home'),
    path('register/', register, name='register'),
    path('login/', user_login, name='login'),
    # Add other paths as needed
    path('details/', second_page, name='second_page'),
    path('test/',all_userprofile, name='create_user_profile'),
    path('user-data/', user_data_page, name='user_data_page'),
    path('update_user_is_active/', update_user_is_active, name='update_user_is_active'),
    path('logout/', user_logout, name='logout'),
    path('single_user/<int:user_id>/', single_user, name='single_user'),
    path('search/', search_by_username, name='search_by_username'),
    path('role/',create_group, name='create_group'),
    path('products/', product_list, name='product_list'),
    path('module-list/', module_list, name="module_list"),
    path('activate_product/<int:product_id>/', activate_product, name='activate_product'),
    path('chart/', chart_view, name='chart_view'),
]


