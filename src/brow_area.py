import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as patches

def draw_aoi_regions(background_image_path, aoi_data):
    """
    指定された背景画像に、指定されたAOIの矩形を描画します。
    背景画像は元の向きを維持し、矩形の位置は左下を原点とする座標系に合わせます。

    Args:
        background_image_path (str): 背景画像のファイルパス。
        aoi_data (list): 各AOI領域の 'name', 'x', 'y', 'width', 'height' を
                         含む辞書のリスト。

    Returns:
        numpy.ndarray: 矩形が描画された画像。
    """
    try:
        # Matplotlibで背景画像を読み込む
        image = plt.imread(background_image_path)
    except FileNotFoundError:
        print(f"Error: Could not read image from {background_image_path}")
        return None

    image_height, image_width, _ = image.shape

    # Matplotlibのカラーリスト (RGB形式)
    colors = [
        'green',
        'blue',
        'red',
        'yellow',
        'cyan',
        'magenta',
        'silver',
        'navy',
        'darkgreen',
        'maroon'
    ]

    # プロットと軸を作成
    fig, ax = plt.subplots(1)
    ax.imshow(image)

    # ax.invert_yaxis() を削除し、y座標を手動で変換します

    for i, aoi in enumerate(aoi_data):
        # 左下を原点とする座標を、Matplotlibのimshowの座標系（左上が原点）に変換
        x = aoi['x']
        y_bottom_left = aoi['y']
        width = aoi['width']
        height = aoi['height']

        # y座標を変換
        # 変換式: y_top_left = image_height - y_bottom_left - height
        y_top_left = image_height - y_bottom_left - height

        # 矩形の色を取得
        color = colors[i % len(colors)]

        # 矩形を作成して描画
        rect = patches.Rectangle((x, y_top_left), width, height,
                                 linewidth=2, edgecolor=color, facecolor='none')
        ax.add_patch(rect)

        # 領域名を書き込む
        # テキストのy座標も同様に変換する
        text_y_top_left = image_height - (y_bottom_left + height) + 25
        ax.text(x + 5, text_y_top_left, aoi['name'],
                color=color, fontsize=10, ha='left', va='top')

    # 軸を非表示にする
    ax.axis('off')

    # レンダラーを取得してバッファから画像データを取得
    fig.canvas.draw()
    renderer = fig.canvas.renderer
    image_with_rects = np.array(renderer.buffer_rgba(), dtype=np.uint8)

    # MatplotlibのRGBA（赤、緑、青、アルファ）からRGBに変換
    # アルファチャネルを削除
    image_with_rects = image_with_rects[:, :, :3]

    # プロットを閉じる
    plt.close(fig)

    return image_with_rects