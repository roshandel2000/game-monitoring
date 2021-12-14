from django.urls import path

from games import views as app_view

urlpatterns = [
    # 1
    path('comparison/<str:name1>/<str:name2>', app_view.ComparisonTwoGames.as_view()),
    # 2
    path('totalsales/<int:fYear>/<int:lYear>', app_view.AnnualSales.as_view()),
    # 3: example: localhost:8000/comparisonpublisher/2006/2015/Sony Computer Entertainment Europe/Konami Digital Entertainment
    path('comparisonpublisher/<int:fYear>/<int:lYear>/<str:fProducer>/<str:lProducer>',
         app_view.AnnualSalesOfProducers.as_view()),

    path('byrank/<int:rank>', app_view.games_by_rank.as_view()),
    path('byname/<str:name>', app_view.games_by_name.as_view()),
    path('best/', app_view.n_best_games_by.as_view()),
    path('5best/', app_view.five_best_selling_by_platform.as_view()),
    path('eurobetternorth/', app_view.better_selling_games_euro_than_north.as_view()),
]
