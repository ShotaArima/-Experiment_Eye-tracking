import pandas as pd
from sklearn.cluster import KMeans
from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler
import matplotlib.pyplot as plt
import seaborn as sns


def compute_transition_matrix(df: pd.DataFrame) -> dict:
    """area_flgの遷移回数を特徴量辞書として返す"""
    areas = df['area_flg'].astype(str).tolist()
    transitions = {}

    for a, b in zip(areas, areas[1:]):
        key = f"trans_{a}→{b}"
        transitions[key] = transitions.get(key, 0) + 1

    return transitions

def compute_stay_time(df: pd.DataFrame) -> dict:
    """同一area_flgの滞在時間を集計して特徴量辞書として返す"""
    df = df.copy()
    df['Eyetracker timestamp'] = pd.to_numeric(df['Eyetracker timestamp'], errors='coerce')
    df['time_diff'] = df['Eyetracker timestamp'].diff().fillna(0)

    # area_flgごとの時間を合算
    stay_time = df.groupby('area_flg')['time_diff'].sum().to_dict()

    # プレフィックスをつけて返す
    stay_time = {f"dur_{k}": v for k, v in stay_time.items()}
    return stay_time



def run_clustering(df: pd.DataFrame, n_clusters: int = 4) -> pd.DataFrame:
    feature_cols = [col for col in df.columns if col.startswith("trans_") or col.startswith("dur_")]
    X = df[feature_cols].fillna(0)  # 欠損0埋め

    # 正規化
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)

    # KMeansクラスタリング
    kmeans = KMeans(n_clusters=n_clusters, random_state=0, n_init='auto')
    df['cluster'] = kmeans.fit_predict(X_scaled)

    return df

# def plot_clusters(df: pd.DataFrame, path=None, topn: int = 3):

#     # 特徴量のみ抽出
#     feature_cols = [col for col in df.columns if col.startswith("trans_") or col.startswith("dur_")]
#     X = df[feature_cols].fillna(0)

#     # スケーリングとPCA
#     X_scaled = StandardScaler().fit_transform(X)
#     pca = PCA(n_components=2)
#     X_pca = pca.fit_transform(X_scaled)

#     # 主成分に寄与する特徴量（大きい順）
#     pc1_top = pd.Series(pca.components_[0], index=feature_cols).abs().sort_values(ascending=False).head(topn).index.tolist()
#     pc2_top = pd.Series(pca.components_[1], index=feature_cols).abs().sort_values(ascending=False).head(topn).index.tolist()

#     # 軸ラベルを生成（上位3個の特徴量名をカンマ区切りで）
#     pc1_label = "PC1: " + ", ".join(pc1_top)
#     pc2_label = "PC2: " + ", ".join(pc2_top)

#     # プロット
#     plt.figure(figsize=(8, 6))
#     scatter = plt.scatter(X_pca[:, 0], X_pca[:, 1], c=df['cluster'], cmap='tab10')
#     plt.title("Cluster Visualization (PCA)")
#     plt.xlabel(pc1_label)
#     plt.ylabel(pc2_label)
#     plt.colorbar(scatter, label="Cluster")
#     plt.grid(True)
#     plt.tight_layout()

#     if path:
#         plt.savefig(path)
#         plt.close()
#     else:
#         plt.show()

def plot_clusters(df: pd.DataFrame, path=None, topn: int = 5):

    feature_cols = [col for col in df.columns if col.startswith("trans_") or col.startswith("dur_")]
    X = df[feature_cols].fillna(0)

    # スケーリングとPCA
    X_scaled = StandardScaler().fit_transform(X)
    pca = PCA(n_components=2)
    X_pca = pca.fit_transform(X_scaled)

    # 成分ごとの寄与度
    pc1_series = pd.Series(pca.components_[0], index=feature_cols)
    pc2_series = pd.Series(pca.components_[1], index=feature_cols)

    # PC1とPC2で寄与度が高い上位特徴量を取得
    pc1_top = pc1_series.abs().sort_values(ascending=False).head(topn)
    pc2_top = pc2_series.abs().sort_values(ascending=False).head(topn)

    # 軸ラベル
    pc1_label = "PC1: " #+ ", ".join(pc1_top.index.tolist())
    pc2_label = "PC2: " #+ ", ".join(pc2_top.index.tolist())

    # --- プロット領域分割 ---
    fig, axes = plt.subplots(2, 2, figsize=(14, 10))

    # クラスタの散布図
    scatter = axes[0, 0].scatter(X_pca[:, 0], X_pca[:, 1], c=df['cluster'], cmap='tab10')
    axes[0, 0].set_title("Cluster Visualization (PCA)")
    axes[0, 0].set_xlabel(pc1_label)
    axes[0, 0].set_ylabel(pc2_label)
    axes[0, 0].grid(True)
    fig.colorbar(scatter, ax=axes[0, 0], label="Cluster")

    # PC1の寄与特徴量の棒グラフ
    sns.barplot(x=pc1_top.values, y=pc1_top.index, ax=axes[0, 1], orient='h', palette="Blues_r")
    axes[0, 1].set_title("Top Features for PC1")
    axes[0, 1].set_xlabel("Loading")

    # PC2の寄与特徴量の棒グラフ
    sns.barplot(x=pc2_top.values, y=pc2_top.index, ax=axes[1, 1], orient='h', palette="Greens_r")
    axes[1, 1].set_title("Top Features for PC2")
    axes[1, 1].set_xlabel("Loading")

    # 右下の余白は空白にする
    axes[1, 0].axis('off')

    plt.tight_layout()

    if path:
        plt.savefig(path)
        plt.close()
    else:
        plt.show()

