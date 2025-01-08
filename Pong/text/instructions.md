<h1>BROWPONG GAME INSTRUCTIONS</h1>

<p>This program is tunable version of the original Pong (1972). You can adjust the parameters (e.g., paddle size, ball speed) to change the game and experiment with different designs.</p>

<p>Please note that not all combinations of parameters will be playable and some will even crash the game. However, it will revert to the default parameters when you restart, so don't be shy about breaking the game from time to time.</p>

<h2>CONTROLS</h2>

If the player control is set to "arrows", press the up arrow to move the paddle and the down arrow to move it down. If player control is set to "wasd", press w to move the paddle up and s to move it down.
<br><br>
To reset the score, press the r key. 
<br><br>
To pause the game at any time, press the p key. While paused, you can step the game forward one frame at a time with the "]" key. To end the game, press Esc.
<br><br>
If PADDLE_ALLOW_LEFTRIGHT is set to True, you can use the left/right arrows a/d keys to move the paddle.

<h2>MAIN MENU</h2>

<p>When you load the game, you will see the main menu, in which there are several options:</p>
<ol>
<li>Play with Current Settings - As the name suggests, selecting this will play the game with whatever settings are currently loaded. If a preset is being used, it will be specified at the bottom of the menu.</li>
<li>One-Player Standard - Play the standard 1P game.</li>
<li>Two-Player Standard - Play the standard 2P game.</li>
<li>Computer - Watch the AI compete against itself.</li>
<li>Presets - Selecting this loads a submenu from which you can select certain presets. Selecting a preset will bring you back to the main menu, from which you can inspect the individual settings for that preset before playing.</li>
<li>Settings - Selecting this loads a submenu from which you can set individual parameters within the game.</li>
<li>Quit - Close the menu and end the program.</li>
</ol>
<h2>PRESETS</h2>
<ul>
<li>Room Single - A single ball boucing in an enclosed room (no paddles)</li>
<li>Room Many Balls - 100 balls boucing in an enclosed room (no paddles)</li>
<li>One Player Standard - The standard one-player game (also accessible from the main menu).</li>
<li>Two Player Standard - The standard two-player game (also accessible from the main menu).</li>
<li>Zero Player Standard - The standard game with two computer players (also accessible from the main menu as Computer Only).</li>
<li>Zero Player Curved - Watch two computers play with curved paddles.</li>
<li>One Player Curved - One-player game with curved paddles.</li>
<li>Two Player Curved - Two-player game with curved paddles.</li>
<li>One Player Computer Offset No Mistakes - A one-player game against a mistake-free computer player with an offset that allows for high-angle shots.</li>
<li>One Player Original - A one-player game configured to closely resemble the original Atari game.</li>
<li>Two Player Original - A two-player game configured to closely resemble the original Atari game.</li>
<li>Two Player Simple Bounce - The standard two-player game with simple bounces (no dependence on where it hits the paddle).</li>
</ul>
<h2>PARAMETER DESCRIPTIONS</h2>

<p>- All x positions increases to the right and y positions increases down. All colors are three-element vectors of the form (Red, Green, Blue), where each element is between 0 and 256.</p>
<ul>
<li>Screen Height - Height of the playing field in pixels.</li>
<li>Screen Width - Width of the playing field in pixels.</li>
<li>Font Size - Font size in points. Only used for the score display.</li>
<li>Screen Color - The background color of the playing field </li>
<li>Sound volume - Volume of the sound effects, between 0 and 1.</li>
<li>Tick Framerate - Frames per second.</li>
<li>Score Y Position - Y position of the score display as a fraction of the screen height (smaller values towards the top).</li>
<li>Score Hide - If set to True, the score will not be displayed.</li>
<li>Time Hide - If set to True, the game time elapse will not be displayed.</li>
<li>Center Line Hide - If set to False, there will be a white a dashed line marking the center of the court</li>
<li>Player Move Speed - Player movement speed in pixels per second.</li>
<li>Player 1 Control - The controls for player 1. Can be "arrows" (the arrow keys on the keyboard), "wasd" (the corresponding letters on the keyboard), or "computer" for automatic control.</li>
<li>Player 2 Control - The controls for player 2. </li>
<li>Player 1 X Position - The horizontal position of player 1 relative to the screen width (between 0 and 1).</li>
<li>Player 2 X Position - The horizontal position of player 2 relative to the screen width (between 0 and 1).</li>
<li>Player Width - The width of the paddles relative to the screen width (between 0 and 1)</li>
<li>Player Height - The height of the paddles relative to the screen height (between 0 and 1)</li>
<li>Paddle Allow Left Right - When set to True, the paddle can move left/right as well as up/down.</li>
<li>Player 1 Color - The color of player 1's paddle.</li>
<li>Player 2 Color - The color of player 2's paddle.</li>
<li>Player Control Factor - When "Original Bounce" is False, this factor determines how much additional deflection is given to the ball when it hits the sides of the paddles. No additional deflection is 0 and 0.5 is a moderate value.</li>
<li>Curved Paddle - If set to True, a curved paddle will be used in place of the normal pong paddle. This also enables special physics that cause the ball to move in response to the curvature of the paddle.</li>
<li>Player Radius - Radius of curvature for the paddle in pixels. Only used when "Curved Paddle" is set to True.</li>
<li>Ball Number - Number of balls on the playing field to start the game.</li>
<li>Ball Speed Increase - Increase in ball speed with every paddle impact, in pixels per second.</li>
<li>Ball Max Speed - Maximum ball speed in pixels per second. </li>
<li>Ball Speed - Speed of the ball in pixels per second. When "Original Bounce" is True, this is the horizontal speed. When it's False, this is the total speed.</li>
<li>Ball Radius - Radius of the ball in pixels.</li>
<li>Ball Color - Color of the ball</li>
<li>Ball Wait - The number of seconds to wait before a ball is served between points.</li>
<li>Ball Minangle - The minimum possible angle of motion (relative to vertical) for the ball in degrees. Only has an effect if "Original Bounce" is False.</li>
<li>Ball Fix X Speed - When set to True, fixes the x speed of the ball.</li>
<li>Wall Width - The width of the exterior wall as a fraction of the screen height.</li>
<li>Wall Color - The color of the exterior wall.</li>
<li>Goal Size - The size of the openings on the side of the screen, relative to the screen height.</li>
<li>Show Ball Trail - When set to True, the ball's path will be traced as it moves. The path resets between points.</li>
<li>AI Predict Bounce - When True, the computer player will predict the impact of a wall bounce before it happens.</li>
<li>AI Error Distance - The AI will make random paddle placement errors, with a maximum error equal to this value times the length of the paddle. A smaller distance means a better AI.</li>
<li>AI Random Adjust - If non-zero, the AI will randomly adjust its position in this fraction of frames. More adjustments make the AI look more indecisive, but not actually worse.</li>
<li>AI Y-Speed Error Factor - This factor determines how much worse the AI gets as the ball vertical speed increases. A value of zero means the AI is insensitive to speed and a value of 1 is the default for standard one-player mode.</li>
<li>Discrete Steps - When this is True, the ball will only move in steps that are equal to an integer number of pixels.</li>
<li>Original Bounce - When set to True, the ball will bounce off the paddle at a fixed angle based on where it hits the paddle, similar to the original Pong. When set to False, the ball will bounce in a more realistic way (modified by the "Player control Factor").</li>
</ul>
<h2>Running from the Source Code</h2>
If you wish to run the program from the source code using a Python interpreter, you will need pygame and pygame_menu.
