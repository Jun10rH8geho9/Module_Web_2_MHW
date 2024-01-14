import shutil
import re
from pathlib import Path
from rich.console import Console

console = Console()

class FolderOrganizer:
    def __init__(self, folder_path=None):
        self.folder_path = folder_path
        
        self.CYRILLIC_SYMBOLS = 'абвгдеёжзийклмнопрстуфхцчшщъыьэюяєіїґ'
        self.TRANSLATION = ("a", "b", "v", "g", "d", "e", "e", "j", "z", "i", "j", "k", "l", "m", "n", "o", "p", "r", "s", "t", "u",
                           "f", "h", "ts", "ch", "sh", "sch", "", "y", "", "e", "yu", "u", "ja", "je", "ji", "g")

        self.TRANS = dict()

        for cyrillic, latin in zip(self.CYRILLIC_SYMBOLS, self.TRANSLATION):
            self.TRANS[ord(cyrillic)] = latin
            self.TRANS[ord(cyrillic.upper())] = latin.upper()

        self.KNOWN_EXTENSIONS = {
            'Images': {'JPEG', 'JPG', 'PNG', 'SVG'},
            'Video': {'AVI', 'MP4', 'MOV', 'MKV'},
            'Documents': {'DOC', 'DOCX', 'TXT', 'PDF', 'XLSX', 'PPTX'},
            'Audio': {'MP3', 'OGG', 'WAV', 'AMR'},
            'Archives': {'ZIP', 'GZ', 'TAR'},
        }


    def normalize(self, name: str) -> str:
        translate_name = re.sub(r'[^a-zA-Z0-9.]', '_', name.translate(self.TRANS))
        return translate_name

    def get_extension(self, name: str) -> str:
        return Path(name).suffix[1:].upper()

    def handle_file(self, file_name: Path, target_folder: Path):
        extension = self.get_extension(file_name)
        normalized_name = self.normalize(file_name.name)

        if extension in {ext for exts in self.KNOWN_EXTENSIONS.values() for ext in exts}:
            target_folder = target_folder / extension
        else:
            target_folder = target_folder / 'MY_OTHER'

        target_folder.mkdir(exist_ok=True, parents=True)
        target_path = target_folder / normalized_name

        if target_path.exists():
            target_path = target_folder / f"{normalized_name.stem}_{normalized_name.suffix}"

        shutil.move(str(file_name), str(target_path))

    def organize_folder(self, local_path):   
        self.folder_path = Path(local_path) 

        if not self.folder_path.exists() or not self.folder_path.is_dir():     
            console.print(f'[red]Папка "{self.folder_path}" не існує.[/red]')

            while True:
                new_user_input = input('Введіть назву папки для сортування (або натисніть "enter", для введення іншої команди): ')
                if new_user_input == '':
                    break
                else:
                    self.organize_folder(new_user_input)
                    # return
        else:
            for item in self.folder_path.iterdir():
                if item.is_file():
                    self.handle_file(item, self.folder_path)
            console.print(f'[green]Файли в папці "{self.folder_path.name}" відсортовані.[/green]')