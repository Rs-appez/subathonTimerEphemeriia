from django.shortcuts import render

from .models import Bingo, BingoItem

from math import sqrt

def index(request):
    bingo = Bingo.objects.last()
    bingo_items = BingoItem.objects.filter(bingo=bingo)

    bingo_lenght = sqrt(len(bingo_items))

    return render(request, 'bingo.html', {'bingo': bingo, 'bingo_items': bingo_items, 'bingo_lenght': bingo_lenght})
