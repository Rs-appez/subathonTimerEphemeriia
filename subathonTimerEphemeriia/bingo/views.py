from django.shortcuts import render

from .models import Bingo, BingoItem, BingoItemUser

from math import sqrt

def index(request):
    bingo = Bingo.objects.last()
    bingo_items = BingoItem.objects.filter(bingo=bingo)
    bingo_lenght = sqrt(len(bingo_items))

    user = request.GET.get('user')
    if user:
        print("user")
        # bingo_item = BingoItem.objects.get(id=user)
        # bingo_item_user = BingoItemUser.objects.get(bingo_item=bingo_item, user=user)
        # bingo_item_user.is_checked = True
        # bingo_item_user.save()

        return render(request, 'bingo/bingo.html', {'bingo': bingo, 'bingo_items': bingo_items, 'bingo_lenght': bingo_lenght})
    print("no user")
    return  render(request, 'bingo/error.html', {'message': 'User not found'})
