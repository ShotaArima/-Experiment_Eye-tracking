import pandas as pd

def assign_area_flag(df: pd.DataFrame, aoi_list: list, x_col='Gaze point X', y_col='Gaze point Y') -> pd.DataFrame:
    """
    視線座標がどのAOIに属するか判定して 'area_flg' 列を追加
    """
    def get_area(x, y):
        for aoi in aoi_list:
            if aoi["x"] <= x <= aoi["x"] + aoi["width"] and \
               aoi["y"] <= y <= aoi["y"] + aoi["height"]:
                return aoi["name"]
        return "Outside"  # どのAOIにも該当しない場合

    df = df.copy()
    df['area_flg'] = df.apply(lambda row: get_area(row[x_col], row[y_col]), axis=1)
    return df
