#!/usr/bin/env bash
set -euo pipefail

proj_root="$(dirname "$0")"/..
proj_root="$(realpath "$proj_root")"  # 把项目根目录转为绝对路径

input_path="app.qrc"
output_path="app_rc.py"

rcc="$(realpath "$proj_root/.venv/bin/pyside6-rcc")"

resources_dir="$proj_root/src/resources"
cd "$resources_dir"
pwd
echo "$rcc" "$input_path" -o "$output_path"

"$rcc" "$input_path" -o "$output_path"
