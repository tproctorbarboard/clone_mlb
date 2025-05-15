# MLB-StatsAPI

Python wrapper for MLB Stats API

Created by Todd Roberts

https://pypi.org/project/MLB-StatsAPI/

Issues: https://github.com/toddrob99/MLB-StatsAPI/issues

Wiki/Documentation: https://github.com/toddrob99/MLB-StatsAPI/wiki

## Copyright Notice

This package and its author are not affiliated with MLB or any MLB team. This API wrapper interfaces with MLB's Stats API. Use of MLB data is subject to the notice posted at http://gdx.mlb.com/components/copyright.txt.


- Tim's edits: run `generate_trivia_from_game.py` to run the trivia generator for a specified `gamePk`.

    - You can find a list of `gamePk`s using the following endpoint:  
      `https://statsapi.mlb.com/api/v1/schedule?sportId=1&date=2025-05-15`  
      *(Replace the date with the desired game day)*

- The `odds` folder contains packages for the **player-prop prediction game**, which can be run using:

    - `run_live_game.py` or  
    - `run_odds.py`  
      
      The `run_odds.py` is primarily intended for the Sunday Night Baseball "big" fixture, whereas `run_live_game.py` can be used for any live game.

- `generate_gemini_trivia.py` is the core logic behind prompt generation and generating plausible dummy answers from the AI.

- Most other files are outdated or test files that should be cleaned and organized accordingly.
