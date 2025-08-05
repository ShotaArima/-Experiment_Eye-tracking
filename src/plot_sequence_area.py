from sequence_area_flg import plot_gaze_area_transition
import pandas as pd

from src.area_flog import df_selected

for question in (1, 5):
    for user in (1, 10):
        csv_path = f'/output/all-users/pic-{question}/user-{user}-with-area_flg.csv'
        df_selected = pd.read_csv(csv_path)

        plot_gaze_area_transition(df_selected, question)