# walkbot

![Lua](https://img.shields.io/badge/Lua-5.1%2FLuaJIT-blue)
![Platform](https://img.shields.io/badge/Platform-fatality.win-red)
![Game](https://img.shields.io/badge/Game-CS2-orange)
![Mode](https://img.shields.io/badge/Launch-Insecure%20only-yellow)
![til]([https://raw.githubusercontent.com/hashrocket/hr-til/master/app/assets/images/banner.png](https://github.com/breakcoree/idk/blob/main/ezgif-8938751d8d1408ed.gif))
Navmesh-based walkbot with Auto-Queue and Auto-Team for the fatality.win CS2 Lua API. A\* pathfinding on custom `.txt` nav files, bhop/smooth-turn movement, Panorama JS matchmaking integration, and a full in-menu UI.

---

## 📑 Table of Contents

- [About](#-about)
- [Requirements](#-requirements)
- [Installation](#-installation)
- [Usage](#-usage)
- [UI Overview](#-ui-overview)
- [Nav File Format](#-nav-file-format)
- [Auto-Queue](#-auto-queue)
- [Auto-Team](#-auto-team)
- [Visuals](#-visuals)
- [Panorama Dump](#-panorama-dump)
- [Script Structure](#-script-structure)
- [Known Limitations](#-known-limitations)
- [License](#-license)

---

## 📋 About

This script provides:

- ✅ Navmesh-based pathfinding (A\* over custom `.txt` area files)
- ✅ Smooth or instant aim/turn toward the next waypoint
- ✅ Auto-jump for ledge climbing + bunny-hop (bhop)
- ✅ Stuck detection with random escape attempts
- ✅ Periodic path refresh and respawn/teleport recovery
- ✅ Auto-Queue via `LobbyAPI` Panorama JS (5 game modes, 17 map overrides)
- ✅ Auto-Team with configurable delay (CT / T / Random)
- ✅ 3D path and waypoint rendering (colors configurable in menu)
- ✅ On-screen HUD (nav file, path length, bot state)
- ✅ Panorama API dump tool (saves to file + clipboard)

---

## 🔧 Requirements

- **CS2** launched in **`-insecure`** mode (required for `utils.FileRead`, `utils.FileExists`, `panorama.Eval`)
- **fatality.win** is loaded
- Nav `.txt` files for the maps you want to walk (see [Nav File Format](#-nav-file-format))

---

## 🚀 Installation

```
1. Copy walkbot.lua to:
   game/csgo/fatality/scripts/walkbot.lua

2. Copy nav files to:
   game/csgo/fatality/nav/<mapname>.txt
   (e.g. de_dust2.txt, de_mirage.txt)

3. Launch CS2 with -insecure flag

4. Load the script via fatality.win script manager
```

---

## 📖 Usage

1. Open the fatality menu → **WalkBot** tab
2. Enable **WalkBot** in the Settings sub-tab
3. Join a map - the nav file for that map loads automatically
4. The bot starts pathing on the next `presentQueue` tick

To stop the bot: uncheck **Enable WalkBot**. On script unload `__shutdown()` is called automatically, which resets the bot state and stops Auto-Queue.

---

## 🖥️ UI Overview

The script adds a top-level tab **WalkBot** with three sub-tabs:

### Settings tab

| Control | Default | Description |
|---|---|---|
| Enable WalkBot | off | Master on/off |
| Waypoint Reach | 55 | 2D distance (units) to consider a waypoint reached |
| Stuck Timeout | 5.0 s | Seconds without progress before a stuck attempt |
| Auto Jump | on | Jump when a ledge is ahead (vert 18–60 u, dist < 90 u) |
| Bunny Hop | on | Hold IN_JUMP every grounded tick |
| Smooth Turn | on | Lerp view yaw toward waypoint instead of snapping |
| Turn Speed | 6.0 | Lerp factor (1–20); higher = faster turn |

### Queue tab

| Control | Default | Description |
|---|---|---|
| Enable Auto-Queue | off | Start/maintain matchmaking automatically |
| Game Mode | Competitive (Scrimmage) | One of 5 modes (see below) |
| Map Override | Default | Force a specific map group (17 options) |
| Re-Queue Delay | 10 s | Cooldown after a game ends before re-queuing |
| Status label | - | Live AQ state: Idle / Searching… Ns / In Game / Cooldown: Ns |
| Dump Panorama APIs | - | Enumerate available Panorama JS objects (debug) |

### Visuals tab

| Control | Default | Description |
|---|---|---|
| Draw Path | on | Lines between waypoints |
| Draw Waypoints | on | Circles at each waypoint |
| Draw HUD | on | Text overlay (nav, path count, state) |
| Path Color | blue-ish | Color of the path lines |
| Waypoint Color | yellow | Color of non-current waypoint circles |
| Current WP Color | green | Color of the next-target waypoint |

---

## 🗺️ Nav File Format

Plain text, one area per line. Lines starting with `#` are comments.

```
# id   cx      cy      cz      neighbor_id [neighbor_id ...]
1      512.0   -128.0  64.0    2 5 9
2      640.0   -128.0  64.0    1 3
...
```

| Column | Type | Description |
|---|---|---|
| `id` | integer | Unique area ID |
| `cx cy cz` | float | Area centroid (world units) |
| `neighbor_id ...` | integers | IDs of directly connected areas |

Nav files go in `game/csgo/fatality/nav/<mapname>.txt` where `<mapname>` matches the short map name returned by `game.globalVars.m_szMapName` (e.g. `de_dust2`).

---

## 🎮 Auto-Queue

Uses `LobbyAPI` via `panorama.Eval`. Requires `-insecure` and a real internet connection.

**State machine:**

```
IDLE ──► QUEUING ──► IN_GAME ──► COOLDOWN ──► IDLE
          │ (timeout 300s)                     ▲
          └────────────────────────────────────┘
```

**Supported game modes:**

| Index | Label | gtype | gmode | Default mapgroup |
|---|---|---|---|---|
| 0 | Competitive (Scrimmage) | classic | competitive | mg_active |
| 1 | Casual | classic | casual | mg_casualalpha |
| 2 | Deathmatch | gungame | deathmatch | mg_casualalpha |
| 3 | Wingman | classic | scrimcomp2v2 | mg_2v2active |
| 4 | Arms Race | skirmish | skirmish | mg_skirmish_armsrace |

**Map override** replaces the mode's default `mapgroupname` with a specific group (Dust 2, Mirage, Inferno, Nuke, Ancient, Anubis, Vertigo, Train, Overpass, Cache, Office, Italy, or pool groups).

If `LobbyAPI` is unavailable the script prints an error and retries after 5 seconds.

---

## 👥 Auto-Team

Independent of Auto-Queue - triggers on every server connect.

| Option | Behavior |
|---|---|
| Disabled | No team command sent |
| CT | `jointeam 3` after the configured delay |
| T | `jointeam 2` after the configured delay |
| Random | `jointeam 2` or `3` chosen at random |

**Pick Delay** (1–15 s, default 3 s) is measured from the moment `InGame()` transitions to `true`.

---

## 🎨 Visuals

While enabled, the script draws on `presentQueue`:

- **Red line** - player origin → current waypoint (always visible when a path exists)
- **Path lines** - full remaining path in the configured path color
- **Waypoint circles** - radius 3.5 u (non-current) or 6.0 u (current target)
- **HUD text** at screen position (10, 185):
  ```
  WalkBot  nav=de_dust2 (312)  path=18  state=Moving
  ```

---

## 🔍 Panorama Dump

The **Dump Panorama APIs** button enumerates these Panorama JS objects and saves the result:

`LobbyAPI`, `MatchmakingSearchService`, `GameInterfaceAPI`, `GameStateAPI`, `MyPersonaAPI`, `FriendsListAPI`, `InventoryAPI`, `SteamOverlayAPI`, `ContextMenuAPI`

Output goes to two places (whichever APIs are available):

- **File:** `game/csgo/fatality/aq_dump.txt`
- **Clipboard:** full dump text
- **Console:** first 400 characters as preview

Useful for debugging Auto-Queue issues or finding new Panorama endpoints.

---

## 📁 Script Structure

```
walkbot.lua
├── UI - tabs, groups, controls, default values
├── Math helpers - dist2/dist3, norm_yaw, lerp_angle, clamp
├── Nav system
│   ├── nav_load()       - parse .txt nav file on map change
│   ├── nav_nearest()    - closest area to a world position
│   └── nav_astar()      - A* pathfinder (max 5000 iterations)
├── Bot state machine - S_IDLE / S_MOVING / S_STUCK
├── Entity helpers - local_pawn, local_origin, pawn_on_ground, closest_enemy
├── events.createMove - movement, aiming, jump, waypoint advance, stuck escape
├── Auto-Queue
│   ├── AQ_MODE_CFG / AQ_MAP_GRP - mode/map tables
│   ├── aq_start()       - Panorama JS matchmaking call
│   └── AQ state machine - IDLE / QUEUING / IN_GAME / COOLDOWN
├── Auto-Team - aq_schedule_team_join / aq_maybe_join_team
├── events.presentQueue - AQ tick + path building + rendering
├── Panorama Dump - btn_dump callback
└── __shutdown()         - cleanup on script unload
```

---

## ⚠️ Known Limitations

- **Nav files are not included** - you need to generate or obtain `.txt` nav files for each map yourself
- **Auto-Queue requires Insecure mode** - `panorama.Eval` is unavailable in secure/VAC mode
- **`pcall` is not available** in the fatality Lua environment - all protected calls use `xpcall` with a `safe_call` wrapper or explicit nil-checks
- **Queue settings error** - if matchmaking rejects `UpdateSessionSettings`, check the dump output for the correct `mapgroupname` values for your CS2 build
- **Path refresh every 12 s** - intentional to recover from drift; will cause a brief `Idle` frame mid-navigation

---

## 📄 License

MIT - do whatever you want, no warranty.

---

---

## 📞 Contact

For questions and suggestions: [mail@gmail.com](mailto:mail@gmail.com)

Project Status: ✅ Completed  
Version: 1.3.5  
Last Updated: December 2026  
API: fatality.win Lua (CS2)  
Launch flag: `-insecure`
