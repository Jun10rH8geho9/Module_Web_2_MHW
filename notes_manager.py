import os
import csv
from rich.console import Console
from rich.table import Table
from rich.text import Text
from abc import ABC, abstractmethod

console = Console()

class AbstractNote(ABC):
    def __init__(self, text, tags=None):
        self.text = text
        self.tags = tags or []

    @abstractmethod
    def display(self):
        pass

class Note(AbstractNote):
    def display(self):
        print(f"Note: {self.text}, Tags: {', '.join(self.tags)}")

class NotesManager:
    def __init__(self, file_path='notes.csv'):
        self.file_path = file_path
        self.notes = self.load_notes()
        self.console = Console()

    def dump_notes(self):
        with open(self.file_path, 'w', newline='\n') as fh:
            field_names = ['text', 'tags']
            writer = csv.DictWriter(fh, fieldnames=field_names)
            writer.writeheader()
            for note in self.notes:
                writer.writerow({'text': note.text, 'tags': ', '.join(note.tags)})

    def load_notes(self):
        notes = []
        if os.path.exists(self.file_path):
            with open(self.file_path, newline='\n') as fh:
                reader = csv.DictReader(fh)
                for row in reader:
                    text = row['text']
                    tags = row['tags'].split(', ')
                    new_note = Note(text, tags)
                    notes.append(new_note)

            if notes:
                console.print("Нотатки успішно завантажені.")
            else:
                console.print("Не вдалося завантажити нотатки або файл порожній.")
        else:
            console.print(f"Файл '{self.file_path}' не знайдено. Спробуйте створити файл або перевірити шлях.")
        return notes

    def add_note(self, text=None, tags=None):
        """
        Додає нові нотатки.
        Args:
            text (str, optional): Текст нотатки. За замовчуванням - None.
            tags (list, optional): Список тегів для нотатки. За замовчуванням - None.
        """

        
        while True:
            text = input("Текст нотатки (або введіть 'закінчити' чи 'вийти' для завершення): ")
            
            if text.lower() == 'закінчити' or text.lower() == 'вийти':
                break

            tags = input("Теги (розділіть їх комою): ").split(',')
             # Додавання нової нотатки
            formatted_tags = [tag.strip() if tag.startswith('#') else f"#{tag.strip()}" for tag in tags]
            new_note = Note(text, tags=formatted_tags)
            self.notes.append(new_note)
            console.print(f"[green]Нотатка успішно додана.[/green]")
            self.dump_notes()


    def list_notes(self):
        """
        Виводить список існуючих нотаток.
        """
            # Виведення списку нотаток
        if not self.notes:
            console.print("[red]У вас немає жодних нотаток.[/red]")
            return  # Повернення з функції, оскільки немає нотаток для редагування

        table = Table(title="Список нотаток")
        table.add_column("[blue]Номер[/blue]")
        table.add_column("[blue]Текст[/blue]")
        table.add_column("[cyan]Теги[/cyan]")

        for i, note in enumerate(self.notes, start=0):
            table.add_row(
                Text(str(i), style="blue"),
                Text(note.text, style="blue"),
                Text(", ".join(note.tags), style="cyan")
            )

        console.print(table, justify="center")
        console.print(f"[green]Кількість існуючих нотаток: {len(self.notes)}[/green]")


        
    def search_notes(self, text_query=None, tag_query=None):
        """
        Пошук нотаток за текстом або тегом.
        Args:
            text_query (str, optional): Текст для пошуку в нотатках. За замовчуванням - None.
            tag_query (str, optional): Тег для пошуку в нотатках. За замовчуванням - None.
        """
        specify_query = input(
            "Введіть слово 'текст' для пошуку за текстом або введіть слово 'тег' для пошуку за тегом: ")
        if specify_query == 'текст':
            text_query = input("Введіть текст для пошуку: ")
        elif specify_query == 'тег':
            tag_query = input("Введіть тег для пошуку: ")

        matching_notes = []
        if text_query is not None:
            matching_notes_text = [note for note in self.notes if text_query.lower() in note.text.lower()]
            matching_notes.extend(matching_notes_text)
        if tag_query is not None:
            matching_notes_tag = [note for note in self.notes if
                                  any(tag_query.lower() in tag.lower() for tag in note.tags)]
            matching_notes.extend(matching_notes_tag)

        if matching_notes:
            console.print(f"[bold green]Результати пошуку:[/bold green]")

            # Виведення знайдених нотаток в таблицю
            table = Table(title="Знайдені нотатки")
            table.add_column("[cyan]Номер[/cyan]")
            table.add_column("[blue]Нотатка[/blue]")
            table.add_column("[green]Теги[/green]")

            for i, note in enumerate(matching_notes, start=0):
                table.add_row(
                    Text(str(i), style='cyan'),
                    Text(note.text, style='blue'),
                    Text(", ".join(note.tags), style='green')
                )

            console.print(table, justify='center')

        else:
            if text_query is None:
                console.print(f"[red]Немає результатів пошуку за тегом: '{tag_query}'[/red]")
            if tag_query is None:
                console.print(f"[red]Немає результатів пошуку за текстом: '{text_query}'[/red]")

    def edit_note(self, note_index):
        """
        Редагує існуючу нотатку за індексом.
        Args:
            note_index (int): Індекс нотатки для редагування.
        """
        if 0 <= note_index < len(self.notes):
            # Отримання нотатки за індексом
            note_to_edit = self.notes[note_index]

            # Редагування тексту нотатки
            new_text = input("Введіть новий текст нотатки: ")
            note_to_edit.text = new_text

            # Редагування тегів нотатки
            new_tags = input("Введіть нові теги нотатки (через кому): ").split(",")
            note_to_edit.tags = [tag.strip() if tag.startswith('#') else f"#{tag.strip()}" for tag in new_tags]

            console.print(f"[green]Нотатка {note_index} успішно відредагована.[/green]")
        else:
            console.print("[red]Невірний індекс нотатки. Спробуйте ще раз.[/red]")
        self.dump_notes()

                
    def delete_note(self):
        """
        Видаляє нотатку користувача за текстом, назвою або тегом.
        Користувач вводить запит для пошуку нотаток. Знайдені нотатки виводяться, і користувач може
        обрати конкретну нотатку для видалення. Видалена нотатка видаляється зі списку нотаток.
        """
        # Отримання запиту від користувача або використання дефолтного значення
        query = console.input("Введіть текст, назву або тег для пошуку: ")

        # Пошук нотаток за текстом, назвою або тегом
        matching_notes = [note for note in self.notes if query.lower() in note.text.lower() or query.lower() in note.tags]

        if matching_notes:
            console.print(f"[bold green]Результати пошуку:[/bold green]")
            for index, note in enumerate(matching_notes, start=0):
                console.print(f"{index}. {note.text}")

            # Отримання від користувача індексу нотатки для видалення
            note_index_str = console.input("[bold cyan]Введіть номер нотатки для видалення (або 0, щоб скасувати):[/bold cyan] ")
            try:
                note_index = int(note_index_str)
            except ValueError:
                note_index = 0

            if 0 < note_index <= len(matching_notes):
                # Видалення вибраної нотатки
                deleted_note = matching_notes[note_index - 1]
                self.notes.remove(deleted_note)
                console.print(f"[bold green]Нотатка успішно видалена:[/bold green] {deleted_note.text}")
            elif note_index == 0:
                console.print("[cyan]Видалення скасовано користувачем.[/cyan]")
            else:
                console.print("[red]Введено невірний номер нотатки. Видалення скасовано.[/red]")
        else:
            console.print(f"[red]Немає результатів пошуку для запиту: {query}[/red]")
        self.dump_notes()


    def sort_notes_by_tags(self):
        """
        Сортує нотатки за тегами та виводить результат у вигляді табличного вигляду.
        Якщо немає жодних нотаток, виводить повідомлення про відсутність нотаток.
        """
        # Сортування нотаток за тегами
        if not self.notes:
            console.print("Немає нотаток для сортування.")
            return
        # створюємо словник для нотаток за тегами
        notes_by_tag_dict = {}  
        for note in self.notes:
            for tag in note.tags:
                if tag not in notes_by_tag_dict:
                    notes_by_tag_dict[tag] = []
                # додаємо нотатку до списку за ключем(тегом)
                notes_by_tag_dict[tag].append(note)

        sorted_tags = sorted(notes_by_tag_dict.keys())

        # відображення нотаток
        table = Table(title="Сортування нотаток за тегами")
        table.add_column("[red]Тег[/red]")
        table.add_column("[green]Текст[/green]")

        for tag in sorted_tags:
            tag_notes = notes_by_tag_dict[tag]
            for note in tag_notes:
                table.add_row(Text(tag, style="red"), Text(note.text, style="green"))

        console.print(table)
        self.dump_notes()
