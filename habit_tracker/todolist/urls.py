from . import views

from django.urls import path

urlpatterns = [path('user_home_page/<str:encoded_id>', views.home_page, name='home'),
               path('delete_page/<str:encoded_id>', views.delete_page, name='delete'),
               path('edit_page/<str:encoded_id>', views.edit_page, name='edit'),
               path('add_page/<str:encoded_id>', views.add_page, name='add'),
               path("test/<str:encoded_id>", views.test, name='test')
               ]
