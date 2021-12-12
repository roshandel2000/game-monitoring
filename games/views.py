from django.db.models import Count
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Games
from .serializers import GamesSerialier


class games_by_rank(APIView):
    serializer_class = GamesSerialier
    permission_classes = (IsAuthenticated,)

    def get(self, request, rank):
        game = Games.objects.filter(id=rank).get()
        result = {
            'name': f"{game.Name}",
            'Platform': f"{game.Platform}",
            'Year': f"{game.Year}",
            'Genre': f"{game.Genre}",
            'Publisher': f"{game.Publisher}",
            'NA_Sales': f"{game.NA_Sales}",
            'EU_Sales': f"{game.EU_Sales}",
            'JP_Sales': f"{game.JP_Sales}",
            'Other_Sales': f"{game.Other_Sales}",
            'Global_Sales': f"{game.Global_Sales}"
        }
        return Response(data=result)


class games_by_name(APIView):
    serializer_class = GamesSerialier
    permission_classes = (IsAuthenticated,)

    def get(self, request, name):
        games = Games.objects.filter(Name__contains=name)

        result = []
        count = 0
        for game in games:
            count += 1
            res = {
                "name": game.Name,
                "platform": game.Platform,
                "year": game.Year,
                "genre": game.Genre,
                "publisher": game.Publisher,
                "na_sales": game.NA_Sales,
                "eu_sales": game.EU_Sales,
                "jp_sales": game.JP_Sales,
                "other_sales": game.Other_Sales,
                "global_sales": game.Global_Sales
            }
            result.append(res)
        return Response(data=result)


class n_best_games_by(APIView):
    serializer_class = GamesSerialier
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        which_one = request.GET.get('which_one')
        num = request.GET.get('number')
        games = Games.objects.values(which_one).annotate(count=Count(which_one))
        selected_games = []
        for game in games:
            if game != "N/A":
                selected_games.append(game.get(which_one))

        res_games = []
        games = []
        for selected_game in selected_games:
            if which_one == "platform":
                res_games = Games.objects.filter(Platform=selected_game).order_by('id')
            elif which_one == "genre":
                res_games = Games.objects.filter(Genre=selected_game).order_by('id')
            elif which_one == "year" and selected_game != 'N/A':
                res_games = Games.objects.filter(Year=selected_game).order_by('id')

            for game in res_games[:int(num)]:
                games.append(f"{selected_game} : name: {game.Name}")

        return Response(data={'result': f"{games},"})


class five_best_selling_by_platform(APIView):
    serializer_class = GamesSerialier
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        year = request.GET.get('year')
        platform = request.GET.get('platform')

        games = Games.objects.filter(Platform=platform).filter(Year=year).order_by('id')
        result = []

        for game in games[:5]:
            result.append(f"name: {game.Name}")

        return Response(data={'result': result, })


class better_selling_games_euro_than_north(APIView):
    serializer_class = GamesSerialier
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        games = Games.objects.filter(EU_Sales__gt=F('NA_Sales'))
        result = []

        for game in games:
            result.append(f"name: {game.Name}")

        return Response(data={'result': result, })