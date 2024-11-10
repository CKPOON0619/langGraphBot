# Host Requirements Specification

The Host is the central controller of the One Night Werewolf game, responsible for managing game flow, state, and player interactions.

## 1. Game Initialization
### Player and Role Management
- Validate player count (3-10 players)
- Select appropriate role set based on player count
- Shuffle and distribute roles:
  - Random role assignment to players
  - Place 3 random cards in center
- Create initial game state
- Record original role assignments

## 2. Night Phase Management
### Action Sequence Control
- Each role will have a `night_action_priority` attribute that determines the order in which roles act during the night phase.
- The Host will retrieve the roles' priorities and execute actions based on their defined order.

### For Each Night Action
- Identify active players for current role
- Present valid action options
- Execute chosen actions
- Update game state
- Maintain action history
- Skip phases with no active players

## 3. Day Phase Management
### Discussion Control
- Initiate discussion phase
- Track discussion time
- Ensure player participation
- Manage information sharing

## 4. Voting Phase Management
### Vote Processing
- Initiate simultaneous voting
- Collect all player votes
- Tally final votes
- Handle tie situations
- Determine elimination

## 5. Game End Management
### Win Condition Verification
Check win conditions based on:
- Original roles
- Final roles
- Voting results

### End Game Processing
- Determine winning team/players
- Reveal all roles
- Display game history

## 6. State Management
### Track Throughout Game
- Current roles (post-swaps)
- Original roles
- Center card information
- Player knowledge
- Night action log
- Complete game history

## 7. Information Control
### Access Management
- Control player-visible information
- Enforce role-based information access
- Manage discussion revelations
- Protect center card information

## Technical Requirements
### Error Handling
- Handle invalid actions
- Manage timeout situations
- Process disconnections/reconnections

### Validation
- Verify action legality
- Validate state changes
- Ensure rule compliance

### Logging
- Record all game events
- Track state changes
- Log player actions

## Integration Requirements
### LLM Integration
- Generate appropriate prompts
- Process LLM responses
- Maintain conversation context

### Player Communication
- Relay necessary information
- Accept player inputs
- Provide feedback

## Notes
- Host must maintain game integrity
- All actions must be deterministic
- State changes must be traceable
- Information leaks must be prevented
