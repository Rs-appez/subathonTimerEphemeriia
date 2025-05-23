from django.db import models
from subathonTimerEphemeriia.storage_backends import RewardStorage, BackgroundStorage
from utils.utils import rename_file_to_upload


from random import shuffle


class BaseCalendar(models.Model):
    size = models.IntegerField()

    mask_url = models.URLField()

    def __str__(self):
        return str(self.size)


class Calendar(models.Model):
    title = models.CharField(max_length=200)
    background = models.ImageField(
        storage=BackgroundStorage(),
        default="FONDSCENEVIERGE.jpg",
        upload_to=rename_file_to_upload,
    )

    base_calendar = models.ForeignKey("BaseCalendar", on_delete=models.CASCADE)

    is_active = models.BooleanField(default=False)

    def __str__(self):
        return str(self.title)

    def generate_cells(self):
        """
        Generate cells for the calendar based on the base calendar size.
        """
        cells = Cell.objects.filter(size=self.base_calendar.size)
        for cell in cells:
            CalendarCell.objects.create(cell=cell, calendar=self)

    def get_sorted_cells(self):
        """
        Retrieve calendar cells sorted by the associated cell's number.
        """
        return self.calendarcell_set.order_by("cell__number")

    def activate(self):
        """
        Activate the calendar and deactivate all other calendars.
        """
        Calendar.objects.filter(is_active=True).update(is_active=False)
        self.is_active = True
        self.save()

    def deactivate(self):
        """
        Deactivate the calendar.
        """
        self.is_active = False
        self.save()

    def shuffle_reward(self):
        """
        Shuffle the rewards and assign them to the calendar cells.
        """
        rewards = []
        cells = CalendarCell.objects.filter(calendar=self)
        for cell in cells:
            rewards.append(cell.reward)

        shuffle(rewards)
        for i, cell in enumerate(cells):
            cell.reward = rewards[i]
            cell.save()

    def close_all_cells(self):
        """
        Close all cells in the calendar.
        """
        cells = CalendarCell.objects.filter(calendar=self)
        for cell in cells:
            cell.is_opened = False
            cell.save()


class CalendarCell(models.Model):
    calendar = models.ForeignKey("Calendar", on_delete=models.CASCADE)
    cell = models.ForeignKey(
        "Cell", on_delete=models.CASCADE, related_name="calendar_cells"
    )
    reward = models.ForeignKey(
        "Reward", on_delete=models.SET_NULL, null=True, blank=True
    )

    is_opened = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.calendar} - {self.cell}"

    def open(self):
        self.is_opened = True
        self.save()


class Cell(models.Model):
    number = models.IntegerField()
    size = models.IntegerField()

    image_url = models.URLField()

    coordonates = models.CharField(max_length=500)

    reward_x = models.IntegerField()
    reward_y = models.IntegerField()
    reward_width = models.IntegerField()
    reward_height = models.IntegerField()

    def __str__(self):
        return str(self.number)


class Reward(models.Model):
    name = models.CharField(max_length=200)
    image = models.ImageField(
        storage=RewardStorage(), upload_to=rename_file_to_upload, blank=True, null=True
    )

    def __str__(self):
        return str(self.name)
