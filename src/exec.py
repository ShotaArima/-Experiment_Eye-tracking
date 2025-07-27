import argparse
import os
import pandas as pd
from gaze_plot_utils import (
    plot_gaze_trajectory_with_gradient,
    plot_gaze_heatmap,
    plot_gaze_heatmap_with_background,
    animate_gaze_plot_with_background
)

# -------------------------
# 1. 引数の処理
# -------------------------
print("start")
parser = argparse.ArgumentParser(description="Gaze Data Visualizer")
parser.add_argument('-user', type=int, required=True, help='User number')
parser.add_argument('-pic', type=int, required=True, help='Picture number')
args = parser.parse_args()

user = args.user
pic = args.pic

print("# 1. 引数の処理 Done")

# -------------------------
# 2. ファイルパス設定
# -------------------------
background_path_pic = f'/data/pic/視線誘導問題.00{pic}.jpeg'
if not os.path.exists(background_path_pic):
    raise FileNotFoundError(f"CSVファイルが見つかりません: {background_path_pic}")

csv_path = f'/data/user-{user}/user-{user}-pic-{pic}.csv'
if not os.path.exists(csv_path):
    raise FileNotFoundError(f"CSVファイルが見つかりません: {csv_path}")

save_dir = f"/output/user-{user}/pic-{pic}"
os.makedirs(save_dir, exist_ok=True)  # ディレクトリ作成
if not os.path.exists(save_dir):
    raise FileNotFoundError(f"CSVファイルが見つかりません: {save_dir}")




print("# 2. ファイルパス設定 Done")

# -------------------------
# 3. データ読み込み
# -------------------------
df = pd.read_csv(csv_path)

min_ts = df['Eyetracker timestamp'].min()
max_ts = df['Eyetracker timestamp'].max()

print(f"Min timestamp: {min_ts} microseconds")
print(f"Max timestamp: {max_ts} microseconds")
print(f"Diff timestamp: {max_ts - min_ts} microseconds")

sampling_intervals = df['Eyetracker timestamp'].diff().dropna()
print(f"Mean interval: {sampling_intervals.mean():.2f} µs")
print(f"Median interval: {sampling_intervals.median():.2f} µs")

print("3. データ読み込み Done")

# -------------------------
# 4. 使用するカラムを選択
# -------------------------
selected_columns = [
    'Eyetracker timestamp',
    'Gaze point X',
    'Gaze point Y',
    'Gaze point left X',
    'Gaze point left Y',
    'Gaze point right X',
    'Gaze point right Y',
    'Validity left',
    'Validity right'
]

df_selected = df[selected_columns]

print("4. 使用するカラムを選択 Done")

# 5. 折れ線グラフの描画
plot_gaze_trajectory_with_gradient(
    df=df_selected,
    x_col='Gaze point X',
    y_col='Gaze point Y',
    time_col='Eyetracker timestamp',
    screen_width=1920,
    screen_height=1080,
    title = 'Gaze Trajectory with Time Gradient',
    save_path = f"{save_dir}/trajectory_gradient.png"
    )

print("5. 折れ線グラフの描画 Done")

# 6. ヒートマップの作成
plot_gaze_heatmap(
    df=df_selected,
    x_col='Gaze point X',
    y_col='Gaze point Y',
    screen_width=1920,
    screen_height=1080,
    bins=(80, 45),  # 例: 24ピクセル単位
    title='Gaze Heatmap Only',
    save_path = f"{save_dir}/heatmap.png"
)

print("6. ヒートマップの作成 Done")

# 7. 背景つきヒートマップの作成
plot_gaze_heatmap_with_background(
    df=df_selected,
    background_path= background_path_pic, 
    x_col='Gaze point X',
    y_col='Gaze point Y',
    bins=(80, 45),
    title='Gaze Heatmap on Background',
    save_path = f"{save_dir}/heatmap_with_background.png"
)

print("7. 背景つきヒートマップの作成 Done")

# 8. 3倍スロー視線移動動画の生成
ani = animate_gaze_plot_with_background(
    df=df_selected,
    background_path = background_path_pic, 
    screen_width=1920,
    screen_height=1080,
    interval_ms=50,         # フレーム間隔（ms）
    trail_length=15,        # 履歴点数
    title='Animated Gaze Movement (slow)',
    save_path =  f"{save_dir}/animation_slow.mp4" 
)

print("8. 3倍スロー視線移動動画の生成 Done")

# 9. 30秒版の視線移動動画の生成
ani = animate_gaze_plot_with_background(
    df=df_selected,
    background_path = background_path_pic, 
    screen_width=1920,
    screen_height=1080,
    interval_ms=17,         # フレーム間隔（ms）
    trail_length=15,        # 履歴点数
    title='Animated Gaze Movement (60fps)',
    save_path =  f"{save_dir}/animation_60fps.mp4" 
)

print("9. 30秒版の視線移動動画の生成 Done")
print(f"user-{user}, pic-{pic} all finished")