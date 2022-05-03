from django.conf import settings
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from django.db.models import Sum

from utils import constants


class Team(models.Model):
    name = models.CharField(max_length=100)
    country = models.CharField(max_length=100)
    team_money = models.PositiveIntegerField(
        default=constants.INITIAL_TEAM_MONEY,
        validators=[
            MinValueValidator(0),
        ],
    )
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    @property
    def team_cost(self):
        return Player.objects.filter(team=self).aggregate(Sum("market_value"))[
            "market_value__sum"
        ]

    def __str__(self):
        return f"{self.name} / {self.country}"


class Player(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    country = models.CharField(max_length=100)
    age = models.PositiveIntegerField(
        validators=[MinValueValidator(18), MaxValueValidator(40)]
    )
    market_value = models.PositiveIntegerField(
        validators=[
            MinValueValidator(0),
        ],
        default=constants.INITIAL_PLAYER_COST,
    )
    team = models.ForeignKey(Team, on_delete=models.CASCADE, related_name="players")
    position = models.CharField(max_length=20, choices=constants.PLAYER_POSITIONS)

    def update_price(self, new_team_country):
        self.market_value *= self.get_price_raise_due_to_age()
        self.market_value *= self.get_price_raise_due_to_position()
        self.market_value *= self.get_price_raise_for_domestic_player(new_team_country)

    def get_price_raise_due_to_age(self):
        if self.age <= constants.YOUNGEST_PLAYER_AGE:
            return constants.PRICE_RAISE_FOR_YOUNGEST_PLAYERS
        elif self.age <= constants.YOUNG_PLAYER_AGE:
            return constants.PRICE_RAISE_FOR_YOUNG_PLAYERS
        return 1

    def get_price_raise_due_to_position(self):
        return constants.PRICE_RAISE_DEPENDING_ON_POSITION[self.position]

    def get_price_raise_for_domestic_player(self, new_team_country):
        if self.country == new_team_country:
            return constants.PRICE_RAISE_FOR_DOMESTIC_PLAYER
        return 1

    def __str__(self):
        return f"{self.first_name} {self.last_name} / {self.country}"


class Transfer(models.Model):
    player = models.ForeignKey(Player, on_delete=models.DO_NOTHING)
    is_sold = models.BooleanField(default=False)
    asking_price = models.PositiveIntegerField(
        validators=[
            MinValueValidator(1),
        ]
    )

    def __str__(self):
        return f"{self.player.first_name} {self.player.last_name} / {self.asking_price}"


class TransferHistory(models.Model):
    transferred_time = models.DateField(auto_now_add=True)
    selling_team = models.ForeignKey(
        Team, on_delete=models.DO_NOTHING, related_name="sales"
    )
    buying_team = models.ForeignKey(
        Team, on_delete=models.DO_NOTHING, related_name="purchases"
    )
    transfer = models.ForeignKey(Transfer, on_delete=models.DO_NOTHING)

    def __str__(self):
        return f"{self.transfer} / {self.transferred_time}"
