import os
import shutil
import sys
from pathlib import Path
from urllib.parse import urlparse
from urllib.request import urlretrieve

import tomli


def load_config(config_path: str) -> str:
    """Load the assignment directory path from config.toml"""
    with open(config_path, 'rb') as f:
        config = tomli.load(f)
    return config['assignment_directory']['path']


def read_students(data_dir: Path) -> list:
    """Read students.csv and return list of student dicts"""
    students = []
    csv_path = data_dir / 'students.csv'
    
    with open(csv_path, 'r') as f:
        lines = f.readlines()
        
        for line in lines[1:]:
            parts = line.strip().split(',', 2)
            if len(parts) >= 3:
                students.append({
                    'first_name': parts[0].strip(),
                    'last_name': parts[1].strip(),
                    'website': parts[2].strip()
                })
    
    return students


def download_website(url: str, dest_dir: Path, student_name: str) -> bool | None:
    """Download website content using python's urlretrieve"""
    if not url or not url.strip():
        return False
    
    url = url.strip()
    parsed = urlparse(url)
    
    if not parsed.scheme:
        url = 'http://' + url
    
    dest_file = dest_dir / 'website.html'
    
    if dest_file.exists():
        return None
    
    try:
        urlretrieve(url, dest_file)
        return True
    except Exception as e:
        return False


def copy_other_files(data_dir: Path, student_dir: Path, exclude: str = 'students.csv'):
    """Copy all files from .data except students.csv"""
    for file in data_dir.iterdir():
        if file.name != exclude and file.is_file():
            dest = student_dir / file.name
            if not dest.exists():
                shutil.copy2(file, dest)
                print(f"  Copied {file.name}")


def main():
    config_path = 'config.toml'
    
    if len(sys.argv) > 1:
        config_path = sys.argv[1]
    
    assignment_dir = Path(load_config(config_path))
    data_dir = assignment_dir / '.data'
    
    if not data_dir.exists():
        print(f"Error: .data directory not found at {data_dir}")
        return
    
    students = read_students(data_dir)
    
    successful = 0
    failed = 0
    skipped = 0
    failed_students = []
    
    for student in students:
        student_dir = assignment_dir / f"{student['first_name']}-{student['last_name']}"
        student_dir.mkdir(exist_ok=True)
        
        result = download_website(student['website'], student_dir, f"{student['first_name']} {student['last_name']}")
        
        if result is True:
            successful += 1
        elif result is False:
            failed += 1
            failed_students.append(f"{student['first_name']} {student['last_name']}")
        else:
            skipped += 1
        
        copy_other_files(data_dir, student_dir)
    
    print_summary(successful, failed, skipped, failed_students)


def print_summary(successful: int, failed: int, skipped: int, failed_students: list):
    """Clear screen and print download summary"""
    os.system('cls' if os.name == 'nt' else 'clear')
    
    print('------------------------')
    print('Download Summary')
    print('------------------------')
    print(f'Successfully downloaded: {successful}')
    print(f'Failed downloads:        {failed}')
    print(f'Skipped (already existed): {skipped}')
    if failed_students:
        print('\nFailed students:')
        for name in failed_students:
            print(f'  - {name}')
    print('------------------------')


if __name__ == '__main__':
    main()
