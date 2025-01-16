<h1>Version 2.0</h1>

<p>This program is tunable version of the original Pong (1972). You can adjust the parameters (e.g., paddle size, ball speed) to change the game and experiment with different designs. It is a standalone executable so just remove the old version and replace it with this one.</p>

<p>Please note that not all combinations of parameters will be playable. However, the game will revert to the default parameters when you restart, so don't be shy about breaking it from time to time.</p>

<h2>New Features</h2>

<ul>
<li>Option to add up to four paddles at a time (including a 4-player option).</li>
<li>Mouse support.</li>
<li>Option to display the ball as a square instead of a circle.</li>
<li>A configurable maximum score that will end the game.</li>
<li>Choice to remove any paddle from the game. </li>
<li>Presets that correspond to Hockey and Crazy Foot coin-ops.</li>
<li>Optional IJKL keyboard controls.</li>
<li>Fullscreen mode.</li>
<li>Option to set a "split" paddle that amounts to two vertically separated paddles moving together.</li>
</ul>
<h2>Bug Fixes</h2>
<ul>
<li>Ball was bouncing backwards off the corners when the goal was full size. </li>
<li>Ball was getting removed before completely exiting the screen on the right.</li>
</ul>

<h2>Improvements</h2>
<ul>
<li>Moved the player control settings to the main menu.</li>
<li>Moved mouse, volume, and screen size settings to a separate menu from the game parameters.</li>
<li>Eliminated redundant presets that only changed the number of players.</li>
<li>The wait between serves was reduced to 2 seconds in standard 2-player mode.</li>
<li>Computer player will now move in full 2-D when left/right motion is enabled.</li>
<li>Appearance of Back and OK buttons now stands out from other menu options.</li>
<li>Sorted the parameters and presets menus alphabetically.</li>
<li>Made the original preset to be more like the original Pong.</li>
<li>Boundary enforcement for the left/right walls.</li>
<li>Distinct fonts for in-game messages and score.</li>
</ul>

<h1>Version 1.2</h1>


<h2>New Features</h2>

<ul>
<li>User can add a dashed center line to the court.</li>
<li>User can now add a wait to the serve between points.</li>
<li>User can optionally display the elapsed game time in the corner.</li>
<li>User can reset the game score with the r key.</li>
<li>Added the ability to reset the score with the r key.</li>
<li>Added an "About" section to the main menu, where you can view the game version and basic info.</li>
<li>Added walls to the edge of the playing field, including the option to have them extend up the sides to create a "goal".</li>
<li>User can set the paddle to move left/right as well as up/down.</li>
<li>User can request that the ball's horizontal speed remain fixed.</li>
<li>The score display now resembles the original Pong (thanks to "Pong Score Extended", https://fontstruct.com/fontstructions/show/2450791/).</li>
<li>The direction of the serve is now randomized whether it goes left or right rather than always going right.</li>
</ul>
<h2>Bug Fixes</h2>
<ul>
<li>Fixed a bug with the curved paddle that was sometimes causing a crash when the ball hit the edge of the curved paddle.</li>
<li>Curved paddle height was not being properly accounted for.</li>
<li>Minimum angle restrictions were not being enforced in some cases.</li>
<li>Initial serve could start with the ball inside of a wall.</li>
<li>Some parameters (including the volume) weren't adjustable in Settings because they were being treated as integers</li>
</ul>
<h2>Improvements</h2>
<ul>
<li>Improved the curved paddle AI and controls with the features already present with the regular paddle.</li>
<li>The ball speed now resets between points.</li>
<li>Never allow backwards bounce with curved paddle. </li>
</ul>

<h1>Version 1.1</h1>

<ul>
<li>Updated the AI to be more tunable, including an error rate that depends on ball speed.</li>
<li>Added "Original" presets to make BrowPong appear similar to the original Atari game.</li>
<li>Added the ability to reset the score with the r key.</li>
<li>Added the option for a 2-second wait before a ball is served.</li>
<li>Added the option for a center line to be drawn down the middle of the court.</li>
<li>Added an option to display the elapsed game duration in the upper right corner.</li>
<li>Added an option to trace the ball's path during a game.</li>
<li>Added presets demonstrating different AI settings.</li>
</ul>
<h2>Bug Fixes</h2>
<ul>
<li>Fixed an issue with the AI that was causing it to move to the top of the screen intermittently between hits.</li>
<li>Fixed an issue with the AI that was causing it to sometimes ignore the ball.</li>
</ul>
<h2>Improvements</h2>
<ul>
<li>Improved the layout of the settings sub-menu.</li>
</ul>
