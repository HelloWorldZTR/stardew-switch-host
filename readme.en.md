# Stardew Valley Multiplayer Save Host Swap

🌍 [English](readme.en.md) | 🇨🇳 [中文](readme.zh.md) 

## Usage

```sh
python main.py [path_to_your_save]
```

```
> python .\main.py .\farm_397798933
Stardew Valley Save File Host Swapper

---------Player List----------

Current Host User:
AAA @ FarmHouse (-445)

Other Users:
1. BBB @ FarmHousea490 (-816)
2. Host @ FarmHouse5e46 (7112)

Which player should be the host user?
Enter the index of the player: 2
```

Enter the corresponding number of the host user (e.g. 2)
The save file should be automatically updated, with the original file backed up to xxx.bak 

Save file location:
```
# Windows system
%APPDATA%\StardewValley\Saves\<name>_<number>
# Linux/MacOS
~/.config/StardewValley/Saves/<name>_<number>
```

For example: `C:\Users\hlwdztr\AppData\StardewValley\Saves\farm_397798933\farm_397798933`

## Use Cases

### Existing Multiplayer Save

If player A is currently hosting a multiplayer game with players B and C joining, but now they want B to host the server while A and C join the game.  
If B directly loads A's save file, he will be using A's character.

**Solution:**

Use the script to swap A and B.

### Hosting a Server using a Single-Player Save Without Losing Progress

Player A has a single-player save but wants to set up a server using mods like `Always On Server`.  
If A directly loads the existing save file, they won't be able to play as their own character.

**Solution:**

First, ask Robin to build at least two cabins, enable multiplayer mode, and create a new farmer (e.g., named "Host").  
Save the game.  
Use the script to swap A and "Host".  
Load the modified save onto the server. The server should now display the current user as "Host".

## Save File Structure

```XML
<?xml version="1.0" ?>
<SaveGame xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance">
    <player>
        ...
    </player>
    <farmhands>
        <Farmer>
            ...
            <homeLocation>FarmHouse5e468786-1057-41a1-9143-3ccffdc77907</homeLocation>
            <uniqueMultiplayerID>1122334455667788</uniqueMultiplayerID>
            ...
        </Farmer>
        <Farmer>
            ...
        </Farmer>
    </farmhands>
    <locations>
        <locations>
            <GameLocation xsi:type="Farm">
                <buildings>
                    <Building>
                        <indoors>
                            <farmhandReference>1122334455667788</farmhandReference>
                        </indoors>
                    </Building>
                </buildings>
            </GameLocation>
    </locations>
</SaveGame>
```

Although `player` and `Farmer` have different tags, they share the exact same structure and both represent "users".  
- `player` is the host and there is only one.  
- `Farmer` represents farmhands and there can be multiple.  
- The `Farmer` tags are created when cabins are built. There will be one `Farmer` tag per cabin.

Each user has a `homeLocation`:
- `FarmHouse` is the initial house.  
- Houses with suffixes are cabins for farmhands.  

Each user also has a `uniqueMultiplayerID`, which determines ownership of items (such as animals).

The `farmhandReference` in cabins corresponds to a specific user, determining whether a player owns a particular house and mailbox.  
If not modified, messages like "This is not your mailbox" will occur when you try to interact.