from django.shortcuts import render

from .models import Bingo, BingoItem, BingoItemUser, User

from math import sqrt
import bleach

def index(request):
    bingo = Bingo.objects.last()


    user_name = request.GET.get('user')
    if user_name:

        user_name = bleach.clean(user_name)
        user = User.objects.filter(name=user_name)
        if not user:
            user = User.objects.create(name=user_name)
            bingo_default_items = BingoItem.objects.filter(bingo=bingo).order_by('?')
            for bingo_item in bingo_default_items:
                BingoItemUser.objects.create(user=user, bingo_item=bingo_item)
            
        else:
            user = user.first()

        bingo_items = BingoItemUser.objects.filter(user=user)
        bingo_lenght = sqrt(len(bingo_items))

        return render(request, 'bingo/bingo.html', {'bingo': bingo, 'bingo_items': bingo_items, 'bingo_lenght': bingo_lenght})
    
    return  render(request, 'bingo/error.html', {'message': 'User not found'})
