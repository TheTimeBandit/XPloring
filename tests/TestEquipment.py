import contextlib
import io
import unittest

from CommandRunner import CommandRunner
from GameState import GameState


class TestEquipment(unittest.TestCase):

    def setUp(self) -> None:
        self.map0 = '../game_states/game0_repr.json'
        self.game_state = GameState(self.map0)
        self.cr = CommandRunner(self.game_state)

        self.map_two_helmets = '../game_states/game_two_helmets.json'
        self.game_two_helmets = GameState(self.map_two_helmets)
        self.cr_two_helmets = CommandRunner(self.game_two_helmets)

    def tearDown(self) -> None:
        del self.game_state
        del self.cr

    def test_equip_regular_item_inv(self):
        self.cr.execute(["take", "envelope"])
        stdout = io.StringIO()
        with contextlib.redirect_stdout(stdout):
            self.cr.execute(["equip", "envelope"])
        result_output = stdout.getvalue()
        expected_output = "You can't equip the envelope.\n"
        self.assertEqual(expected_output, result_output)

    def test_equip_item_in_inventory(self):
        self.cr.execute(["take", "sword"])
        stdout = io.StringIO()
        with contextlib.redirect_stdout(stdout):
            self.cr.execute(["equip", "sword"])
        result_output = stdout.getvalue()
        expected_output = "You are now equipped with sword\n"
        self.assertEqual(expected_output, result_output)
        self.assertEqual("#equipment_steel_sword", self.game_state.hero.right_hand)

    def test_equip_same_item_twice(self):
        self.cr.execute(["take", "sword"])
        self.cr.execute(["equip", "sword"])
        stdout = io.StringIO()
        with contextlib.redirect_stdout(stdout):
            self.cr.execute(["equip", "sword"])
        result_output = stdout.getvalue()
        expected_output = "You are already equipped with sword\n"
        self.assertEqual(expected_output, result_output)
        self.assertEqual("#equipment_steel_sword", self.game_state.hero.right_hand)

    def test_equip_occupied_slot(self):
        self.cr_two_helmets.execute(["take", "helmet1"])
        self.cr_two_helmets.execute(["equip", "helmet1"])
        self.assertEqual("#helmet1", self.game_two_helmets.hero.head)
        self.cr_two_helmets.execute(["take", "helmet2"])
        stdout = io.StringIO()
        with contextlib.redirect_stdout(stdout):
            self.cr_two_helmets.execute(["equip", "helmet2"])
        result_output = stdout.getvalue()
        expected_output = "You are now equipped with helmet2\n"
        self.assertEqual(expected_output, result_output)
        self.assertEqual("#helmet2", self.game_two_helmets.hero.head)

    def test_equip_already_equipped(self):
        self.cr.execute(["take", "helmet"])
        self.cr.execute(["equip", "helmet"])
        self.cr.execute(["take", "chestplate"])
        self.cr.execute(["equip", "chestplate"])
        self.cr.execute(["take", "sword"])
        self.cr.execute(["equip", "sword"])

        stdout = io.StringIO()
        with contextlib.redirect_stdout(stdout):
            self.cr.execute(["equip", "helmet"])
            self.cr.execute(["equip", "chestplate"])
            self.cr.execute(["equip", "sword"])
        result_output = stdout.getvalue()
        expected_output = f"You are already equipped with helmet\nYou are already equipped with chestplate\nYou are already equipped with sword\n"
        self.assertEqual(expected_output, result_output)