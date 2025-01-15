<h1>BrowSpaceRace Game Instructions</h1>

<p>This program is tunable version of the original Space Race (1973). You can adjust the parameters (e.g., ship size, asteroid density) to change the game and experiment with different designs.</p>

<p>Please note that not all combinations of parameters will be playable and some will even crash the game. However, it will revert to the default parameters when you restart, so don't be shy about breaking the game from time to time.</p>

<h2>Controls</h2>

If the player control is set to "arrows", press the up arrow to move up and the down arrow to move down. If player control is set to "wasd", press w to move up and s to move down.
<br><br>
To reset the score, press the r key. 
<br><br>
To pause the game at any time, press the p key. While paused, you can step the game forward one frame at a time with the "]" key. To end the game, press Esc.

<h2>Main Menu</h2>

<p>When you load the game, you will see the main menu, in which there are several options:</p>
<ol>
<li>Play with Current Settings - As the name suggests, selecting this will play the game with whatever settings are currently loaded. If a preset is being used, it will be specified at the bottom of the menu.</li>
<li>Presets - Selecting this loads a submenu from which you can select certain presets. Selecting a preset will bring you back to the main menu, from which you can inspect the individual settings for that preset before playing.</li>
<li>Settings - Selecting this loads a submenu from which you can set display, sound, and input settings.</li>
<li>Game Parameters - Selecting this loads a submenu from which you can set individual game parameters within the game.</li>
<li>About - Displays some basic information about the game.</li>
<li>Quit - Close the menu and end the program.</li>
</ol>
<h2>Presets</h2>
<ul>
<li>Standard - The standard game configuration.</li>
<li>Original - A game configured to closely resemble the original Atari coin-op.</li>
</ul>
<h2>Setting/Parameter Descriptions</h2>

<p>- All x positions increases to the right and y positions increases down. All colors are three-element vectors of the form (Red, Green, Blue), where each element is between 0 and 256.</p>
<ul>
<li>Screen Height - Height of the playing field in pixels.</li>
<li>Screen Width - Width of the playing field in pixels.</li>
<li>Sound volume - Volume of the sound effects, between 0 and 1.</li>
<li>Mouse Sensitivity - Sensitivity of the mouse input. Larger values are more sensitive.</li>
<li>Fullscreen Mode - When turned on, the game will go to fullscreen mode once the menu is exited.</li>
<li>Font Size - Font size in points. Only used for the score display.</li>
<li>Screen Color - The background color of the playing field </li>
<li>Tick Framerate - Frames per second.</li>
<li>Score Y Position - Y position of the score display as a fraction of the screen height (smaller values towards the top).</li>
<li>Score Hide - If set to On, the score will not be displayed.</li>
<li>Score Max - The number of points scored by either player that will end the game.</li>
<li>Time Hide - If set to On, the game time elapse will not be displayed.</li>
<li>Player Move Speed - Player movement speed in pixels per second.</li>
<li>Player [1-2] Control - The controls for player [1-4]. Can be "arrows" (the arrow keys on the keyboard), "wasd" (the corresponding letters on the keyboard), or "computer" for automatic control.</li>
<li>Player [1-2] X Position - The horizontal position of player [1-4] relative to the screen width (between 0 and 1).</li>
<li>Player [1-2] Color - The color of player [1-4]'s paddle.</li>
<li>Player Width - The width of the paddles relative to the screen width (between 0 and 1)</li>
<li>Player Height - The height of the paddles relative to the screen height (between 0 and 1)</li>
</ul>
<h2>Running from the Source Code</h2>
If you wish to run the program from the source code using a Python interpreter, you will need pygame and pygame_menu.
