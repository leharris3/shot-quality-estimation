import pandas as pd
import json
from concurrent.futures import ThreadPoolExecutor, as_completed
from tqdm import tqdm

import os
import pandas as pd
from datascience import *

dir_path = '/Volumes/Seagate_19X/Euroleague_data/Game_log_data'
csv_fps = []

for root, dir, files in os.walk(dir_path):
    for file in files:
        fp = os.path.join(root, file)
        if fp.endswith('.csv'):
            csv_fps.append(fp)
            
keys = "id	action_id	action_name	player_id	player_name	team_id	team_name	opponent_id	opponent_name	opponent_team_id	opponent_team_name	teammate_id	teammate_name	half	second	pos_x	pos_y	possession_id	possession_name	possession_team_id	possession_team_name	possession_number	possession_start_clear	possession_end_clear	playtype	hand	shot_type	drive	dribble_move	contesting	ts".split()

def process_file(fp):
    try:
        league = fp.split('/')[-2]
        temp_df = pd.read_csv(fp, delimiter=';', names=keys)
        return league, {
            '1-': sum(temp_df['action_name'] == '1-'),
            '1+': sum(temp_df['action_name'] == '1+'),
            '2-': sum(temp_df['action_name'] == '2-'),
            '2+': sum(temp_df['action_name'] == '2+'),
            '3-': sum(temp_df['action_name'] == '3-'),
            '3+': sum(temp_df['action_name'] == '3+')
        }
    except Exception as e:
        print(f"Error: could not read file at {fp}")
        return league, None

def update_log_stats(results):
    log_stats = {}
    for league, stats in results:
        if stats is not None:
            if league not in log_stats:
                log_stats[league] = {
                    '1-': 0, 
                    '1+': 0, 
                    '2-': 0, 
                    '2+': 0, 
                    '3-': 0, 
                    '3+': 0
                    }
            for key in stats:
                log_stats[league][key] += stats[key]
    return log_stats

# Main processing with concurrent execution
def main(csv_fps):
    results = []
    with ThreadPoolExecutor(max_workers=32) as executor:
        future_to_fp = {executor.submit(process_file, fp): fp for fp in csv_fps}
        for future in tqdm(as_completed(future_to_fp), total=len(csv_fps)):
            result = future.result()
            if result:
                results.append(result)

    log_stats = update_log_stats(results)

    # Save the log statistics to a JSON file
    with open('log_stats.json', 'w') as f:
        json.dump(log_stats, f)

    print("Completed processing and saved the results.")

main(csv_fps)