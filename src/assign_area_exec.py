import argparse
import os
import pandas as pd
from gaze_plot_utils import (
    plot_gaze_heatmap_with_background,
)
from assign_area import (
    assign_area_flag
)
# 設定
all_users = [1, 2, 3, 4, 5, 6, 7, 8, 9]  # すべてのユーザID
all_pics = [1, 2, 3, 4]  # すべての問題番号

aoi_dict = {
    1: [
        {"name": "question_statement", "x": 0, "y": 790, "width": 1920, "height": 380},
        {"name": "question_graph", "x": 0, "y": 0, "width": 750, "height": 790},
        {"name": "opt-1", "x": 750, "y": 640, "width": 1170, "height": 150},
        {"name": "opt-2", "x": 750, "y": 490, "width": 1170, "height": 150},
        {"name": "opt-3", "x": 750, "y": 340, "width": 1170, "height": 150},
        {"name": "opt-4", "x": 750, "y": 190, "width": 1170, "height": 150},
    ],

    2: [
        {"name": "question_statement", "x": 0, "y": 800, "width": 1920, "height": 380},
        {"name": "question_graph", "x": 0, "y": 0, "width": 1000, "height": 800},
        {"name": "opt-1", "x": 1000, "y": 400, "width": 400, "height": 400},
        {"name": "opt-2", "x": 1400, "y": 400, "width": 520, "height": 400},
        {"name": "opt-3", "x": 1000, "y": 0, "width": 400, "height": 400},
        {"name": "opt-4", "x": 1400, "y": 0, "width": 520, "height": 400},
    ],

    3: [
        {"name": "question_statement", "x": 0, "y": 750, "width": 1920, "height": 330},
        {"name": "question_graph", "x": 0, "y": 0, "width": 1000, "height": 750},
        {"name": "opt-1", "x": 1000, "y": 580, "width": 920, "height": 170},
        {"name": "opt-2", "x": 1000, "y": 410, "width": 920, "height": 170},
        {"name": "opt-3", "x": 1000, "y": 240, "width": 920, "height": 170},
        {"name": "opt-4", "x": 1000, "y": 0, "width": 920, "height": 240},
    ],

    4: [
        {"name": "question_statement", "x": 0, "y": 780, "width": 1920, "height": 300},
        {"name": "question_graph", "x": 0, "y": 0, "width": 1140, "height": 780},
        {"name": "opt", "x": 1140, "y": 680, "width": 920, "height": 100},
        {"name": "opt-1", "x": 1140, "y": 580, "width": 920, "height": 100},
        {"name": "opt-2", "x": 1140, "y": 480, "width": 920, "height": 100},
        {"name": "opt-3", "x": 1140, "y": 380, "width": 920, "height": 100},
        {"name": "opt-4", "x": 1140, "y": 280, "width": 920, "height": 100},
        {"name": "opt-5", "x": 1140, "y": 180, "width": 920, "height": 100},
        {"name": "opt-6", "x": 1140, "y": 0, "width": 920, "height": 180},
    ]
}


# 手続き
for pic in all_pics:
    background_path_pic = f'/data/pic/視線誘導問題.00{pic}.jpeg'
    if not os.path.exists(background_path_pic):
        print(f"背景画像が見つかりません: {background_path_pic}")
        continue

    # 問題ごとの出力ディレクトリ
    save_dir = f"/output/all_users/"
    os.makedirs(save_dir, exist_ok=True)

    for user in all_users:
        csv_path = f'/data/user-{user}/user-{user}-pic-{pic}.csv'
        if not os.path.exists(csv_path):
            print(f"CSVファイルなし: {csv_path}")
            continue

        # データ読み込み
        df = pd.read_csv(csv_path)

        # 必要なカラムだけ抽出
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

        # 背景つきヒートマップ作成
        save_path = f"{save_dir}/user-{user}/pic-{pic}_heatmap_with_background.png"
        plot_gaze_heatmap_with_background(
            df=df_selected,
            background_path=background_path_pic,
            x_col='Gaze point X',
            y_col='Gaze point Y',
            bins=(80, 45),
            title='Gaze Heatmap on Background',
            save_path=f"{save_dir}_heatmap_with_background.png"
        )

        problem_num = pic  # 対象の問題番号
        df_selected = assign_area_flag(df_selected, aoi_dict[problem_num])
        df_selected.to_csv(f"{save_dir}/user-{user}/pic-{pic}_with_area_flg.csv", index=False)