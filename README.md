<div align="center">
  <p>
    <a href="#"><img src="https://i.imgur.com/XtHuH2j.png" width="964" height="478" alt="screenshot" /></a>
  </p>
</div>

## General info
This is a keyboard layout visualizer for ZSA Moonlander keyboard (because I didn't find their Oryx or their training tool particularly useful). Layout information is created and updated manually in a TXT file (e.g. no automation of any kind, it doesn't read layouts from the keyboard itself, from Oryx, etc.) The intended usage is to keep it open somewhere in the corner of the screen while memorizing the layouts by typing and practicing.
## Requirements

`Python 3.x`
`wxPython` (`pip install wxpython`)

## Usage

Run `layout.pyw`, it reads layouts information from `all_layouts.txt`

## Layouts format

For each tab in the visualizer (the names can be anything):
```
SET name

...

END
```
The content of a set consists of one or more subsets, for example:
```
SUBSET normal
20 20
0 0 127
| Esc |  1  |  2  |  3  |  4  |  5  |  !  |-----|  '  |  6  |  7  |  8  |  9  |  0  |  -  |
| Prt |  Q  |  W  |  E  |  R  |  T  |  /  |-----|  .  |  Y  |  U  |  I  |  O  |  P  |     |
|  ⇧  |  A  |  S  |  D  |  F  |  G  |  \  |-----|  ,  |  H  |  J  |  K  |  L  |     |     |
|  ⇫  |  Z  |  X  |  C  |  V  |  B  |-----------------|  N  |  M  |     |     |     |  ⇫  |
|LCtrl|LAlt |     |LAlt |LCtrl|-----------------------------|  ▲  |  ▼  |RAlt |RCtrl|Ru/En|

------------------------| Win |-----------------------------|  ⏎  |------------------------
------------------------|  ⎵  | Tab |     |-----|     | Del |  ⌫  |------------------------

SUBSET symbols
10 2
220 128 0
|  +  | F1  | F2  | F3  | F4  | F5  |  *  |-----|     | F6  | F7  | F8  | F9  | F10 | F11 |
|  -  |  !  |  @  |  {  |  }  |  |  |     |-----|     |PgUp |Home |  ▲  | End |     | F12 |
|  =  |  #  |  $  |  (  |  )  |  `  |     |-----|     |PgDn |  ◀  |  ▼  |  ▶  |     | Ins |
|     |  %  |  &  |  [  |  ]  |  ~  |-----------------|     |     |     |     |     |     |
|     |     |  ^  |  <  |  >  |-----------------------------|     |     |     |     |     |

------------------------|     |-----------------------------|     |------------------------
------------------------|     |     | ⟲SYM|-----| ⟲SYM|     |     |------------------------
```
The second line represents where each key description is drawn, relative to the key's upper left corner. 

The third line represents the RGB color of the key descriptions (decimal numbers in range 0~255).

The rest is this rigid 'matrix', each 'key' is 5 characters wide (if less than 5, should be padded with spaces), separated with vertical bars. Empty keys should be 5 spaces. The long sequences of `-` characters should be where they are.

Subsets are read from top to bottom of the file, if a key description in a 'lower' subset is identical to the key description in a 'higher' subset, the 'lower' one is ignored (e.g. not displayed again, possibly at different coordinates and in a different color).

Sets support a primitive form of 'inheritance': `SET name2:name1` (`name1` should be defined before `name2`). If both sets have subsets with the same name (say, `symbols`), and `name2` had empty keys on its `symbols` subset, the key description from the set `name1` subset `symbols` will be displayed for that key instead.