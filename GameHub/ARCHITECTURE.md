# Architecture notes

## Core interfaces

- `core/game.py` and `core/match.py` keep the sequential engine. Each `Game` subclass describes turn order, legal moves, state transitions, terminal checks, and final results.
- `core/simultaneous.py` introduces `SimultaneousGame` and `SimultaneousMatch`, which assume every player chooses an action before the joint state update. Bots reuse the same `Player` interface and plug into either runner.

## Registry plumbing

- `registry.py` keeps a catalog of sequential/simultaneous games, bots, and optional interaction factories so `runners/play.py` can discover titles automatically. Registering a new game or bot there makes it available to the unified runner and any new UI.
- Each game module (e.g., `games/tictactoe`, `games/rps`) calls the registry during import, so the interactive menu never needs to know about concrete classes.
- `ConfigPrompt` entries attach per-bot configuration prompts; `runners/play.py` stores the answers in `configs/bot_configs.json` via `config_store.py` so depth/seed values persist across runs unless overridden.
- Game metadata (`GameConfig`) lives in `configs/game_configs.json` and can seed UI defaults or future settings screens, so new games can advertise descriptions and defaults without touching the runner.
- `ConfigPrompt` objects let you ask for depth limits, RNG seeds, or other bot-specific settings when the user configures a bot. The `runners/play.py` loop gathers those values before constructing the bot so every bot can expose its own “level” controls without changing the runner.

## Adding a game

1. Create a `games/<name>/state.py` that subclasses `core.state.State` (implementing `active_players` and `copy`) for the domain.
2. Add `games/<name>/game.py` that inherits from `Game` or `SimultaneousGame`, declares `player_ids`, legal actions, `next_state`, and terminal/result logic, then exposes constants like `PLAYERS` for reuse.
3. Implement player adapters under `players/<type>/<game>/` to keep decision logic separate from rules (e.g., the new `players/ai/games/rps/random.py`).
4. Wire everything through `runners/*` (e.g., `runners/rps_bot_match.py`), which builds the game instance, selects bots, runs the proper match runner, and handles presentation (print summary, CLI prompts, or logs).

## Interaction hints

- Keep I/O out of the core engines. Instead, let runners or dedicated `interaction` adapters render states, ask humans for moves, and feed actions to bots.
- When you add a new bot, accept the relevant `State` type and `legal_actions` iterable; the core `Match`/`SimultaneousMatch` loop already feeds actions in order.
- For simultaneous games, ensure each `Player` implementation only uses the visible state and the legal actions provided in that tick.

## Templates and play runner

- `templates/sequential_game.py`, `templates/simultaneous_game.py`, and `templates/bot_template.py` outline the minimal overrides and registration calls so new games and bots can be scaffolded without guessing which methods the core engine requires.
- `runners/play.py` provides the recommended entry point. It lists registered games/bots, asks for player assignments, and dispatches either `Match` or `SimultaneousMatch`. Launch it via `PYTHONPATH=. python runners/play.py` once you register new content—the menu updates automatically.
- The play runner also wires an `EventBus` plus subscribers (`TerminalLogger`, `SimpleWebBridge`, any interaction port that implements `EventHandler`) so turns/actions/results stream to outside listeners without changing game logic.

## Sequential games & interaction

- Sequential games keep using `core/match.Match`. Human representations now depend on `interaction.port.InteractionPort`, and runners instantiate ports (e.g., `interaction.cli.TicTacToeCLIInteraction`) so the engine stays unaware of CLI details.
- Use `interaction/cli.py` (or future adapters) to adapt `ui.cli.tictactoe` helpers, show the board, and collect moves. Call `InteractionPort.show_result` after the match to centralize the final summary.
- Additional sequential games need only supply a state, a `Game`, optional interaction port, and plug them into a runner; the player types and shared bots reuse the existing engine and search modules.

## Example: Rock-Paper-Scissors

- `games/rps/game.py` implements `SimultaneousGame` so both `PLAYER_A` and `PLAYER_B` commit moves before the state updates.
- `runners/rps_bot_match.py` demonstrates hooking two random bots into the simultaneous runner and summarizing win/draw statistics.

## Event stream

- `core/events.py` defines `MatchEvent`, `TurnStarted`, `ActionTaken`, `MatchEnded`, and `EventBus`. Both `Match` and `SimultaneousMatch` publish these events, so observers can log, replay, or visualize matches without touching the deterministic engines.
- Use `interaction.terminal.TerminalLogger` or `interaction.web.SimpleWebBridge` (already wired into `runners/play.py`) as examples of event handlers; they subscribe to the bus automatically whenever you start a match through the runner.

Keep these conventions when adding more games or bots so the matchmaking and interaction code stays minimal.
