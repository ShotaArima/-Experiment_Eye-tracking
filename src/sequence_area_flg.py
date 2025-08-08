import matplotlib.pyplot as plt
import pandas as pd

def switch_category(category: int):
    if category == 1:
        category_order =  ["question_statement", "question_graph", "opt-1", "opt-2", "opt-3", "opt-4"]
    elif category == 2:
        category_order = ["question_statement", "question_graph", "opt-1", "opt-2", "opt-3", "opt-4"]
    elif category == 3:
        category_order = ["question_statement", "question_graph", "opt-1", "opt-2", "opt-3", "opt-4"]
    elif category == 4:
        category_order = ["question_statement", "question_graph", "opt", "opt-1", "opt-2", "opt-3", "opt-4", "opt-5", "opt-6"]
    return category_order

def plot_gaze_area_transition(df: pd.DataFrame,
                              category: int,
                              save_path: str,
                              time_col: str = 'Eyetracker timestamp',
                              x_col: str = 'Gaze point X',
                              y_col: str = 'Gaze point Y',
                              area_col: str = 'area_flg',
                              validity_left: str = 'Validity left',
                              validity_right: str = 'Validity right',
                              figsize=(12, 6)):
    """
    視線の時系列におけるAOI遷移を折れ線グラフで表示する関数

    Parameters
    ----------
    df : pd.DataFrame
        視線データ
    category_order : list
        AOIのカテゴリ順序（y軸の順序）
    time_col : str
        時刻カラム名
    area_col : str
        AOI列名
    validity_left : str
        左目のバリディティカラム
    validity_right : str
        右目のバリディティカラム
    figsize : tuple
        グラフサイズ
    """
    # 1. データのフィルタリング
    df_plot = df.copy()
    df_plot = df_plot[
        (df_plot[area_col] != 'Outside') &
        ~((df_plot[validity_left] != 'Valid') & (df_plot[validity_right] != 'Valid'))
    ]

    category_order = switch_category(category)

    # 2. カテゴリ順序を設定して数値に変換
    df_plot[area_col] = pd.Categorical(df_plot[area_col], categories=category_order, ordered=True)
    df_plot['area_code'] = df_plot[area_col].cat.codes

    # 3. 折れ線グラフ
    fig, ax = plt.subplots(figsize=figsize)
    ax.plot(df_plot[time_col] - df_plot[time_col].iloc[0], df_plot['area_code'], marker='o', markersize=2, linewidth=1)

    # 4. 軸ラベル・タイトル設定
    ax.set_yticks(range(len(category_order)))
    ax.set_yticklabels(category_order)
    ax.set_xlabel("Eyetracker timestamp (µs)")
    ax.set_ylabel("AOI Area")
    ax.set_title("Gaze Area Transition Over Time")

    ax.grid(axis='y', linestyle='--', alpha=0.5)

    if save_path:
        plt.savefig(save_path)
        plt.close()
    else:
        plt.slow()
