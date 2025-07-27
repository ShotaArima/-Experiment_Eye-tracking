import matplotlib.animation as animation
import matplotlib.pyplot as plt
from matplotlib.collections import LineCollection
from matplotlib.colors import Normalize
import matplotlib.cm as cm
import matplotlib.image as mpimg
import numpy as np
import pandas as pd

def plot_gaze_trajectory_with_gradient(
        df, 
        x_col='Gaze point X', 
        y_col='Gaze point Y', 
        time_col='Eyetracker timestamp',
        screen_width=1920, 
        screen_height=1080, 
        title='Gaze Trajectory with Time Gradient', 
        save_path = None
    ):
    
    df_clean = df[[x_col, y_col, time_col]].dropna().copy()
    df_clean['time_sec'] = (df_clean[time_col] - df_clean[time_col].min()) / 1_000_000
    df_clean = df_clean.sort_values('time_sec')

    x = df_clean[x_col].values
    y = df_clean[y_col].values
    t = df_clean['time_sec'].values

    points = np.array([x, y]).T.reshape(-1, 1, 2)
    segments = np.concatenate([points[:-1], points[1:]], axis=1)

    norm = Normalize(vmin=t.min(), vmax=t.max())
    cmap = cm.get_cmap('plasma')
    lc = LineCollection(segments, cmap=cmap, norm=norm)
    lc.set_array(t[:-1])
    lc.set_linewidth(2)

    plt.figure(figsize=(10, 6))
    plt.gca().add_collection(lc)
    plt.xlim(0, screen_width)
    plt.ylim(screen_height, 0)
    plt.xlabel(x_col)
    plt.ylabel(y_col)
    plt.title(title)
    plt.colorbar(lc, label='Time (s)')
    plt.grid(True)
    plt.tight_layout()

    if save_path:
        plt.savefig(save_path)
        plt.close()
    else:
        plt.slow()

def plot_gaze_heatmap(
        df, 
        x_col='Gaze point X', 
        y_col='Gaze point Y', 
        screen_width=1920, 
        screen_height=1080, 
        bins=(80, 45), 
        cmap='hot', 
        title='Gaze Heatmap on AOI',
        save_path = None
    ):
    df_clean = df[[x_col, y_col]].dropna()
    heatmap, xedges, yedges = np.histogram2d(df_clean[x_col].values, df_clean[y_col].values, bins=bins, range=[[0, screen_width], [0, screen_height]])
    heatmap = heatmap.T[::-1, :]

    plt.figure(figsize=(12, 6))
    plt.imshow(heatmap, extent=[0, screen_width, 0, screen_height], cmap=cmap, interpolation='nearest', aspect='auto', origin='lower')
    plt.colorbar(label='Gaze Fixation Count')
    plt.title(title)
    plt.xlabel(f'{x_col} (pixels)')
    plt.ylabel(f'{y_col} (pixels)')
    plt.grid(False)
    plt.tight_layout()
    
    if save_path:
        plt.savefig(save_path)
        plt.close()
    else:
        plt.show()


def plot_gaze_heatmap_with_background(
        df, 
        background_path, 
        x_col='Gaze point X', 
        y_col='Gaze point Y', 
        bins=(80, 45), 
        cmap='hot', 
        alpha=0.5, 
        title='Gaze Heatmap Overlay on AOI Image',
        save_path = None
    ):
    bg_img = mpimg.imread(background_path)
    img_height, img_width = bg_img.shape[:2]
    df_clean = df[[x_col, y_col]].dropna()

    heatmap, xedges, yedges = np.histogram2d(df_clean[x_col], df_clean[y_col], bins=bins, range=[[0, img_width], [0, img_height]])
    heatmap = heatmap.T[::-1, :]

    plt.figure(figsize=(12, 6))
    plt.imshow(bg_img, extent=[0, img_width, 0, img_height])
    plt.imshow(heatmap, extent=[0, img_width, 0, img_height], cmap=cmap, interpolation='nearest', alpha=alpha, aspect='auto')
    plt.colorbar(label='Gaze Fixation Count')
    plt.title(title)
    plt.xlabel(f'{x_col} (pixels)')
    plt.ylabel(f'{y_col} (pixels)')
    plt.xlim(0, img_width)
    plt.ylim(0, img_height)
    plt.tight_layout()
    
    if save_path:
        plt.savefig(save_path)
        plt.close()
    else:
        plt.show()


