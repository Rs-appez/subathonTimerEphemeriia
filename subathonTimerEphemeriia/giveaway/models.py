from django.db import models


class BaseCalendar(models.Model):
    size = models.IntegerField()

    mask_url = models.URLField()

    def __str__(self):
        return str(self.size)


class Calendar(models.Model):
    title = models.CharField(max_length=200)
    background_url = models.URLField()

    base_calendar = models.ForeignKey("BaseCalendar", on_delete=models.CASCADE)

    cells = models.ManyToManyField("CalendarCell", related_name="cells")

    is_active = models.BooleanField(default=False)

    def __str__(self):
        return str(self.title)

    def generate_cells(self):
        """
        Generate cells for the calendar based on the base calendar size.
        """
        cells = Cell.objects.filter(size=self.base_calendar.size)
        for cell in cells:
            calendar_cell = CalendarCell.objects.create(cell=cell)
            self.cells.add(calendar_cell)
        self.save()


class CalendarCell(models.Model):
    cell = models.ForeignKey(
        "Cell", on_delete=models.CASCADE, related_name="calendar_cells"
    )
    reward = models.ForeignKey(
        "Reward", on_delete=models.CASCADE, null=True, blank=True
    )

    is_opened = models.BooleanField(default=False)

    def open(self):
        self.is_opened = True
        self.save()


class Cell(models.Model):
    number = models.IntegerField()
    size = models.IntegerField()

    image_url = models.URLField()

    coordonates = models.CharField(max_length=500)

    def __str__(self):
        return str(self.number)


class Reward(models.Model):
    name = models.CharField(max_length=200)
    image_url = models.URLField()

    def __str__(self):
        return str(self.name)
