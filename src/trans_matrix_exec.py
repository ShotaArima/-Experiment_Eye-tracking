from trans_matrix import compute_transition_matrix, compute_stay_time, run_clustering, plot_clusters
import pandas as pd
import os

df_all = []

for question in range(1, 5):
    for user in range(1, 10):
        csv_path =f'/output/all_users/pic-{question}/user-{user}_with_area_flg.csv'
        if not os.path.exists(csv_path):
            print("not csv file")
            continue
        df = pd.read_csv(csv_path)

        # 列名の空白を除去
        df.columns = df.columns.str.strip()

        # 安全確認
        if 'area_flg' not in df.columns:
            print(f"[スキップ] {csv_path} に area_flg が存在しません。列一覧: {df.columns.tolist()}")
            continue

        df = df[['Eyetracker timestamp', 'area_flg']]

        # 遷移行列
        trans_feat = compute_transition_matrix(df)
        stay_feat = compute_stay_time(df)

        metadata = {
            "user_id": f"user-{user}",
            "question_id": f"pic-{question}"
        }
        feature_row = {**metadata, **trans_feat, **stay_feat}
        df_all.append(feature_row)


# クラスタリングする関数
# 特徴量データフレーム化
df_input = pd.DataFrame(df_all)

# クラスタリング＋可視化
clustered_df = run_clustering(df_input)
save_path = f'/output/trans_matrix_clustering.png'
plot_clusters(clustered_df, path=save_path)

# CSV出力
clustered_df.to_csv("/output/trans_matrix.csv", index=False)