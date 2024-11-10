# Roles Design Documentation

## Overview
Roles in the One Night Werewolf game define the abilities, win conditions, and team affiliations of players. Each role has unique mechanics that influence gameplay, and they interact with the game state and other players in specific ways.

## Role Structure

### BaseRole Class
- **Purpose**: Serves as the abstract base class for all roles.
- **Attributes**:
  - `name`: The name of the role (derived from the class name).
  - `team`: The team affiliation (Village, Werewolf, Independent).
  - `night_action_priority`: The order in which roles act during the night phase, represented as an integer. Lower numbers indicate higher priority.
  - `original_player`: Reference to the player assigned this role.
  - `has_performed_night_action`: Boolean indicating if the role has performed its night action.
  - `action_history`: List to track actions performed by the role.
  - `gained_knowledge`: List to track information learned by the role.

- **Methods**:
  - `get_valid_night_actions(game_state)`: Returns a list of valid night actions for the role.
  - `perform_night_action(action, game_state)`: Executes the specified night action and returns results.
  - `check_win_condition(game_state)`: Checks if the role's win condition is met.
  - `get_known_information()`: Returns information the role has learned.
  - `add_knowledge(info)`: Adds new information learned by the role.
  - `can_view_center_cards()`: Determines if the role can view center cards.
  - `can_swap_cards()`: Determines if the role can swap cards.
  - `must_perform_night_action()`: Determines if the night action is mandatory.
  - `validate_action(action, game_state)`: Validates if an action is legal for this role.

### Role Implementations

#### 1. Villager
- **Team**: Village
- **Night Actions**: None
- **Night Action Priority**: None (not applicable)
- **Win Condition**: Village wins if at least one Werewolf is eliminated.

#### 2. Seer
- **Team**: Village
- **Night Actions**: Can view one player's card or two center cards.
- **Night Action Priority**: 4
- **Win Condition**: Same as Villager.

#### 3. Robber
- **Team**: Village
- **Night Actions**: Can swap their card with another player's card and view their new card.
- **Night Action Priority**: 5
- **Win Condition**: Same as Villager.

#### 4. Troublemaker
- **Team**: Village
- **Night Actions**: Can swap cards between two other players without viewing them.
- **Night Action Priority**: 6
- **Win Condition**: Same as Villager.

#### 5. Mason
- **Team**: Village
- **Night Actions**: Can view other Masons.
- **Night Action Priority**: 3
- **Win Condition**: Same as Villager.

#### 6. Drunk
- **Team**: Village
- **Night Actions**: Must swap their card with a center card without viewing it.
- **Night Action Priority**: 7
- **Win Condition**: Same as Villager.

#### 7. Insomniac
- **Team**: Village
- **Night Actions**: Can view their own card at the end of the night.
- **Night Action Priority**: 8
- **Win Condition**: Same as Villager.

#### 8. Werewolf
- **Team**: Werewolf
- **Night Actions**: Can view other Werewolves and, if alone, view one center card.
- **Night Action Priority**: 1
- **Win Condition**: Werewolves win if no Werewolf is eliminated.

#### 9. Minion
- **Team**: Werewolf
- **Night Actions**: Can view all Werewolves.
- **Night Action Priority**: 2
- **Win Condition**: Wins with the Werewolves if no Werewolf is eliminated.

#### 10. Tanner
- **Team**: Independent
- **Night Actions**: None
- **Night Action Priority**: None (not applicable)
- **Win Condition**: Wins if they are eliminated.

## Interaction with Game State
- Each role interacts with the game state through the `perform_night_action` method, which modifies the game state based on the actions taken.
- Roles can gain knowledge about other players, their roles, and the game state, which influences their decisions and strategies.
- The `check_win_condition` method allows roles to determine if their specific win conditions have been met based on the current game state.

## Validation and Security
- Each role must validate its actions using the `validate_action` method to ensure compliance with game rules.
- Information access must be controlled based on the role's abilities and the current game phase to prevent information leaks.

## Conclusion
The roles in One Night Werewolf are designed to create a dynamic and engaging gameplay experience. Each role has unique abilities and win conditions that contribute to the overall strategy and interaction among players. The structure allows for easy expansion and modification of roles as needed.
