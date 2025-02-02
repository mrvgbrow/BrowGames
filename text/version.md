<h1>Version 1.12</h1>

<p>BrowGames is a collection of customizable classic games, all coded from scratch in Python. See The Retrogame Deconstruction Zone (https://www.retrogamedeconstructionzone.com) for details.</p>

<h2>New Features</h2>

<ul>
<li>Quadrapong: Added a Standard preset for games that aren't trying to mimic the original version.</li>
<li>Quadrapong: Added a parameter to adjust the size of the life counter.</li>
<li>Quadrapong: Added a parameter to set a maximum number of "dribbles" before the ball bounces in a random direction (this helps avoid infinite loops).</li>
<li>Space Race: Reverse Thrust option allows the ship to thrust backwards when gravity is on.</li>
</ul>
<h2>Bug Fixes</h2>
<ul>
<li>Quadrapong: "Ball Square" parameter wasn't working.</li>
</ul>

<h2>Improvements</h2>
<ul>
<li>Quadrapong: In the default preset, adjusting the layout and colors to more closely match original game.</li>
<li>Quadrapong: "Original Bounce" now fixes the X or Y speed depending on the paddle it is deflected from.</li>
<li>Quadrapong: Game now ends when one player remains.</li>
<li>Quadrapong: Reset the computer target ball when it hits a wall. </li>
<li>Quadrapong: Added special logic for impacts from the paddle side, to allow dribbling.</li>
<li>Quadrapong: Implemented fixed bounce angles of +-(0,30,45,60) when "Original Bounce" is on.</li>
</ul>

<h1>Version 1.11</h1>

<p>BrowGames is a collection of customizable classic games, all coded from scratch in Python. See The Retrogame Deconstruction Zone (https://www.retrogamedeconstructionzone.com) for details.</p>

<h2>New Features</h2>

<ul>
<li>Space Race: Added presets for gravity and animated sprites.</li>
<li>Space Race: Can optionally tell computer player to only move forward.</li>
<li>Quadrapong: Adding curved paddle option.</li>
</ul>
<h2>Bug Fixes</h2>
<ul>
<li>Space Race: Ship was resetting repeatedly in home position.
<li>Capitalize both letters in acronym "AI" in parameter names.</li>
<li>Off-by-one error in AI algorithm (currently just used in Space Race).</li>
</ul>

<h2>Improvements</h2>
<ul>
<li>Space Race: When gravity is on, limit computer player to speed specified in game parameters.</li>
</ul>

<h1>Version 1.1</h1>

<p>BrowGames is a collection of customizable classic games, all coded from scratch in Python. See The Retrogame Deconstruction Zone (https://www.retrogamedeconstructionzone.com) for details.</p>

<h2>New Features</h2>

<ul>
<li>Added Quadrapong as a playable game.</li>
<li>Space Race: Can specify a revive time for the ship after it's hit by an asteroid.</li>
<li>Space Race: Can optionally turn off the end-game message.</li>
<li>Pong: Can optionally turn off the end-game message.</li>
</ul>
<h2>Bug Fixes</h2>
<ul>
<li>Space Race: "Juiced Up" had the timer duration set too low, increased to one minute.</li>
</ul>

<h2>Improvements</h2>
<ul>
<li>Game parameters menus no longer display underscores in the parameter names.</li>
<li>After a game is finished, return to the game main menu rather than the main menu. Also, remembers the game parameters that were set during the last play.</li>
<li>X button in main menu closes the program. </li>
<li>X button in game menu returns to main menu. </li>
<li>Color submenus in game parameters menu are labelled with appropriate color (red, green, blue, or alpha).</li>
<li>Space Race: Improved tuning of "Original" preset to more closely resemble the original.</li>
</ul>

<h1>Version 1.0</h1>

<p>BrowGames is a collection of customizable classic games, all coded from scratch in Python. The original versions of most of these games are not playable in emulators because they had no CPU. In addition, BrowGames gives you the freedom to manipulate basic game parameters to see how it changes the gameplay.</p>
By default, BrowGames uses a parameter set that is very similar to the original game, but many other presets are available to experiment with. If you're interested in the historical context on the games included here, as well as details about their implementation, see The Retrogame Deconstruction Zone (https://www.retrogamedeconstructionzone.com).</p>

<p>Please note that not all combinations of parameters will be playable and some will even crash the game. However, BrowGames will revert to the default parameters when you restart, so don't be shy about breaking the game from time to time.</p>

<h2>New Features</h2>

<ul>
<li>Merged BrowPong v2.0 into a game package with a new game, called Space Race. The game package is called BrowGames.</li>
<li>Added a top-level menu from which games can be selected. Moved the About section to this menu and included sound/input/display settings at the top level.</li>
<li>Added Pong presets that correspond to the original <i>Pong Doubles</i>, Ramtek <i>Soccer</i>, and Bally's <i>Crazy Foot</i>.</li>
<li>In addition to a preset corresponding to the original <i>Space Race</i>, there is a "Juiced Up" version of the game available to play. The latter includes animation, power-ups, and gravity/thrusting physics.</li>
</ul>
<h2>Bug Fixes</h2>
<ul>
<li>Decreased font size in game parameters menu to remove horizontal scroll bar and avoid odd behavior when settings are clicked with a mouse.</li>
</ul>

<h2>Improvements</h2>
<ul>
<li>Added the Mr. Brow logo to the main menu and defined a new theme for the menus.</li>
<li>Moved the player control settings to the main menu.</li>
<li>Ending a game now brings the user back to the main menu rather than ending the program.</li>
<li>Screen height/width moved back to the game parameters menu.</li>
</ul>

