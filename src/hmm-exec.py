from sequence_area_flg import plot_gaze_area_transition
import pandas as pd
from hmm import hmm_model

for question in range(1, 5):
    for user in range(1, 10):
        csv_path = f'/output/all_users/pic-{question}/user-{user}_with_area_flg.csv'
        # save_path =f'/output/all_users/pic-{question}/user-{user}_plot_gaze_area_transition.png'
        df = pd.read_csv(csv_path)


        # hmm_model(df, question, save_path=save_path)