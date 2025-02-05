from django.db import models
import threading
import math

import bleach


class Bingo(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=False)

    def __str__(self):
        return str(self.name)

    def reset_all_items(self):
        bingo_items = BingoItem.objects.filter(bingo=self)
        users = User.objects.all()
        for bingo_item in bingo_items:
            bingo_item.desactivate_item()
        for user in users:
            user.reset_all_items(self)

    def activate_bingo(self):

        old_bingos = Bingo.objects.filter(is_active=True)
        for bingo in old_bingos:
            bingo.desactivate_bingo()

        self.is_active = True
        self.save()

    def desactivate_bingo(self):
        self.is_active = False
        self.save()
        return self.is_active


class BingoItem(models.Model):
    name = models.CharField(max_length=100)
    bingo = models.ForeignKey(Bingo, on_delete=models.CASCADE)
    is_active = models.BooleanField(default=False)

    def __str__(self):
        return self.name

    def save(self, **kwargs):
        self.name = bleach.clean(self.name).upper()
        return super().save(**kwargs)

    def activate_item(self):
        self.is_active = True
        self.save()
        self.__auto_desactivate()
        return self.is_active

    def desactivate_item(self):
        self.is_active = False
        self.save()
        return self.is_active

    def __auto_desactivate(self):
        min = 6
        timer = threading.Timer(min * 60, self.desactivate_item)
        timer.name = f"Auto desactivate item {self.id}"
        timer.start()


class User(models.Model):
    name = models.CharField(max_length=100)
    id_twitch = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    has_won = models.BooleanField(default=False)

    def __str__(self):
        return str(self.name)

    def save(self, **kwargs):
        self.name = bleach.clean(self.name)
        return super().save(**kwargs)

    @staticmethod
    def create_with_bingoIteam(name, id_twitch, bingo):
        user = User.objects.create(name=name, id_twitch=id_twitch)
        user.get_new_items(bingo)

        return user

    def get_bingo_items(self, bingo):

        bingo_items = BingoItemUser.objects.filter(
            user=self, bingo_item__bingo=bingo
        ).order_by("id")

        if not bingo_items:
            self.get_new_items(bingo)
            bingo_items = BingoItemUser.objects.filter(
                user=self, bingo_item__bingo=bingo
            ).order_by("id")

        return bingo_items

    def get_new_items(self, bingo):
        bingo_default_items = BingoItem.objects.filter(bingo=bingo).order_by("?")
        BingoItemUser.objects.filter(user=self, bingo_item__bingo=bingo).delete()
        for bingo_item in bingo_default_items:
            BingoItemUser.objects.create(user=self, bingo_item=bingo_item)
        self.save()

    def reset_all_items(self, bingo):
        BingoItemUser.objects.filter(user=self, bingo_item__bingo=bingo).delete()

        self.has_won = False
        self.save()

    def win(self):
        self.has_won = True
        self.save()


class BingoItemUser(models.Model):
    bingo_item = models.ForeignKey(BingoItem, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    is_checked = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.bingo_item}"

    def check_item(self):

        if not self.is_checked:
            self.is_checked = self.bingo_item.is_active
            self.save()
        return self.is_checked

    def check_bingo(self):
        bingo_items = BingoItemUser.objects.filter(user=self.user).order_by("id")

        size = int(math.sqrt(len(bingo_items)))

        for i in range(size):
            line = bingo_items[i * size : (i + 1) * size]
            if all([item.is_checked for item in line]):
                return True

            column = bingo_items[i::size]
            if all([item.is_checked for item in column]):
                return True

        diagonal1 = bingo_items[:: size + 1]
        if all([item.is_checked for item in diagonal1]):
            return True

        diagonal2 = bingo_items[size - 1 :: size - 1][:size]
        if all([item.is_checked for item in diagonal2]):
            return True

        return False
