from . import views

from django.urls import path

urlpatterns = [path('habit_tracking/<str:encoded_id>', views.tracking_home_page, name='home'),
               path("habit_days_streak/<str:encoded_id>", views.get_habit_days_streak_view, name="days_streak"),
               path('habits_performance/<str:encoded_id>', views.get_performance_graph_view, name="performance")
               ]
