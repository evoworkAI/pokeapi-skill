#!/usr/bin/env bash
# PokéAPI skill。公开接口，不用 Key。
#
# 在懒人包目录执行：
#   bash pokeapi/install.sh

set -euo pipefail

SKILL_NAME="pokeapi"
SRC="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
FILES=(SKILL.md scripts)

copy_into() {
  local dst="$1"
  mkdir -p "$dst"
  local f
  for f in "${FILES[@]}"; do
    rm -rf "${dst:?}/$f"
    cp -R "$SRC/$f" "$dst/"
  done
  echo "已安装 → $dst"
}

echo "安装 PokéAPI skill"
copy_into "$HOME/.claude/skills/$SKILL_NAME"
copy_into "$HOME/.cursor/skills/$SKILL_NAME"

if [ "$PWD" != "$SRC" ]; then
  copy_into "$PWD/.claude/skills/$SKILL_NAME"
  copy_into "$PWD/.cursor/skills/$SKILL_NAME"
fi

echo
echo "不用填 Key。试一下："
echo "  python3 ~/.claude/skills/$SKILL_NAME/scripts/poke.py pikachu"
