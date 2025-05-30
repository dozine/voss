# from django.contrib import admin
# from django.contrib.admin.sites import AdminSite
# from .models import Counselor
# # Register your models here.

# class VossAdminSite(AdminSite):
#     site_header = 'Voss Admin'
#     site_title = 'Voss Admin Portal'
#     index_title = 'Welcome to Voss Admin'

#     def get_urls(self):
#         urls = super().get_urls()
#         custom_urls = [
#             # 커스텀 URL 추가 가능
#         ]
#         return custom_urls + urls
    
#     def each_context(self, request):
#         context = super().each_context(request)
#         context['custom_admin_css'] = 'adminpage/css/voss_admin.css'
#         return context

# custom_admin_site = VossAdminSite(name='voss_admin')

# custom_admin_site.register(Counselor)

