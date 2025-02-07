# 星露谷联机存档服主转换

🌍 [English](readme.en.md) | 🇨🇳 [中文](readme.zh.md) 

## 使用方法

```sh
python main.py [path_to_your_save]
```

```
> python .\main.py .\farm_397798933
Stardew Valley Save File Host Swapper

---------Player List----------

Current Host User:
好名字 @ FarmHouse (-445)

Other Users:
1. 大萝卜 @ FarmHousea490 (-816)
2. 服主 @ FarmHouse5e46 (7112)

Which player should be the host user?
Enter the index of the player: 2
```

输入新服主对应的序号。存档内容应更新，原始存档被保存在.bak后缀文件里。

存档的位置
```
# Windows系统
%APPDATA%\StardewValley\Saves\<name>_<number>\<name>_<number>
# Linux/MacOS
~/.config/StardewValley/Saves/<name>_<number>/<name>_<number>
```

形如 C:\Users\hlwdztr\AppData\StardewValley\Saves\farm_397798933\farm_397798933

## 使用场景

### 已有联机存档

如果现在 A 开了多人游戏，B，C 加入了游戏。现在想换 B 开服务器，A，C 加入游戏。
如果直接加载 A 的存档，那么 B 玩的是 A 的角色。

解决方案：

用脚本交换 A 和 B

### 单人存档开设服务器，但不想丢失当前人物的进度

A 有一个单人存档，但他想用 `Always On Server` 等 Mod 架设服务器。
如果直接加载现有存档，A 的角色就不能游玩了。

解决方案：

先找罗宾修建至少两个联机小屋，打开联机模式，创建一个新农夫（比如叫“服主”）。
保存存档
用脚本交换 A 和 服主
将新存档加载到服务器,这时候服务器应当显示当前用户为“服主”。

## 存档结构

`player` 和 `Farmer` 虽然标签不同，但是结构完全一致，都是“用户”
`player` 是服主，只有一个；`Farmer` 可以有多个
注意这里的 `Farmer` 标签是随着联机小屋生成的，有几个小屋就有几个`Farmer`标签

每个用户都有一个 `homeLocation`, 其中 `FarmHouse` 是初始屋子，带后缀的是联机小屋。
每个用户都有一个 `uniqueMultiplayerID，` 用于确定物品的归属（比如动物）。

联机小屋的 `farmhandReference` 与用户存在一对一关系，用于判断这是不是你的房子和信箱。
如果没修改，则会显示“这不是你的信箱”，“你不能移动别的玩家屋里的床”等等。

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