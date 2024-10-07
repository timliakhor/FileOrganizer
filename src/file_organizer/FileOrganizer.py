
import os
import shutil
import json
import csv
from datetime import datetime

class FileOrganizer:
    def __init__(self, config_path, path_to_folder, output_folder, loc_limit, file_limit):
        self.path_to_folder = path_to_folder
        self.output_folder = output_folder
        self.loc_limit = loc_limit
        self.file_limit = file_limit
        self.load_config(config_path)
        self.src_folder = os.path.join(self.output_folder, "src")
        self.tests_folder = os.path.join(self.output_folder, "tests")
        self.static_folder = os.path.join(self.output_folder, "static")
        self.resources_folder = os.path.join(self.output_folder, "resources")
        self.log_file = os.path.join(self.output_folder, "file_organization_log.csv")
        self.log_id = self.get_initial_log_id()

    def load_config(self, config_path):
        with open(config_path, 'r') as config_file:
            config = json.load(config_file)
            self.source_extensions = config.get("source_extensions", [".java", ".py", ".cpp"])
            self.tests_root_path = config.get("tests_root_path", "src/test/java/tests")
            self.excluded_folders = config.get("excluded_folders", [".venv", ".idea"])
            self.excluded_files = config.get("excluded_files", [".azure", ".DS_Store", ".gitignore"])

    def get_initial_log_id(self):
        if os.path.exists(self.log_file):
            with open(self.log_file, 'r') as log_csv:
                reader = csv.reader(log_csv)
                rows = list(reader)
                if len(rows) > 1:
                    return len(rows)
        return 1

    def scan_folder(self):
        src_files, test_files, static_files, resource_files = [], [], [], []
        for root, _, files in os.walk(self.path_to_folder):
            if any(excluded in root for excluded in self.excluded_folders):
                continue

            for file in files:
                if file in self.excluded_files:
                    continue

                file_path = os.path.join(root, file)
                extension = os.path.splitext(file)[1]

                if self.tests_root_path in root:
                    if extension in [".json", ".yml", ".yaml", ".xml"]:
                        resource_files.append(file_path)
                    else:
                        test_files.append(file_path)
                else:
                    if extension in [".html", ".css"]:
                        static_files.append(file_path)
                    elif extension in self.source_extensions:
                        src_files.append(file_path)
                    elif extension in [".json", ".yml", ".yaml", ".xml"]:
                        resource_files.append(file_path)

        return src_files, test_files, static_files, resource_files

    def organize_files(self):
        src_files, test_files, static_files, resource_files = self.scan_folder()
        if src_files:
            self.group_and_copy_files(src_files, self.src_folder, "src")
        if test_files:
            self.group_and_copy_files(test_files, self.tests_folder, "test")
        if static_files:
            self.group_and_copy_files(static_files, self.static_folder, "static")
        if resource_files:
            self.group_and_copy_files(resource_files, self.resources_folder, "resource")

    def group_and_copy_files(self, files, destination_folder, file_type):
        group_num, file_count, loc_count = 1, 0, 0
        dest_folder = os.path.join(destination_folder, str(group_num))
        os.makedirs(dest_folder, exist_ok=True)

        for file in files:
            loc = self.count_lines(file)
            if file_count >= self.file_limit or (loc_count + loc > self.loc_limit and file_count > 0):
                group_num += 1
                file_count, loc_count = 0, 0
                dest_folder = os.path.join(destination_folder, str(group_num))
                os.makedirs(dest_folder, exist_ok=True)

            output_path = os.path.join(dest_folder, os.path.basename(file))
            shutil.copy(file, output_path)
            self.log_file_organization(file, output_path, file_type, loc)
            file_count += 1
            loc_count += loc

    def count_lines(self, file_path):
        with open(file_path, 'r') as file:
            return sum(1 for _ in file)

    def log_file_organization(self, src_path, output_path, file_type, number_of_lines):
        process_date_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        log_entry = [
            self.log_id, src_path, output_path, file_type, number_of_lines, process_date_time
        ]

        log_exists = os.path.exists(self.log_file)
        with open(self.log_file, 'a', newline='') as log_csv:
            log_writer = csv.writer(log_csv)
            if not log_exists:
                log_writer.writerow(["id", "src_path", "output_path", "file_type", "number_of_lines", "process_date_time"])
            log_writer.writerow(log_entry)
        self.log_id += 1