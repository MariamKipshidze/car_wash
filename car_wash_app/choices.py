from django.db.models import IntegerChoices


class OrderFilterChoice(IntegerChoices):
    Last_Week = 1,
    Last_Month = 2,
    Last_Year = 3