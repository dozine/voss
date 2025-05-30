from django.urls import path
from . import api
from crm import api as crm_api
# from notice import api as notice_api
from useraccount import api as user_api
# from call import api as call_api


urlpatterns = [
    # path('admin-login/', api.admin_login, name='admin-login'),
    # path('admin-logout/', api.admin_logout, name='admin-logout'),
    # path('admin-profile/', api.admin_profile, name='admin-profile'),
    
    path('admin-home/', api.admin_home, name='admin-home'),

    # Counselor URLs
    path('user/', user_api.user_list, name='user-list'),
    path('user/<pk>/', user_api.user_detail, name='user-detail'),

    # # Customer URLs
    # path('customers/', crm_api.special_list, name='customer-list'),
    # path('customers/<phone>/', crm_api.customers_detail, name='customer-detail'),

    # VOC Record URLs
    # path('records/', call_api.voc_record_list, name='record-list'),
    # path('records/<int:pk>/', call_api.voc_record_detail, name='record-detail'),

    # # Notice URLs
    # path('posts/', notice_api.posts_list, name='post-list'),
    # path('posts/create/', notice_api.create_post, name='create-post'),
    # path('posts/<int:pk>/', notice_api.posts_detail, name='post-detail'),
    # path('posts/<int:pk>/update/', notice_api.update_post, name='update-post'),
    # path('posts/<int:pk>/delete/', notice_api.delete_post, name='delete-post'),
]