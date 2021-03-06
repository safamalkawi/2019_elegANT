import sys
from src.model.player import Player
from src.model.game_state import GameState
from src.view.view import View


class Controller:
    def __init__(self):
        self.player = Player()
        self.view = View(1300, 800)
        self.view.change_view_state(View.STARTVIEW)
        self.game_state = None

        self.event_list_start_view = {
            'start_button': self.start_button_pressed,
            'quit_game': self.quit_button_pressed
        }

        self.event_list_game_view = {
            'build_scout': self.create_ant,
            'quit_game': self.quit_button_pressed
        }
        self.game_loop()

    def start_button_pressed(self, color, player_name):
        """
        Event-handler for the start button to change Viewstate from Startview to Gameview
        :param color: Color chosen by player
        :param player_name: Name chosen by player
        :return: returns a game_state object for initialization of the game
        """
        if player_name:
            self.view.change_view_state(View.GAMEVIEW)
            player = Player(color, player_name)
            player_list = [player]
            game_state = GameState(player_list)
            return game_state
        else:
            # TODO Get view to show pop up with message
            print('Player name not entered')

    def quit_button_pressed(self):
        """

        :return: empty
        """
        sys.exit()

    def create_ant(self):
        """
        Event-handler for creating ants using the create ants button
        :param nest_position: Position of nest that should create ants
        :param ant_amount: Amount of ants created with one event
        :return: empty
        """
        print(self.game_state.get_nests())
        nest = self.game_state.get_nests()[0]
        self.game_state.create_ants(nest, amount=1)

    def game_loop(self):
        """
        Main game loop
        :return: empty
        """
        while True:
            if self.game_state is None:
                self.view.draw()

                # Get the list of events from view
                # event_argument_list = self.view.get_event()
                event_argument_list = self.view.events()
                if event_argument_list:
                    print(event_argument_list)

                # Getting events and arguments as two lists
                event = list(event_argument_list.keys())
                args = list(event_argument_list.values())

                # Initializing player and game_state class
                for i in range(len(event)):
                    if event[i] in self.event_list_start_view.keys():
                        if args[i] is not None:
                            self.game_state = self.event_list_start_view[event[i]](*args[i])

            else:
                self.view.draw()
                self.view.update(self.game_state.get_objects_in_region(self.view.pos[0], self.view.pos[1]))

                # Get the list of events from view
                # event_argument_list = self.view.get_event()
                event_argument_list = self.view.events()
                if event_argument_list:
                    print(event_argument_list)

                # Getting events and arguments as two lists
                event = list(event_argument_list.keys())
                args = list(event_argument_list.values())

                for i in range(len(event)):
                    print(event[i])
                    if event[i] in self.event_list_game_view.keys():
                        self.event_list_game_view[event[i]](*args[i])

                self.game_state.update()


if __name__ == "__main__":
    controller = Controller()
    controller.game_loop()
