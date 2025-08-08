from hmmlearn import hmm
import numpy as np
import pandas as pd


def hmm_model():

    df = pd.read_csv(f'/output/all_users/pic-1/user-1_with_area_flg.csv')
    print("comlete read csv")
    # Validity leftとValidity rightが両方ともValidなデータにフィルタリング
    df_valid = df[(df['Validity left'] == 'Valid') & (df['Validity right'] == 'Valid')]
    # 必要なカラムだけを抽出
    df_valid = df_valid[['Eyetracker timestamp', 'area_flg']]
    # 遷移を作成
    df_valid['next_area_flg'] = df_valid['area_flg'].shift(-1)

    # 現在の`area_flg`と次の`area_flg`のペアを使って遷移回数を計算
    transitions = pd.crosstab(df_valid['area_flg'], df_valid['next_area_flg'], dropna=False)

    # 行ごとに正規化して遷移確率を計算
    transition_matrix = transitions.div(transitions.sum(axis=1), axis=0)

    # `area_flg`のユニークな値を取得
    states = df_valid['area_flg'].unique()

    # HMMを構築（この場合、モデルの状態数は`area_flg`のユニーク数と一致させる）
    model = hmm.MultinomialHMM(n_components=len(states), random_state=42)

    # 状態に対応する数値を設定
    state_mapping = {state: i for i, state in enumerate(states)}

    # `area_flg`のデータを数値に変換
    df_valid['area_flg_numeric'] = df_valid['area_flg'].map(state_mapping)

    # データをHMMモデルに適合させるための形式に整形
    sequence = df_valid['area_flg_numeric'].values.reshape(-1, 1)

    # HMMの学習
    model.fit(sequence)

    # 学習した遷移確率を表示
    print("遷移確率行列:")
    print(model.transmat_)

    # 新しいデータ（例えば、最初の状態）に対して遷移予測
    logprob, predicted_states = model.decode(sequence)

    # 予測された状態を対応する`area_flg`に戻す
    predicted_area_flg = [states[state] for state in predicted_states]

    # 予測結果の表示
    print(predicted_area_flg)


if __name__ == "__main__":
    hmm_model()
