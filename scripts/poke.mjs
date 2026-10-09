#!/usr/bin/env node
// 查 PokéAPI，并可选下载官方精灵图。不用 Key，也不用 Python。
//   node poke.mjs pikachu
//   node poke.mjs 25 --out pikachu.png

import fs from "node:fs"
import path from "node:path"

const API = "https://pokeapi.co/api/v2"
const SPRITES = {
  gen3: "https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/versions/generation-iii/emerald/{id}.png",
  default: "https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/{id}.png",
}

function die(message) {
  console.error(message)
  process.exit(1)
}

function parseArgv(argv) {
  const values = {}
  const positionals = []
  for (let i = 0; i < argv.length; i++) {
    const arg = argv[i]
    if (!arg.startsWith("--")) {
      positionals.push(arg)
      continue
    }
    const key = arg.slice(2)
    const next = argv[i + 1]
    if (next === undefined || next.startsWith("--")) die(`缺少参数：--${key}`)
    i += 1
    values[key] = next
  }
  return { values, positionals }
}

async function getJson(url) {
  let response
  try {
    response = await fetch(url, {
      headers: { "User-Agent": "pokeapi-skill", Accept: "application/json" },
      signal: AbortSignal.timeout(30000),
    })
  } catch (error) {
    die(`网络错误: ${error.message}`)
  }
  if (response.status === 404) die(`没找到：${url}\n名字用英文小写，比如 pikachu、mr-mime；或直接用图鉴编号。`)
  if (!response.ok) die(`HTTP ${response.status}\n${(await response.text()).slice(0, 500)}`)
  return response.json()
}

function chineseName(species) {
  for (const item of species.names || []) {
    if ((item.language?.name || "").toLowerCase() === "zh-hans") return item.name || ""
  }
  return ""
}

const { values, positionals } = parseArgv(process.argv.slice(2))
const name = positionals[0]
if (!name || values.help) {
  console.log("用法: node poke.mjs pikachu [--sprite gen3] [--out 文件.png]")
  process.exit(name ? 0 : 1)
}
const spriteSet = values.sprite || "gen3"
if (!SPRITES[spriteSet]) die("--sprite 只能是 gen3 或 default")

const key = name.trim().toLowerCase().replaceAll(" ", "-").replaceAll(".", "")
const pokemon = await getJson(`${API}/pokemon/${key}`)
const species = await getJson(pokemon.species.url)
const sprite = SPRITES[spriteSet].replace("{id}", String(pokemon.id))
console.log(JSON.stringify({
  id: pokemon.id,
  name: pokemon.name,
  name_zh: chineseName(species),
  types: (pokemon.types || []).map((slot) => slot.type.name),
  sprite,
  sprite_set: spriteSet,
}))

if (!values.out) process.exit(0)
let downloaded
try {
  downloaded = await fetch(sprite, {
    headers: { "User-Agent": "pokeapi-skill" },
    signal: AbortSignal.timeout(30000),
  })
} catch (error) {
  die(`精灵图下载失败: ${error.message}`)
}
if (!downloaded.ok) die(`精灵图下载失败 HTTP ${downloaded.status}: ${sprite}`)
const file = path.resolve(values.out)
fs.mkdirSync(path.dirname(file), { recursive: true })
fs.writeFileSync(file, Buffer.from(await downloaded.arrayBuffer()))
console.log(file)
