from django.urls import path
from games import views as app_view

urlpatterns = [
    path('byrank/<int:rank>', app_view.games_by_rank.as_view()),
    path('byname/<str:name>', app_view.games_by_name.as_view()),
    path('best/', app_view.n_best_games_by.as_view()),
]