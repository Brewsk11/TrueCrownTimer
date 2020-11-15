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
* **Major flaw:** The timer's memory address (`ProcessMemoryReaders.py:83`) is hardcoded now and has to be extracted with external memory reader before use. This may possibly cause "error 299" while attaching to Spelunky 2 process. A solution for this is is development now.
  * **Workaround:** # TODO
* When enabling the timer during a level it doesn't take into account when the Crown was picked up.
  * **Workaround:** pick up the True Crown when it would normally teleport you, so it's in sync. The timer can help you with that if you enable it beforehand.
  * **Warning:** if you don't do the workaround in eg. in the City of Gold you'll have the timer desynced for the rest of the level with no option to resync. Next level it'll be in sync again.
* Attaching to Spelunky 2 can sometimes fail for no reason. It's caused by a wrong PID lookup.
  * **Workaround:** Just try attaching again.

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
