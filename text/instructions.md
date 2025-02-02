<h1>BrowGames Instructions</h1>

<p>BrowGames is a collection of customizable classic games, all coded from scratch in Python. The original versions of most of these games are not playable in emulators because they had no CPU. In addition, BrowGames gives you the freedom to manipulate basic game parameters to see how it changes the gameplay.</p>
By default, BrowGames will use a parameter set that is very similar to the original game, but many other presets are available to experiment with. For historical context on the games included here, as well as details about their implementation, see The Retrogame Deconstruction Zone (https://www.retrogamedeconstructionzone.com).</p>

<h2>Running from the Source Code</h2>
If you wish to run the program from the source code using a Python interpreter, you will need pygame and pygame_menu.

<h2>Controls</h2>

If the player control is set to "arrows", press the up arrow to move up and the down arrow to move down. If player control is set to "wasd", press w to move up and s to move down.
<br><br>
To reset the score, press the r key. 
<br><br>
To pause the game at any time, press the p key. While paused, you can step the game forward one frame at a time with the "]" key. To end the game, press Esc.

<h2>Main Menu</h2>

When you load BrowGames, you will  be greeted by the main menu
<ol>
<li>Select Game - Load a list of games that are playable in BrowGames.</li>
<li>Settings - Selecting this loads a submenu from which you can set display, sound, and input settings.</li>
<li>About - Displays some basic information about the game.</li>
</ol>

<h2>Game Menu</h2>

<p>After selecting a game in the main menu, you will see the game menu, in which there are several options:</p>
<ol>
<li>Play with Current Settings - As the name suggests, selecting this will play the game with whatever settings are currently loaded. If a preset is being used, it will be specified at the bottom of the menu.</li>
<li>Presets - Selecting this loads a submenu from which you can select certain presets. Selecting a preset will bring you back to the main menu, from which you can inspect the individual settings for that preset before playing.</li>
<li>Settings - Just as in the main menu, selecting this loads a submenu from which you can set display, sound, and input settings.</li>
<li>Game Parameters - Selecting this loads a submenu from which you can set individual game parameters within the game.</li>
<li>Quit - Close the menu and end the program.</li>
</ol>
<h2>Settings</h2>
<p>The settings can be adjusted from either the main menu or the game menu. These include things like the display, input, and sound.</p>
<ol>
<li>Fullscreen Mode - When set to On, the game will load in fullscreen mode (the menus remain windowed).</li>
<li>Sound volume - Volume of the sound effects, between 0 and 1.</li>
<li>Mouse Sensitivity - Sensitivity of the mouse input. Larger values are more sensitive.</li>
</ol>
<h2>Common Parameters</h2>
<p>The following parameters are common throughout the various BrowGames and will always have the same meaning.</p>
<ol>
<li>Screen Height - Height of the playing field in pixels.</li>
<li>Screen Width - Width of the playing field in pixels.</li>
<li>Font Size - Font size in points. Not all in-game messages have customizable sizes, but this typically controls the score display.</li>
<li>Colors - All colors are either three-element vectors of the form (Red, Green, Blue), or four-element vectors of the form (Red, Green, Blue, Alpha), where each element should be between 0 and 256. Colors are specified in a distinct submenu one level down from the game parameters menu.</li>
<li>X/Y Positions - Except where noted, positions are specified in fractions of the screen width (for x positions) or screen height (for y positions). Values should be between 0 and 1 and smaller values are towards the left/top.</li>
<li>Scales - The sizes of game objects will often (but not always) be specified as a scale, which represents a multiplicative scaling to the native sprite size. Integer values of these parameters will usually produce better looking sprites.</li>
<li>Tick Framerate - Frames per second.</li>
<li>Player [1-4] Control - The controls for player [1-4]. Can be "Arrows" (the arrow keys on the keyboard), "WASD" or "IJKL" (the corresponding letters on the keyboard), "Computer" for automatic control, or "None". When available, the "None" option removes the player from the game.</li>
<li>Show End Message - When set to On, a message will display at the end of the game indicating who won.</li>
</ol>
<h2>Pong</h2>
<p>The BrowGames version of Pong is actually multiple games in one program. Because many of the ball and paddle games that appeared in arcades in the early '70s (e.g., Pong, Pong Doubles, Pong Soccer) were so similar, I can reproduce them by simply altering the game parameters of the original <i>Pong</i>.</p>
<p>If you load a Pong variant from the main menu, it will take you to the Pong game menu with the appropriate parameters pre-loaded. All of the same parameters and presets are adjustable for Pong, Pong Doubles, etc.</p>
<h3>Presets</h3>
<ul>
<li>Standard - The standard game configuration.</li>
<li>Original - A game configured to closely resemble the original Atari coin-op.</li>
<li>Simple Bounce - The standard game with simple bounces (no dependence on where the ball hits the paddle).</li>
<li>Curved Paddle - Uses curved paddles instead of the usual flat ones, with corresponding change in bounce physics.</li>
<li>Room Single - A single ball boucing in an enclosed room (no paddles)</li>
<li>Room Many Balls - 100 balls boucing in an enclosed room (no paddles)</li>
<li>Computer No Mistakes - A game against a mistake-free computer player with no paddle offsets.</li>
<li>Computer Offset No Mistakes - A game against a mistake-free computer player with an offset that allows for high-angle shots.</li>
<li>Computer See No Bounces - A game against a computer player that does not account for bounces off the walls.</li>
<li>Doubles - A game configured to closely resemble the original <i>Pong Doubles</i> coin-op.</li>
<li>Pong Soccer - A game configured to closely resemble the original Ramtek <i>Soccer</i> coin-op.</li>
<li>Crazy Foot - A game configured to closely resemble the original Bally <i>Crazy Foot</i> coin-op. In this game, both paddles have full 2-D freedom to move.</li>
</ul>
<h3>Parameter Descriptions</h3>

<ul>
<li>Score Hide - If set to On, the score will not be displayed.</li>
<li>Score Max - The number of points scored by either player that will end the game.</li>
<li>Time Hide - If set to On, the game time elapse will not be displayed.</li>
<li>Center Line Hide - If set to False, there will be a white a dashed line marking the center of the court</li>
<li>Player Move Speed - Player movement speed in pixels per second.</li>
<li>Player [1-4] Paddle Type - The type of paddle used by player [1-4]. The options are "normal", "curved", and "split". The "curved" option enables special physics that cause the ball to move in response to the curvature of the paddle. The "split" separates the paddle into two parts that move together. </li>
<li>Player Width - The width of the paddles relative to the screen width (between 0 and 1)</li>
<li>Player Height - The height of the paddles relative to the screen height (between 0 and 1)</li>
<li>Paddle Allow Left Right - When set to On, the paddle can move left/right as well as up/down.</li>
<li>Player Control Factor - When "Original Bounce" is False, this factor determines how much additional deflection is given to the ball when it hits the sides of the paddles. No additional deflection is 0 and 0.5 is a moderate value.</li>
<li>Player Radius - Radius of curvature for the paddle in pixels. Only used when "Curved Paddle" is set to On.</li>
<li>Ball Square - When set to On, the ball will be a square instead of a circle.</li>
<li>Ball Number - Number of balls on the playing field to start the game.</li>
<li>Ball Speed Increase - Increase in ball speed with every paddle impact, in pixels per second.</li>
<li>Ball Max Speed - Maximum ball speed in pixels per second. </li>
<li>Ball Speed - Speed of the ball in pixels per second. When "Original Bounce" is On, this is the horizontal speed. When it's False, this is the total speed.</li>
<li>Ball Radius - Radius of the ball in pixels.</li>
<li>Ball Wait - The number of seconds to wait before a ball is served between points.</li>
<li>Ball Minangle - The minimum possible angle of motion (relative to vertical) for the ball in degrees. Only has an effect if "Original Bounce" is False.</li>
<li>Ball Fix X Speed - When set to On, fixes the x speed of the ball.</li>
<li>Wall Width - The width of the exterior wall as a fraction of the screen height.</li>
<li>Goal Size - The size of the openings on the side of the screen, relative to the screen height.</li>
<li>Show Ball Trail - When set to On, the ball's path will be traced as it moves. The path resets between points.</li>
<li>AI Predict Bounce - When On, the computer player will predict the impact of a wall bounce before it happens.</li>
<li>AI Error Distance - The AI will make random paddle placement errors, with a maximum error equal to this value times the length of the paddle. A smaller distance means a better AI.</li>
<li>AI Random Adjust - If non-zero, the AI will randomly adjust its position in this fraction of frames. More adjustments make the AI look more indecisive, but not actually worse.</li>
<li>AI Y-Speed Error Factor - This factor determines how much worse the AI gets as the ball vertical speed increases. A value of zero means the AI is insensitive to speed and a value of 1 is the default for standard one-player mode.</li>
<li>Discrete Steps - When this is On, the ball will only move in steps that are equal to an integer number of pixels.</li>
<li>Original Bounce - When set to On, the ball will bounce off the paddle at a fixed angle based on where it hits the paddle, similar to the original Pong. When set to False, the ball will bounce in a more realistic way (modified by the "Player control Factor").</li>
</ul>
<h2>Space Race</h2>
<p>Unlike <i>Pong</i>, there is only one original game included in the BrowGames Space Race program. There are still presets to choose from, but only one of them corresponds to a classic coin-op.</p>
<h3>Presets</h3>
<ul>
<li>Original - A reproduction of the original game.</li>
<li>Juiced Up - I have added a slew of features in an attempt to make the game more fun. This includes power-ups, gravity, animated sprites, and asteroid collision impulses.</li>
</ul>
<h3>Setting/Parameter Descriptions</h3>
<ul>
<li>Gravity - The acceleration due to gravity, in pixels per second squared. Set to zero for no gravity. If this value is larger than Player Acceleration, gravity will prevent the ship from moving.</li>
<li>Start Countdown - The initial countdown before the game begins.</li>
<li>Player Speed - The speed of the player when Gravity is set to 0, in pixels per second. When gravity is non-zero, this is the maximum speed a computer player will go.</li>
<li>Player Acceleration - The acceleration of the player when thrusters are active, in pixels per second squared. This value only applies when gravity is set greater than zero. If this value is lower than the acceleration due to gravity, the player won't be able to move.</li>
<li>Reverse Thrust - When set to On, the ship can thrust backwards as well as forwards (only works when gravity is on).</li>
<li>Player [1-2] Steps Anticipate - When the computer player is determining when to move, it will look this many steps ahead before doing so.</li>
<li>AI Forward Only - When set to On, the computer player will only move forward or remain still, never move backwards.</li>
<li>Player Collision Reset - When set to On, the player will return to their starting position when they hit an asteroid. When it's off, asteroid collisions will result in an impulse that reverses the player speed.</li>
<li>Player Animate - When set to On, the player sprite will be animated with thrusters and sometimes an invincibility sequence.</li>
<li>Player Anim Pace - When the player sprite is animated, this is the number of game frames between frames of animation.</li>
<li>Powerup Time - When the player collects a canister, they will be invincible for this amount of time, in seconds.</li>
<li>Timer Duration - The length of the game, in seconds.</li>
<li>Timer Top - The top of the timer, in fractions of the screen height. Zero means it starts at the top of the screen.</li>
<li>Timer Bottom - The bottom of the timer, in fractions of the screen height. </li>
<li>Timer Width - The width of the timer, in fractions of the screen width. </li>
<li>Asteroid Speed - The horizontal speed of the asteroids in pixels per second.</li>
<li>Asteroid Speed Spread - Randomizes the motion of the asteroids every time they reset. This is the spread in speeds that will result, in pixels per second. Set this to zero to keep the asteroid speeds the same.</li>
<li>Asteroid Horiztonal Impulse - When an asteroid strikes a player, you can add an impulse that changes the player's horizontal speed by the specified amount (in pixels per second). Set to zero for no impulse.</li>
<li>Asteroid Separation - The vertical separation, as a fraction of the screen height, between asteroids.</li>
<li>Asteroid Max Height - The maximum height of the asteroid field, as a fraction of the screen height. Smaller values will extend the field closer to the top.</li>
<li>Asteroid Old Type - When set to On, the asteroids will look like they did in the original <i>Space Race</i> (like dashes). Turn this off if you want sprites that look more like real asteroids.</li>
<li>Asteroid Revive Time - When asteroids leave the screen, they reappear on the other side after this amount of time. Times are specified in seconds.</li>
<li>Canister Speed - The speed of the powerup canisters, in pixels per second.</li>
<li>Canister Fraction - The fraction of the asteroid field that is randomly replaced by canisters, between 0 and 1.</li>
</ul>

<h2>Quadrapong</h2>
<p>The BrowGames version of Quadrapong is a distinct program from the other Pong variants because of the significant differences in the game geometry. </p>
<p>Despite that fact, many of the parameters in Quadrapong have the same meaning as in Pong, so check that section if a parameter is not listed here.</p>
<h3>Presets</h3>
<ul>
<li>Standard - The standard game configuration.</li>
</ul>
<h3>Parameter Descriptions</h3>

<ul>
<li>Screen Pad - The distance of the walls from the edge of the screen, as a fraction of the screen height.</li>
<li>Score Size - Size of the life counter relative to the screen height.</li>
<li>Lives Start - The initial number of lives that each player has. When these lives expire, the player is removed from the game.</li>
<li>Paddle Wall Offset - The offset between the paddle and the wall, as a fraction of the screen height.</li>
<li>Wall Length - The distance from the corner of a wall to the start of a player goal, as a fraction of the screen height.</li>
<li>AI Try All - When set to On, the computer player will try to hit a ball even if the paddle speed isn't enough to make it.</li>
<li>Paddle Max Dribble - Sets a maximum number of times the ball can bounce off the paddle side before it bounces at a random angle. This logic is intended to avoid infinite loops.</li>
</ul>
