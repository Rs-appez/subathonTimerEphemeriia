from django.db import models
import threading
import bleach

# Create your models here.
class Bingo(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=False)

    def __str__(self):
        return self.name


    def reset_all_items(self):
        bingo_items = BingoItem.objects.filter(bingo=self)
        bingo_item_users = BingoItemUser.objects.filter(bingo_item__in=bingo_items)
        for bingo_item in bingo_items:
            bingo_item.desactivate_item()
        for bingo_item_user in bingo_item_users:
            bingo_item_user.is_checked = False
            bingo_item_user.save()
    
class BingoItem(models.Model):
    name = models.CharField(max_length=100)
    bingo = models.ForeignKey(Bingo, on_delete=models.CASCADE)
    is_active = models.BooleanField(default=False)

    def __str__(self):
        return self.name
    
    def save(self):
        self.name = bleach.clean(self.name)
        return super().save()
    
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
        min = 5
        timer = threading.Timer(min*60, self.desactivate_item)
        timer.name = f"Auto desactivate item {self.id}"
        timer.start()        
    
class User(models.Model):
    name = models.CharField(max_length=100)
    id_twitch = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name
    
    @staticmethod
    def create_with_bingoIteam(name, id_twitch, bingo):
        user = User.objects.create(name=name, id_twitch=id_twitch)
        bingo_default_items = BingoItem.objects.filter(bingo=bingo).order_by("?")
        for bingo_item in bingo_default_items:
            BingoItemUser.objects.create(user=user, bingo_item=bingo_item)
        return user

    def reset_all_items(self):
        bingo_items = BingoItemUser.objects.filter(user=self)
        for bingo_item in bingo_items:
            bingo_item.is_checked = False
            bingo_item.save()
    
class BingoItemUser(models.Model):
    bingo_item = models.ForeignKey(BingoItem, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    is_checked = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.bingo_item}'
    
    def check_item(self):

        if not self.is_checked :
            self.is_checked = self.bingo_item.is_active
            self.save()
        return self.is_checked

    
