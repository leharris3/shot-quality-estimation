import math
import os
import cv2
import pandas as pd
import numpy as np
import tqdm
import multiprocessing
import subprocess
from datascience import *

logs_dir = '/Users/leviharris/Library/CloudStorage/GoogleDrive-leviharris555@gmail.com/Other computers/mac_new/NBA_HUDL_data/nba-plus-statvu-dataset/hudl-game-logs'

# create map of video paths
base_video_dir = '/Users/leviharris/Library/CloudStorage/GoogleDrive-leviharris555@gmail.com/Other computers/mac_new/NBA_HUDL_data/nba-plus-statvu-dataset/game-replays/720'
all_videos = [os.path.join(base_video_dir, f) for f in os.listdir(base_video_dir)]
videos_map = {}

for v in all_videos:
    split = v.split('_')
    game_id = split[3].split('/')[-1]
    quarter = split[-1][6]
    uni_id = game_id + '_' + quarter
    videos_map[uni_id] = v

def is_shot(s):
    legal_strings = ['2+', '2-', '3+', '3-']
    return s in legal_strings

def is_made(s):
    if '+' in s:
        return True
    else: return False 

def get_shot_attempts(fp):

    # gather all shot attempts
    full_table = Table.from_df(pd.read_csv(fp, delimiter=';'))
    shot_attempts = full_table.with_column(
        'is_shot', 
        [is_shot(i) for i in full_table.column('action_name')],
    ).where('is_shot', are.equal_to(True)).select(['action_name', 'half', 'second'])

    # add columns
    shot_attempts = shot_attempts.with_columns(
        'is_made', [is_made(i) for i in shot_attempts.column('action_name')],
        'game_id', np.repeat(fp.split('.')[-2], shot_attempts.num_rows)
    )

    # add unified game qaurter string ids
    uni_ids = []
    for quarter, game_id in zip(shot_attempts.column('half'), shot_attempts.column('game_id')):
        uni_id = str(game_id) + '_' + str(quarter)
        uni_ids.append(uni_id)

    # append video paths to table
    video_paths = []
    for id in uni_ids:
        if id in videos_map:
            video_paths.append(videos_map[id])
        else:
            video_paths.append(None)

    shot_attempts: Table = shot_attempts.drop('game_id').drop('half').with_column(
        'video_path', video_paths
    ).with_column(
        'uni_id', uni_ids
    )
    return shot_attempts.to_df()

# 1. filter through hudl logs and concatinate all shot attempts into a table
# 2. match each shot attempt with its corresponding video path and timestamps
# 3. extract all shot attempts

logs = [os.path.join(logs_dir, f) for f in os.listdir(logs_dir)]
all_shot_attempts = None

# concatinate all logs together
for log_path in tqdm.tqdm(logs):
    if all_shot_attempts is None:
        all_shot_attempts = get_shot_attempts(log_path)
    else:
        all_shot_attempts = pd.concat([all_shot_attempts, get_shot_attempts(log_path)], axis=0)

# convert to datasceince table, filter out all missing videos
all_shot_attempts_table = Table.from_df(all_shot_attempts).where('video_path', are.not_equal_to(None))
all_shot_attempts_table

database_path = 'finetune_vgg/dataset_b'

def create_new_clip(row, database_dir):
    """
    Given a shot attempt row and dataset path, save a new clip to the
    corresponding 'make' or 'miss' subdirectory.
    """

    # game id info from row object
    attempt = str(row['action_name'])
    timestamp = str(row['second'])
    is_made = 'make' if row['is_made'] else 'miss'
    video_path = str(row['video_path'])
    uni_id = str(row['uni_id'])

    # game name and dst path
    # currently using .png extension
    name = 'uni_id_' + uni_id + '.' + 'points_' + attempt + '.timestamp_' + timestamp + '_' + '.png'
    dst_path = os.path.join(database_dir, is_made, name)

    # open cv2 capture object
    capture = cv2.VideoCapture(video_path)
    if not capture.isOpened():
        raise Exception(f'Could not open video at path {dst_path}!')
    
    # create a video writer object
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    fps = capture.get(cv2.CAP_PROP_FPS)
    # writer = cv2.VideoWriter(
    #     dst_path,
    #     fourcc,
    #     fps,
    #     (224, 224)
    # )
    
    # calculate the starting frame of the shot attempt
    # currently taking one frame starting at two seconds before timestamp
    clip_start_frame = float(timestamp) * fps - (2.75 * fps)

    # each clip will be three seconds in length
    clip_duration = 1

    # frame step for sparse sampling
    frame_step = math.floor((clip_duration) / 16) # current not used
    frame_index = clip_start_frame

    # write resized frames to clip out path
    for index in range(0, 1):

        # set video capture to next frame
        capture.set(cv2.CAP_PROP_POS_FRAMES, frame_index)
        ret, frame = capture.read()

        # resize frame to (224x224)
        # currently not resizing frames
        # resized_frame = cv2.resize(frame, (224, 224), interpolation=cv2.INTER_AREA)

        # write a single frame to the output destination

        cv2.imwrite(dst_path, frame)

        # writer currently not used
        # writer.write(resized_frame)

        # increment the frame index
        # currently not used
        # frame_index += frame_step

    # release writer/reader objects
    capture.release()

    # currently not used
    # writer.release()

def create_new_clip_wrapper(row_database_path_tuple):
    try:
        row, database_path = row_database_path_tuple
        create_new_clip(row, database_path)
    except:
        print(f"Could not process video: {row['uni_id']}.")

def row_to_dict(row):
    return {
        'action_name': row.action_name,
        'second': row.second,
        'is_made': row.is_made,
        'video_path': row.video_path,
        'uni_id': row.uni_id
    }

def main():
    rows_with_path = [(row_to_dict(row), database_path) for row in all_shot_attempts_table.rows]
    num_processes = multiprocessing.cpu_count()
    with multiprocessing.Pool(processes=num_processes) as pool:
        for _ in tqdm.tqdm(
            pool.imap_unordered(create_new_clip_wrapper, rows_with_path), 
            total=len(rows_with_path)
            ):
            pass

if __name__ == '__main__':
    multiprocessing.freeze_support()
    main()