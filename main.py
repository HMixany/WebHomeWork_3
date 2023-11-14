'''
Відсортувати файли в папці
'''

import re
import shutil
from pathlib import Path
from threading import Thread
import logging
import concurrent.futures
import sys


groups_files = {
    'images': ['JPEG', 'PNG', 'JPG', 'SVG'],
    'video': ['AVI', 'MP4', 'MOV', 'MKV'],
    'documents': ['DOC', 'DOCX', 'TXT', 'PDF', 'XLSX', 'PPTX'],
    'audio': ['MP3', 'OGG', 'WAV', 'AMR'],
    'archives': ['ZIP', 'GZ', 'TAR']
}

folders = []


def normalize(name):
    UKRAINIAN_SYMBOLS = 'абвгдеєжзиіїйклмнопрстуфхцчшщьюяы'
    TRANSLATION = (
        "a", "b", "v", "g", "d", "e", "je", "zh", "z", "y", "i", "ji", "j", "k", "l", "m", "n", "o", "p", "r", "s", "t",
        "u", "f", "h", "ts", "ch", "sh", "sch", "", "ju", "ja", "y"
    )
    TRANS = {}
    for key, value in zip(UKRAINIAN_SYMBOLS, TRANSLATION):
        TRANS[ord(key)] = value
        TRANS[ord(key.upper())] = value.upper()
    name, *extension = name.split('.')
    new_name = name.translate(TRANS)
    new_name = re.sub(r'\W', "_", new_name)

    return f"{new_name}.{'.'.join(extension)}"


def translation(folder):
    for item in folder.iterdir():
        if item.is_dir():
            translation(item)
        new_name = normalize(item.name).rstrip('.')
        item.rename(folder / new_name)


def grabs_folder(path: Path) -> None:
    for item in path.iterdir():
        if item.is_dir():
            folders.append(item)
            grabs_folder(item)


def moving_file(file: Path, dist) -> None:
    target_folder = path / dist
    target_folder.mkdir(exist_ok=True)
    logging.info(f'Start movimg {file.name}')
    distinction = target_folder / file.name
    shutil.move(file, distinction)


def moving_archive(file, dist):
    target_folder = path / dist
    if not target_folder.exists():
        target_folder.mkdir()
    new_name = file.name.replace(file.suffix, '')
    archive_folder = target_folder / new_name
    archive_folder.mkdir(exist_ok=True)
    try:
        shutil.unpack_archive(file, archive_folder)
    except shutil.ReadError:
        archive_folder.rmdir()
        return
    file.unlink()


def scan_folder(folder: Path) -> None:
    logging.info(f'Start thread folder {folder.name}')
    threads = []
    for item in folder.iterdir():
        dist = 'others'
        if item.is_file():
            extension = item.suffix.upper().lstrip('.')
            if extension in groups_files['archives']:
                Thread(target=moving_archive, args=(item, 'archives')).start()
                continue
            else:
                for key, value in groups_files.items():
                    if extension in value:
                        dist = key
                        break
            thread = Thread(target=moving_file, args=(item, dist))
            thread.start()
            threads.append(thread)
    [th.join() for th in threads]


def remove_empty_folders(folder_path):
    for item in folder_path.iterdir():
        if item.is_dir():
            logging.info(f'Scan for remove {item.name}')
            if item.name in ['images', 'video', 'documents', 'audio', 'archives', 'others']:
                continue
            if not any(item.iterdir()):
                item.rmdir()
                remove_empty_folders(path)
            else:
                remove_empty_folders(item)


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO, format='%(threadName)s %(message)s')
    # path = Path('D:/Projects/Мотлох')
    path = Path(sys.argv[1])
    path = path.rename(path.parent / normalize(path.name).rstrip('.'))
    translation(path)
    folders.append(path)
    grabs_folder(path)
    print(folders)
    with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
        executor.map(scan_folder, folders)
    # threads = []
    # for folder in folders:
    #     th = Thread(target=scan_folder, args=(folder,))
    #     th.start()
    #     threads.append(th)
    # [thread.join() for thread in threads]
    remove_empty_folders(path)
