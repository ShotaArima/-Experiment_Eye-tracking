from brow_area import draw_aoi_regions
import matplotlib.pyplot as plt
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




for key, aoi_data in aoi_dict.items():
    print(f"写真 {key} の画像を生成しています...")
    background_image_path = f"/data/pic/視線誘導問題.00{key}.jpeg"
    # AOI領域が描画された画像を作成
    output_image = draw_aoi_regions(background_image_path, aoi_data)

    if output_image is not None:
        # 画像を保存
        image_filename = f"/data/pic/photo_{key}_aoi.png"
        plt.imsave(image_filename, output_image)
        print(f"{image_filename} を保存しました")

print("\nすべての画像の生成が完了しました。")