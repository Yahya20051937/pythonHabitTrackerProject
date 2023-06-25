from . import views

from django.urls import path

urlpatterns = [path('user_home_page/<str:encoded_id>/<str:day>', views.home_page, name='home'),
               path('delete_page/<str:encoded_id>/<str:day>', views.delete_page, name='delete'),
               path('edit_page/<str:encoded_id>/<str:day>', views.edit_page, name='edit'),
               path('add_page/<str:encoded_id>/<str:day>', views.add_page, name='add'),
               path('change_day/<str:encoded_id>', views.change_day, name='change')

               ]
