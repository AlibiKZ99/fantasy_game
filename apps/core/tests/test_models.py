import random

from django_countries import countries

from apps.account.tasks import create_team_for_user
from django.test import TestCase
from apps.account.models import User
from apps.core.models import Team, Player, Transfer, TransferHistory
from utils import tools, constants


TEST_USERNAME = "Alibi"
TEST_USER_GMAIL = "alibi@gmail.com"
ADDRESS_TYPE = "@gmail.com"
INITIAL_PLAYERS_AMOUNT = 20


class CoreTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username=TEST_USERNAME,
            email=TEST_USER_GMAIL,
            password=tools.get_random_password(),
        )
        create_team_for_user(self.user.id)
        self.team = Team.objects.get(user=self.user.id)
        self.player = Player.objects.filter(team=self.team).first()
        self.transfer = Transfer.objects.create(
            player=self.player, asking_price=constants.INITIAL_PLAYER_COST
        )
        self.transfer_history = TransferHistory.objects.create(
            selling_team=self.team, buying_team=self.team, transfer=self.transfer
        )

    def test_initial_team_cost(self):
        self.assertEqual(
            constants.INITIAL_PLAYER_COST * INITIAL_PLAYERS_AMOUNT, self.team.team_cost
        )

    def test_str_team(self):
        self.assertEqual(str(self.team), f"{self.team.name} / {self.team.country}")

    def test_update_price(self):
        player = Player.objects.filter(team=self.team).first()
        initial_market_value = player.market_value
        country = player.country
        player.update_price(country)
        self.assertGreater(player.market_value, initial_market_value)

    def test_get_price_raise_due_to_age(self):
        players = Player.objects.filter(team=self.team)
        for player in players:
            price_raise = player.get_price_raise_due_to_age()
            if player.age <= constants.YOUNGEST_PLAYER_AGE:
                self.assertEqual(
                    constants.PRICE_RAISE_FOR_YOUNGEST_PLAYERS, price_raise
                )
            elif player.age <= constants.YOUNG_PLAYER_AGE:
                self.assertEqual(constants.PRICE_RAISE_FOR_YOUNG_PLAYERS, price_raise)
            else:
                self.assertEqual(1, price_raise)

    def test_get_price_raise_for_domestic_player(self):
        self.assertEqual(
            self.player.get_price_raise_for_domestic_player(self.player.country),
            constants.PRICE_RAISE_FOR_DOMESTIC_PLAYER,
        )
        while True:
            country = random.choice(list(countries))[1]
            if country != self.player.country:
                self.assertEqual(
                    self.player.get_price_raise_for_domestic_player(country), 1
                )
                break

    def test_team_str(self):
        self.assertEqual(
            str(self.player),
            f"{self.player.first_name} {self.player.last_name} / {self.player.country}",
        )

    def test_transfer_str(self):
        self.assertEqual(
            str(self.transfer),
            f"{self.player.first_name} {self.player.last_name} / {self.transfer.asking_price}",
        )

    def test_transfer_history_str(self):
        self.assertEqual(
            str(self.transfer_history),
            f"{self.transfer} / {self.transfer_history.transferred_time}",
        )
