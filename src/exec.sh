#!/bin/bash
# 権限付与 chmod +x exec.sh
# exec.sh - 全ユーザー × ピクチャー 組合せを実行

for user in {1..9}; do
  for pic in {1..4}; do
    echo "Running for user=${user}, pic=${pic}..."
    uv run gaze_plot_utils_exec.py-user=${user} -pic=${pic}
    echo "Finished for user=${user}, pic=${pic}"
    echo "-----------------------------"
  done
done
