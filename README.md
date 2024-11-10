# About
This is a demo project for learning how to build AI agents with langchain and langGraph.

## Setup
First install poetry: pipx install poetry
Then run:
- `poetry install` to install dependencies
- `poetry env info --path` for the virtural environment path

If using vscode: ctrl + shift + p and type python: select interpreter, choose "Enter interpreter path" and paste the venv path. Make sure the interpreter path is the path to the virtual environment you just created in poetry. 
It should be something like: Poetry (langgraphbot-uAaZHXKr-py3.12)


## TweetingChainBot
This is a simple example of a twitter bot that uses a reflection chain to improve a tweet. A reflection chain is a chain of llms that first generates a response, then reflects on it and then evaluates it. Based on the evaluation it either accepts the response or asks the generator to improve it.

To run the bot:
- `poetry install` to install dependencies
- `poetry run python tweetingChainBot/main.py`

## TweetingGraphBot
This is a more complex example of a twitter bot that uses a graph to improve a tweet. The graph is defined in the file `tweetingGraphBot/twitter_graph.py`. It is a more complex graph that includes a custom node that uses an llm to generate a response.

To run the bot:
- `poetry install` to install dependencies
- `poetry run python tweetingGraphBot/main.py`

## OneNightWerewolf
This is an experimental project that uses langchain to build a bot for the game One Night Werewolf.

Key architectural points:
1. Role System:
Base Role class with specialized implementations for each role
Each role has specific night actions and win conditions
Roles know their team alignment (Village/Werewolf/Tanner)

2. Player System:
Players maintain their current and original roles
Players use LLM for decision making and mimic discussion
Players keep track of information they learn during the game

3. Host System:
Manages game flow and state
Coordinates night actions in correct order
Facilitates discussion and voting phases
Maintains role-player mapping
Controls information flow between players

4. Game Flow:
LLM Integration:
Players use "hotter" LLM for creative discussion and deception
Host uses "cooler" LLM for consistent rule enforcement
Different prompts for different game phases

6. State Management:
Track original and current roles
Maintain center cards
Record night action results
Store player knowledge

This is a basic framework that can be expanded. We would need to:
1. Implement specific role behaviors
2. Create detailed LLM prompts for each game phase
3. Add game state validation
Implement win condition checking
4. Add proper error handling
5. Create a proper discussion phase structure

# One Night Ultimate Werewolf

A digital implementation of the social deduction game One Night Ultimate Werewolf using LLM for player interactions. 
(This project is done with latest claude sonnet 3.5 to test it reasoning capabilities in project planning, game design and code implementation.)

## Game Rules and Requirements

### Game Setup
- **Player Count**: 3-10 players
- **Total Cards**: Number of players + 3 center cards
- **Card Distribution**:
  - Each player gets 1 random card
  - 3 random cards in center
  - No fixed/guaranteed positions

### Role Pool

#### Village Team
- **Villager**: No special ability
- **Seer**: Views cards
- **Robber**: Swaps and views
- **Troublemaker**: Swaps others
- **Mason**: Knows other Mason
- **Insomniac**: Checks own card at end
- **Drunk**: Blindly swaps with center

#### Werewolf Team
- **Werewolf**: Sees other werewolves
- **Minion**: Sees werewolves

#### Independent
- **Tanner**: Wins by dying

### Night Phase Order
Fixed sequence that never changes:
1. Werewolves
2. Minion
3. Masons
4. Seer
5. Robber
6. Troublemaker
7. Drunk
8. Insomniac

### Night Actions

#### 1. Werewolves
- Open eyes to recognize each other
- If alone, may view one center card

#### 2. Minion
- Views who werewolves are
- Werewolves don't know minion

#### 3. Masons
- Open eyes to see each other

#### 4. Seer
Choose either:
- View another player's card
- View two center cards

#### 5. Robber
- May swap card with another player
- Views new card after swap

#### 6. Troublemaker
- Swaps cards of two other players
- Doesn't view any cards

#### 7. Drunk
- Must swap with center card
- Doesn't view new card

#### 8. Insomniac
- Views own card at night end

### Day Phase
1. Discussion time (~5 minutes)
2. Single voting round
3. Simultaneous voting
4. Ties result in no death

### Win Conditions

#### Village Team wins if:
- At least one werewolf dies
- No one dies when no werewolves in play

#### Werewolf Team wins if:
- No werewolves die

#### Tanner wins if:
- Tanner is killed
- Overrides other win conditions

### Game State Requirements
1. Track original roles (for win conditions)
2. Track current roles (after swaps)
3. Track night action results
4. Maintain center card information
5. Track player knowledge

### Player Requirements
1. Can lie about role/information
2. Must perform night action if called
3. Must pretend to act even if role changed


### Recommended Role Sets by Player Count

These are suggested role combinations for balanced gameplay. All cards are shuffled together, and 3 will randomly end up in the center.

#### 3 Players (6 cards total)
Basic Setup:
- 2 Werewolves
- 3 Villagers
- 1 Seer

Alternative Setup:
- 1 Werewolf
- 1 Seer
- 1 Robber
- 2 Villagers
- 1 Troublemaker

#### 4 Players (7 cards total)
- 1 Werewolf
- 1 Seer
- 1 Robber
- 1 Troublemaker
- 2 Villagers
- 1 Drunk

#### 5 Players (8 cards total)
- 2 Werewolves
- 1 Seer
- 1 Robber
- 1 Troublemaker
- 2 Villagers
- 1 Drunk

#### 6 Players (9 cards total)
- 2 Werewolves
- 1 Seer
- 1 Robber
- 1 Troublemaker
- 1 Drunk
- 2 Villagers
- 1 Insomniac

#### 7 Players (10 cards total)
- 2 Werewolves
- 1 Seer
- 1 Robber
- 1 Troublemaker
- 1 Drunk
- 1 Insomniac
- 2 Villagers
- 1 Tanner

#### 8 Players (11 cards total)
- 2 Werewolves
- 2 Masons
- 1 Seer
- 1 Robber
- 1 Troublemaker
- 1 Drunk
- 2 Villagers
- 1 Insomniac

#### 9-10 Players (12-13 cards total)
Base Setup:
- 2 Werewolves
- 1 Minion
- 2 Masons
- 1 Seer
- 1 Robber
- 1 Troublemaker
- 1 Drunk
- 1 Insomniac
- 2 Villagers
- Add additional Villagers for 10 players

### Important Notes About Role Sets
1. These combinations are recommendations, not strict rules
2. All cards are shuffled together before distribution
3. Any three cards can end up in the center
4. Game balance is maintained by the total role pool, not fixed positions
5. House rules and variations are common and acceptable

### Project Structure
