from src.file_organizer.FileOrganizer import FileOrganizer
import sys

if __name__ == "__main__":

    if len(sys.argv) < 6:
        print("Usage: python main.py <config_path> <path_to_folder> <output_folder> <loc_limit> <file_limit>")
        sys.exit(1)

    config_path = sys.argv[1]
    path_to_folder = sys.argv[2]
    output_folder = sys.argv[3]
    loc_limit = int(sys.argv[4])
    file_limit = int(sys.argv[5])

    organizer = FileOrganizer(config_path, path_to_folder, output_folder, loc_limit, file_limit)
    organizer.organize_files()