import matplotlib.pyplot as plt
import numpy as np
from django.db.models import Count
from django.db.models import F
from django.db.models import Sum
from matplotlib.lines import Line2D
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


class ComparisonTwoGames(APIView):
    serializer_class = GamesSerialier
    permission_classes = (IsAuthenticated,)

    def get(self, request, name1, name2):
        game1 = Games.objects.filter(Name=name1)
        game2 = Games.objects.filter(Name=name2)

        NumberofCols = 5
        twoGamesNames = [name1, name2]
        twoGamesCols = []
        maxNumber = 0
        upperMargin = 5  # For Plotting

        for game in [game1, game2]:
            vars = np.zeros((NumberofCols))
            if len(game) != 1:
                for g1 in game:
                    sum_to = np.array([g1.NA_Sales, g1.EU_Sales, g1.JP_Sales, g1.Other_Sales, g1.Global_Sales])
                    vars += sum_to
            else:  # In case there is only a game
                vars = np.array([game.get().NA_Sales, game.get().EU_Sales, game.get().JP_Sales, game.get().Other_Sales,
                                 game.get().Global_Sales])

            maxNumber = max(maxNumber, max(vars))
            twoGamesCols.append(vars)

        ##Plot Type 1:
        # figure, axis = plt.subplots(1, 2, constrained_layout=True, figsize=(15, 10))
        # for index, game in enumerate(twoGamesCols):
        #     axis[index].set_ylim(0, maxNumber+upperMargin)
        #     axis[index].set_title(f"{twoGamesNames[index]}")
        #     axis[index].bar(['NA', 'EU', 'JP', 'Other', 'Global'], game, color=['purple', 'orange', 'green', 'blue', 'red'])
        #     #axis[index].legend(['NA', 'EU', 'JP', 'Other', 'Global'])
        # plt.show()
        # plt.savefig(f"comparison_{twoGamesNames[0]}_with_{twoGamesNames[1]}.png")

        ##Plot Type 2:
        bars = ['NA', 'EU', 'JP', 'Other', 'Global']
        xPos = np.arange(len(bars))
        distanceBetweenGames = 10

        legend_elements = [Line2D([0], [0], color='purple', lw=2, label='NA'),
                           Line2D([0], [0], color='orange', lw=2, label='EU'),
                           Line2D([0], [0], color='green', lw=2, label='JP'),
                           Line2D([0], [0], color='blue', lw=2, label='Other'),
                           Line2D([0], [0], color='red', lw=2, label='Global')]

        plt.bar(xPos, twoGamesCols[0], color=['purple', 'orange', 'green', 'blue', 'red'])
        plt.legend(handles=legend_elements)
        plt.bar(xPos + distanceBetweenGames, twoGamesCols[1], color=['purple', 'orange', 'green', 'blue', 'red'])
        plt.xticks([2, distanceBetweenGames + 2], [name1, name2])
        plt.show()

        return Response(data={
            'NA1': twoGamesCols[0][0],
            'EU1': twoGamesCols[0][1],
            'JP1': twoGamesCols[0][2],
            'Other1': twoGamesCols[0][3],
            'Global1': twoGamesCols[0][4],
            'NA2': twoGamesCols[1][0],
            'EU2': twoGamesCols[1][1],
            'JP2': twoGamesCols[1][2],
            'Other2': twoGamesCols[1][3],
            'Global2': twoGamesCols[1][4],
        })


class AnnualSales(APIView):
    serializer_class = GamesSerialier
    permission_classes = (IsAuthenticated,)

    def get(self, request, fYear, lYear):
        timeSpan = np.arange(fYear, lYear + 1)  # Since it has been defined as [)
        salesOverTimeSpan = [None] * timeSpan.shape[0]
        for index, year in enumerate(timeSpan):
            salesOverTimeSpan[index] = 0
            games_sum = Games.objects.filter(Year=year).aggregate(
                sum=Sum('EU_Sales') + Sum('NA_Sales') + Sum('JP_Sales') + Sum('Other_Sales') + Sum('Global_Sales')).get(
                'sum')
            if games_sum is None:
                games_sum = 0
            salesOverTimeSpan[index] = games_sum

        fig = plt.figure(figsize=(10, 5))
        plt.bar(timeSpan, salesOverTimeSpan)
        plt.title(f"Culmulative Sales between {fYear} and {lYear}")
        plt.xlabel("Year")
        plt.ylabel("Amount of Sale")
        plt.show()
        plt.savefig(f"Culmulative Sales between {fYear} and {lYear}.png")

        return Response(data={
            'year': timeSpan,
            'sales': salesOverTimeSpan,
        })


class AnnualSalesOfProducers(APIView):
    serializer_class = GamesSerialier
    permission_classes = (IsAuthenticated,)

    def get(self, request, fYear, lYear, fProducer, lProducer):
        timeSpan = np.arange(fYear, lYear + 1)  # Since it has been defined as [)
        salesOverTimeSpan = np.zeros((2, timeSpan.shape[0]))
        for index, producer in enumerate([fProducer, lProducer]):
            for idx, year in enumerate(timeSpan):
                games_sum = Games.objects.filter(Year=year, Publisher=producer).aggregate(
                    sum=Sum('EU_Sales') + Sum('NA_Sales') + Sum('JP_Sales') + Sum('Other_Sales') + Sum(
                        'Global_Sales')).get('sum')
                if games_sum is None:
                    games_sum = 0
                salesOverTimeSpan[index][idx] = games_sum

        plt.plot(timeSpan, salesOverTimeSpan[0])
        plt.plot(timeSpan, salesOverTimeSpan[1])
        plt.legend([fProducer, lProducer])
        plt.xlabel("Years")
        plt.ylabel("Amount of Sale")
        plt.show()

        plt.savefig(f"comparison_{fProducer}_with_{lProducer}_Anuually.png")

        return Response(data={
            'Time Span': timeSpan,
            'Sales': salesOverTimeSpan,
        })


class AnnualSalesOfGenres(APIView):
    serializer_class = GamesSerialier
    permission_classes = (IsAuthenticated,)

    def get(self, request, fYear, lYear):

        allGenres = Games.objects.values_list('Genre').distinct()
        allGenresNames = []
        for genre in allGenres:
            allGenresNames.append(genre[0])
        allSales = np.zeros((len(allGenres)))

        for index, genre in enumerate(allGenresNames):
            sale = Games.objects.filter(Genre=genre).filter(Year__lte=lYear).filter(Year__gte=fYear).aggregate(
                sum=Sum('EU_Sales') + Sum('NA_Sales') + Sum('JP_Sales') + Sum('Other_Sales') + Sum('Global_Sales')).get(
                'sum')
            allSales[index] = sale

        fig = plt.figure(figsize=(15, 5))

        plt.bar(allGenresNames, allSales)

        plt.tick_params(axis='x', colors='purple', direction='out', length=13, width=3)
        plt.xlabel("Game Genre")
        plt.ylabel("Amount of Sale")
        plt.title(f"Total Sales between {fYear} and {lYear} per each Genre")
        plt.show()
        plt.savefig(f"Total Sales between {fYear} and {lYear} per Genre.png")

        return Response(data={
            'sales': allSales,
            'genre': allGenresNames,
        })
