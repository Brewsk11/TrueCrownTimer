# True Crown timer for Spelunky 2

## `timer_mem.py`

A better version of the timer below that pulls the level timer directly from Spelunky 2 process memory. Much better, but still WIP.
Stay tuned for updates.

## `timer.py`

This is a timer for Spelunky 2 True Crown item. Features:
* runs a 22 seconds timer in a loop,
* plays a set sound `n` seconds before the timer expires (configurable),
* pauses the timer then `menu` button is pressed on an XInput controller,
* unpauses the timer then `confirm` button is pressed (user pressed continue in the menu),
* resyncing the timer with controller (for when changing levels),
* timer controls can be temprorarly disabled for menu browsing, without `Confirm` unpausing the timer.

### Installation

Tested with Python 3.8.2, so that's recommended, but latest should be good.
Please install Python with Python Launcher, pip, and "Add to PATH" enabled.
After Python is installed you have to install the requirements with pip: in a command line run `pip install -r requirements.txt` form the script directory.

### Usage

The first time you run the script it'll create a `settings.txt` file in the working directory, as well as run a button logging code. Now you need to identify button IDs for various script functions (more info inside the script).

After filling the `settings.txt` file run the scipt again and if it detects XInput controller the timer is started with the `confirm` button.

When the timer is running:
`menu` button pauses the timer until `confirm` isn't pressed again.
`resync` resets the timer to 22 seconds.
`disable` disables all buttons except `disable` until pressed again.

Press `resync` immediately when the level has been changed.

### Notes

Warning: this code is **heavily** spaghettified and isn't really readable, contains bugs with the time management and could be written 100x better, but I've made the thing in an hour so yeah.

Further work is planned to read the timer values directly from Spelunky 2 memory, instead of relying on user input.

### Known bugs

Please don't desync the timer when paused (I really meant **heavily** spaghettified).

### Credits
- `xinput.py`: https://github.com/r4dian/Xbox-Controller-for-Python
- `notification.mp3`: https://freesfx.co.uk/sfx/balloon-snap