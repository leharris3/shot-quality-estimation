from utils.config import *
from extract_rh_shots import run_parallel_job

def main():

    dst_dir = "/playpen-storage/levlevi/contextualized-shot-quality-analysis/data/experiments/train-sets/result-hidden/raw_clips/05_31_24_mean_err_30"
    hudl_logs_dir = "/mnt/sun/levlevi/nba-plus-statvu-dataset/hudl-game-logs"
    nba_replays_dir = "/mnt/sun/levlevi/nba-plus-statvu-dataset/game-replays"
    run_parallel_job(dst_dir, hudl_logs_dir, nba_replays_dir, num_devices=NUM_GPUS)


if __name__ == "__main__":
    main()
