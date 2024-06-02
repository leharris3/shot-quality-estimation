from format_data_kinetics_tf import clean_directory, format_dataset_kinetics
from split_dataset import copy_and_split_dataset

def main():

    train_val_src_dir = "/playpen-storage/levlevi/contextualized-shot-quality-analysis/data/experiments/train-sets/result-hidden/raw_clips/05_10_24_mean_err_70/nba_results_hidden_30k_480"
    test_dir = "/playpen-storage/levlevi/contextualized-shot-quality-analysis/data/experiments/test-sets/result-hidden/856x480/formatted/cleaned/nba_1.3k_balanced"
    dst_dir = "/playpen-storage/levlevi/contextualized-shot-quality-analysis/data/experiments/train-sets/result-hidden/formatted_datasets/oprime/noisey_vs_clean_data_ablation/nba_30k_bal_480_mean_err_70"

    # copy_and_split_dataset(
    #     train_val_src_dir=train_val_src_dir,
    #     test_dir=test_dir,
    #     dst_dir=dst_dir,
    #     num_files_to_copy=30000,
    #     # class_balance=[0.4529, 0.5471],
    # )

    clean_directory(dst_dir)
    format_dataset_kinetics(dst_dir)

if __name__ == "__main__":
    main()