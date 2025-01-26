# Assassin Game Manager
# Nic Nikcevic
# With the help Claude for reading in user commands

import random
import json
from typing import List, Optional, Dict

class Team:
    def __init__(self, name: str, players: List[str]):
        self.name = name
        self.players = players
        self.target: Optional['Team'] = None
        self.is_alive = True
    
    def assign_target(self, target: 'Team') -> None:
        self.target = target
    
    def eliminate(self) -> None:
        self.is_alive = False
    
    # convert team to a dictionary for saving
    def to_dict(self) -> dict:
        return {
            'name': self.name,
            'players': self.players,
            'target_name': self.target.name if self.target else None,
            'is_alive': self.is_alive
        }
    
    @classmethod
    # create team from a saved dictionary
    def from_dict(cls, data: dict) -> 'Team':
        team = cls(data['name'], data['players'])
        team.is_alive = data['is_alive']
        return team
    
    # String representation of the team
    def __str__(self) -> str:
        players_str = ", ".join(self.players)
        target_name = self.target.name if self.target else "None"
        status = "Active" if self.is_alive else "Eliminated"
        return f"{self.name} - Players: {players_str} - Target: {target_name}"

class AssassinGame:
    def __init__(self):
        self.teams: Dict[str, Team] = {}
    
    def save_game(self, filename: str = "game_state.json") -> None:
        # Save the current game state to a file
        game_state = {
            'teams': {name: team.to_dict() for name, team in self.teams.items()}
        }
        with open(filename, 'w') as f:
            json.dump(game_state, f, indent=2)
        print(f"Game saved to {filename}")
    
    @classmethod
    # load the game state from a saved file
    def load_game(cls, filename: str = "game_state.json") -> 'AssassinGame':
        game = cls()
        with open(filename, 'r') as f:
            game_state = json.load(f)
        
        # Create all the teams
        for team_data in game_state['teams'].values():
            team = Team.from_dict(team_data)
            game.teams[team.name] = team
        
        # Assign targets
        for team_data in game_state['teams'].values():
            if team_data['target_name']:
                game.teams[team_data['name']].target = game.teams[team_data['target_name']]
        
        return game
    
    def get_active_teams(self) -> List[Team]:
        return [team for team in self.teams.values() if team.is_alive]

    def create_teams_from_file(self, filename: str, team_size: int = 2) -> None:
        # If a game is being created, targets need to be randomly selected
        with open(filename, 'r') as f:
            players = [line.strip() for line in f.readlines() if line.strip()]
        
        random.shuffle(players)
        
        if len(players) < team_size * 2:
            raise ValueError(f"Not enough players. Need at least {team_size * 2} players.")
        
        team_number = 1
        for i in range(0, len(players), team_size):
            team_players = players[i:i + team_size]
            
            if len(team_players) < team_size:
                for j, player in enumerate(team_players):
                    team_name = f"Team {j + 1}"
                    self.teams[team_name].players.append(player)
                break
            
            team_name = f"Team {team_number}"
            self.teams[team_name] = Team(team_name, team_players)
            team_number += 1

    def assign_targets(self) -> None:
        # Randomly assign targets
        active_teams = self.get_active_teams()
        
        if len(active_teams) < 2:
            raise ValueError("Need at least 2 teams to play!")
        
        teams_list = active_teams.copy()
        random.shuffle(teams_list)
        
        for i in range(len(teams_list)):
            current_team = teams_list[i]
            target_team = teams_list[(i + 1) % len(teams_list)]
            current_team.assign_target(target_team)

    def eliminate_team(self, team_name: str) -> None:
        # when a team is eliminated their target needs to be reassigned
        if team_name not in self.teams:
            raise ValueError(f"{team_name} does not exist!")
            
        eliminated_team = self.teams[team_name]
        if not eliminated_team.is_alive:
            raise ValueError(f"Team {team_name} is already eliminated!")
        
        # Find the team whose target was the eliminated team
        hunter_team = None
        for team in self.teams.values():
            if team.is_alive and team.target == eliminated_team:
                hunter_team = team
                break
        
        # Assign that teams target to be the target of the eliminated team
        hunter_team.assign_target(eliminated_team.target)
        eliminated_team.eliminate()


    # The game is over if only one team remains
    def is_game_over(self) -> bool:
        return len(self.get_active_teams()) <= 1

   
    def get_winner(self) -> Optional[Team]:
        active_teams = self.get_active_teams()
        if self.is_game_over() and active_teams:
            return active_teams[0]
        return None

# Print the current state of the game, helpful for weekly emails :)
def print_game_state(game: AssassinGame):
    print("\nCurrent game state:")
    for team in game.teams.values():
        if team.is_alive:
            print(team)

# Read a command from the user
def get_user_command() -> str:
    print("\nAvailable commands:")
    print("- eliminate <team_name>: Eliminate a team")
    print("- save: Save the current game state")
    print("- status: Show current game status")
    print("- quit: Exit the game")
    return input("\nEnter command: ").strip()

def main():
    # Ask user whether to create new game or load existing
    while True:
        choice = input("Would you like to (n)ew game or (l)oad game? ").lower()
        if choice in ['n', 'l']:
            break
        print("Please enter 'n' for new game or 'l' for load game.")

    try:
        if choice == 'n':
            game = AssassinGame()
            game.create_teams_from_file("Players.txt", team_size=2)
            game.assign_targets()
            print("\nNew game created!")
        else:
            game = AssassinGame.load_game()
            print("\nGame loaded!")
        
        print_game_state(game)
        
        # Main game loop
        while not game.is_game_over():
            command = get_user_command()
            command_lower = command.lower()
            
            if command_lower == 'quit':
                save = input("Would you like to save before quitting? (y/n): ").lower()
                if save == 'y':
                    game.save_game()
                break
            
            elif command_lower == 'save':
                game.save_game()
            
            elif command_lower == 'status':
                print_game_state(game)
            
            elif command_lower.startswith('eliminate '):
                team_name = command[10:].strip()
                try:
                    game.eliminate_team(team_name)
                    print(f"\n{team_name} has been eliminated!")
                    print_game_state(game)
                except ValueError as e:
                    print(f"Error: {e}")
            
            else:
                print("Invalid command!")
        
        if game.is_game_over():
            winner = game.get_winner()
            print(f"\nGame Over! Winner: {winner.name}")
    
    except FileNotFoundError as e:
        print(f"Error: Required file not found! {e}")
    except json.JSONDecodeError:
        print("Error: Game save file is corrupted!")
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    main()