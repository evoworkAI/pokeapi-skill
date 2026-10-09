---
name: pokeapi
description: |
  用公开的 PokéAPI 查宝可梦图鉴、属性、中文名，并下载官方精灵图。
  当用户提到宝可梦、Pokémon、精灵图、图鉴、PokéAPI、皮卡丘或某只小精灵时使用。
  不需要 API Key。Look up Pokémon and download official sprites from PokéAPI.
---

# PokéAPI

公开接口，不用 Key。地址：`https://pokeapi.co/api/v2/`

脚本用 Node.js 运行，不要找 Python。这期已经装过 Node。需要 18 或更新的版本。

精灵图不要用绘图模型重画，用这里的官方图。这期片子用第三世代翡翠版。

## 查一只

在本 skill 目录执行。stdout 是 JSON，精灵图另存时会多打印绝对路径。

```bash
node scripts/poke.mjs pikachu
node scripts/poke.mjs 25 --out pikachu.png
node scripts/poke.mjs charizard --sprite default --out charizard.png
```

装到本机之后：

- `~/.claude/skills/pokeapi/scripts/poke.mjs`
- `~/.cursor/skills/pokeapi/scripts/poke.mjs`

`--sprite gen3` 是默认，第三世代翡翠正面图。`--sprite default` 是通用正面图。

名字用英文小写，中间有空格或点的写成连字符：`mr-mime`、`nidoran-f`。中文名不行，先用图鉴编号。

## 自己请求时

| 要什么 | 地址 |
| --- | --- |
| 编号、属性、种族值、技能 | `https://pokeapi.co/api/v2/pokemon/25` |
| 中文名、分类、进化链 | `https://pokeapi.co/api/v2/pokemon-species/25` |
| 第三世代精灵图 | `https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/versions/generation-iii/emerald/25.png` |

中文名在 species 的 `names` 里，`language.name` 为 `zh-hans`。

一次查一只或一小批。接口没有 Key，也不要并发猛刷。
