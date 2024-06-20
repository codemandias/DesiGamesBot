import random
import asyncio

roles = ['Raja', 'Mantri', 'Chor', 'Sipahi']

class GameState:
    _instance = None

    def __init__(self):
        if GameState._instance is None:
            GameState._instance = self
            self.game_in_progress = False
            self.players = []
            self.player_roles = {}
            self.scores = {}

    @staticmethod
    def get_instance():
        if GameState._instance is None:
            GameState()
        return GameState._instance

async def setup_rmcs_game(client, message):
    state = GameState.get_instance()
    
    if state.game_in_progress:
        await message.channel.send('A game is already in progress.')
        return

    if len(state.players) < 4:
        state.players.append(message.author)
        await message.channel.send(f'{message.author.mention} has joined the game.')
    
    if len(state.players) == 4:
        state.game_in_progress = True
        await message.channel.send('The game is starting! Assigning roles...')
        random.shuffle(roles)
        
        for i, player in enumerate(state.players):
            state.player_roles[player] = roles[i]
            await player.send(f'Your role is: {roles[i]}')
            
        await asyncio.sleep(2)
        
        for player in state.players:
            if state.player_roles[player] == 'Raja' or state.player_roles[player] == 'Mantri':
                await message.channel.send(f'{player.mention} is {state.player_roles[player]}')

async def handle_reveal(client, message):
    state = GameState.get_instance()
    
    if not state.game_in_progress:
        await message.channel.send('No game in progress.')
        return
    
    # if state.player_roles.get(message.author) != 'Mantri':
    #     await message.channel.send('Only the Mantri can reveal the Chor.')
    #     return
    
    guess = message.mentions[0] if message.mentions else None
    if not guess or guess not in state.players:
        await message.channel.send('You must mention a valid player to guess as Chor.')
        return

    if state.player_roles[guess] == 'Chor':
        result_message = "Raja: 1000, Mantri: 800, Chor: 0, Sipahi: 500"
    else:
        result_message = "Raja: 1000, Mantri: 0, Chor: 800, Sipahi: 500"
    
    # result_message = '\n'.join([f'{player.mention}: {state.scores[player]} points' for player in state.players])
    await message.channel.send(f'Game over!\n\n{result_message}')
    
    # Reset the game
    state.game_in_progress = False
    state.players = []
    state.player_roles = {}