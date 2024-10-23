import os
import csv
from tqdm import tqdm


def get_folder_size(folder_path):
    total_size = 0
    for dirpath, dirnames, filenames in os.walk(folder_path):
        for filename in filenames:
            filepath = os.path.join(dirpath, filename)
            try:
                total_size += os.path.getsize(filepath)
            except (PermissionError, FileNotFoundError) as e:
                # Skip files that cannot be read
                print(f"Error reading file {filepath}: {e}")
    return total_size


def get_last_used_time(folder_path):
    try:
        return os.path.getatime(folder_path)
    except (PermissionError, FileNotFoundError) as e:
        print(f"Error reading folder {folder_path}: {e}")
        return "N/A"


def main():
    # TODO Replace with your actual root folder path
    root_folder = r'C:\Users\AnthonyWynne'
    csv_file = 'folder_sizes.csv'

    folder_info = []
    # tqdm doesnt know the total number of folders,
    # so it cannot show the progress bar initially
    print("Discovering folders...")
    for dirpath, dirnames, filenames in tqdm(os.walk(root_folder),
                                             desc="Traversing folders"):
        for dirname in dirnames:
            try:
                folder_path = os.path.join(dirpath, dirname)
                size = get_folder_size(folder_path)
                # last_used_time = get_last_used_time(folder_path)
                folder_info.append((folder_path, size, "N/A"))  # , last_used_time removed
            except (PermissionError, FileNotFoundError) as e:
                # Skip folders that cannot be read
                print(f"Error getting info for folder {folder_path}: {e}")

    folder_info.sort(key=lambda x: x[1])  # Sort by size

    with open(csv_file, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['Folder Path', 'Size (bytes)', 'Last Used Time'])
        for folder_path, size, last_used_time in folder_info:
            writer.writerow([folder_path, size, last_used_time])

    print(f"Folder sizes and last used times saved to {csv_file}")


if __name__ == "__main__":
    main()