def animate_gaze_points(
    df,
    x_col='Gaze point X',
    y_col='Gaze point Y',
    time_col='Eyetracker timestamp',
    screen_width=1920,
    screen_height=1080,
    interval_ms=50,
    trail_length=15,
    title='Animated Gaze Movement'
):
    '''
    視線データの時間的な動きをアニメーション表示します。
    Parameters:
    - df: pandas.DataFrame（視線データ）
    - x_col, y_col: 視線座標カラム名
    - time_col: タイムスタンプカラム名（マイクロ秒）
    - screen_width, screen_height: 表示画面サイズ（ピクセル）
    - interval_ms: アニメーションの更新間隔（ミリ秒）
    - trail_length: 点の履歴を何フレーム残すか
    - title: グラフタイトル
    '''

    df_clean = df[[x_col, y_col, time_col]].dropna().copy()
    df_clean['time_sec'] = (df_clean[time_col] - df_clean[time_col].min()) / 1_000_000
    df_clean = df_clean.sort_values('time_sec').reset_index(drop=True)

    x_data = df_clean[x_col].values
    y_data = df_clean[y_col].values
    times = df_clean['time_sec'].values

    fig, ax = plt.subplots(figsize=(10, 6))
    scat = ax.scatter([], [], s=50, c='red')
    trail, = ax.plot([], [], 'bo-', alpha=0.5)

    ax.set_xlim(0, screen_width)
    ax.set_ylim(screen_height, 0)
    ax.set_title(title)
    ax.set_xlabel(x_col)
    ax.set_ylabel(y_col)
    ax.grid(True)

    def init():
        scat.set_offsets([])
        trail.set_data([], [])
        return scat, trail

    def update(frame):
        if frame < trail_length:
            trail_x = x_data[:frame]
            trail_y = y_data[:frame]
        else:
            trail_x = x_data[frame-trail_length:frame]
            trail_y = y_data[frame-trail_length:frame]

        scat.set_offsets([x_data[frame], y_data[frame]])
        trail.set_data(trail_x, trail_y)
        return scat, trail

    ani = animation.FuncAnimation(fig, update, frames=len(x_data),
                                  init_func=init, interval=interval_ms, blit=True)
    plt.close(fig)
    return ani




def animate_gaze_plot_with_background(
    df,
    background_path,
    x_col='Gaze point X',
    y_col='Gaze point Y',
    time_col='Eyetracker timestamp',
    screen_width=1920,
    screen_height=1080,
    interval_ms=50,
    trail_length=15,
    title='Animated Gaze Movement',
    save_path=None
):
    """
    背景画像付きで視線データの時間的な動きをアニメーション表示・保存します。

    Parameters:
    - df: pandas.DataFrame（視線データ）
    - background_path: 背景画像ファイルのパス
    - x_col, y_col: 視線座標カラム名
    - time_col: タイムスタンプカラム名（マイクロ秒）
    - screen_width, screen_height: 表示画面サイズ（ピクセル）
    - interval_ms: アニメーションの更新間隔（ミリ秒）
    - trail_length: 点の履歴を何フレーム残すか
    - title: グラフタイトル
    - save_path: 保存ファイル名（.mp4など）。指定しなければ表示のみ。

    Returns:
    - ani: matplotlib.animation.FuncAnimation オブジェクト
    """

    df_clean = df[[x_col, y_col, time_col]].dropna().copy()
    df_clean['time_sec'] = (df_clean[time_col] - df_clean[time_col].min()) / 1_000_000
    df_clean = df_clean.sort_values('time_sec').reset_index(drop=True)

    x_data = df_clean[x_col].values
    y_data = df_clean[y_col].values

    bg_img = mpimg.imread(background_path)
    img_height, img_width = bg_img.shape[:2]

    fig, ax = plt.subplots(figsize=(10, 6))
    ax.imshow(bg_img, extent=[0, img_width, 0, img_height], origin='lower')
    scat = ax.scatter([], [], s=50, c='red')
    trail, = ax.plot([], [], 'bo-', alpha=0.5)

    ax.set_xlim(0, img_width)
    ax.set_ylim(img_height, 0)
    ax.set_title(title)
    ax.set_xlabel(x_col)
    ax.set_ylabel(y_col)
    ax.grid(True)

    def init():
        scat.set_offsets(np.empty((0, 2)))
        trail.set_data([], [])
        return scat, trail

    def update(frame):
        i = min(frame, len(x_data) - 1)

        if i < trail_length:
            trail_x = x_data[:i]
            trail_y = y_data[:i]
        else:
            trail_x = x_data[i - trail_length:i]
            trail_y = y_data[i - trail_length:i]

        current_point = np.array([[x_data[i], y_data[i]]])
        scat.set_offsets(current_point)
        trail.set_data(trail_x, trail_y)

        return scat, trail

    ani = animation.FuncAnimation(
        fig, update, frames=len(x_data),
        init_func=init, interval=interval_ms, blit=True
    )

    if save_path:
        ani.save(save_path, writer='ffmpeg', fps=1000 // interval_ms)

    plt.close(fig)
    return ani
