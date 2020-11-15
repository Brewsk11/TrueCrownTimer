<img src="https://img.shields.io/badge/Compatible%20Spelunky%202%20version-1.16.1-blue"/>

# True Crown timer for Spelunky 2

A Qt based GUI True Crown timer for Spelunky 2.

## Features

- attaches to Spelunky 2 process to read the level timer directly from memory,
- because it reads the time from a process' memory it's invulnerable to pausing etc.,
- plays a notification sound at specified seconds before teleport,
- shows:
  - current level timer,
  - time until next teleport,
  - previous teleport time,
  - next teleport time,
  - progress bars that fill up with the time passed.

## Installation

1. Python 3.8.2 recommended, but it should work with the latest.
   I recommend installation with with Python Launcher enabled.

2. Install depencencies:
   ```bash
   pip install -r requirements_gui.txt
   ```

## Usage

1. Run `TrueCrownTimerGUI.py`
2. Run Spelunky 2
3. With Spelunky 2 running click "Attach to Spelunky 2"
4. If it says "Attached" continue to next step.
5. When you acquire the True Crown click "Toggle True Crown" button.
   This enables the counter and notifications every 22 level seconds (by default).
   **Important:** There are bugs and limitations, see [below](#known-bugs-and-workarounds).
6. Click the button again to disable the counter and notifications.

## Configuration

In the `QtCustom.py` file the class `MainWindow` contains some options:
| Option | Default value | Description |
|-|-|-|
| `CROWN_INTERVAL` | `22` | Interval at which the counter resets, in seconds. |
| `EMERGENCY_BAR_AT` | `3` | Time remaining to timeoff at which the big green progress bar starts filling up, in seconds. |
| `NOTIFY_AT` |  `[5, 2, 1, 0]` | A Python list that specifies seconds before countdown finish at which to play a notification sound. `5` means that as soon as level timer is at < 6 a notification will be played, so ~6 seconds before teleport. |
| `NOTIFICATION_FILE` | `"./notification.mp3"` | Path to the notification sound file. |

## Known bugs and workarounds
* When enabling the timer during a level it doesn't take into account when the Crown was picked up.
  **Workaround:** pick up the True Crown when it would normally teleport you, so it's in sync. The timer can help you with that if you enable it beforehand.
  **Warning:** if you don't do the workaround in eg. in the City of Gold you'll have the timer desynced for the rest of the level with no option to resync. Next level it'll be in sync again.
* Attaching to Spelunky 2 can sometimes fail for no reason. It's caused by a wrong PID lookup.
  **Workaround:** Just try attaching again.

## TODO

**Features:**
- show number of teleports that have occurred during current level and from the start of True Crown pickup,
- ghost timer with memory reading,
- checking if True Crown is acquired from the memory,
- settings accessible from GUI (now configurable through script),

**Improvements:**
- logic that checks if `n` seconds has passed in the countdown is wonky and needs a rework,
- rework the project structure; at this point it's a mess,

**Bugfixes:**
- all mentioned in [bugs section](#known-bugs-and-workarounds).

***

## Legacy documentation
To be discarded soon.

### `timer_mem.py`

A better version of the `timer.py` below that pulls the level timer directly from Spelunky 2 process memory.
This script only reads and shows the current time. It's been used for memory reading testing purposes only.

### `timer.py` (deprecated)

This is a timer for Spelunky 2 True Crown item. Features:
* runs a 22 seconds timer in a loop,
* plays a set sound `n` seconds before the timer expires (configurable),
* pauses the timer then `menu` button is pressed on an XInput controller,
* unpauses the timer then `confirm` button is pressed (user pressed continue in the menu),
* resyncing the timer with controller (for when changing levels),
* timer controls can be temprorarly disabled for menu browsing, without `Confirm` unpausing the timer.

#### Installation

Tested with Python 3.8.2, so that's recommended, but latest should be good.
Please install Python with Python Launcher, pip, and "Add to PATH" enabled.
After Python is installed you have to install the requirements with pip: in a command line run `pip install -r requirements.txt` form the script directory.

#### Usage

The first time you run the script it'll create a `settings.txt` file in the working directory, as well as run a button logging code. Now you need to identify button IDs for various script functions (more info inside the script).

After filling the `settings.txt` file run the scipt again and if it detects XInput controller the timer is started with the `confirm` button.

When the timer is running:
`menu` button pauses the timer until `confirm` isn't pressed again.
`resync` resets the timer to 22 seconds.
`disable` disables all buttons except `disable` until pressed again.

Press `resync` immediately when the level has been changed.

#### Notes

Warning: this code is **heavily** spaghettified and isn't really readable, contains bugs with the time management and could be written 100x better, but I've made the thing in an hour so yeah.

Further work is planned to read the timer values directly from Spelunky 2 memory, instead of relying on user input.

#### Known bugs

Please don't desync the timer when paused (I really meant **heavily** spaghettified).

### Credits
- `xinput.py`: https://github.com/r4dian/Xbox-Controller-for-Python
- `notification.mp3`: https://freesfx.co.uk/sfx/balloon-snap