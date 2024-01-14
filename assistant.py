from rich.console import Console
from prompt_toolkit import prompt
from prompt_toolkit.completion import WordCompleter
from rich.table import Table
from rich.live import Live
from contact_manager import ContactManager
from notes_manager import NotesManager
from sorter_manager import FolderOrganizer

console = Console()

class PersonalAssistantFacade:
    def __init__(self):
        self.contact_manager = ContactManager()
        self.notes_manager = NotesManager()
        self.sorter_manager = FolderOrganizer()
        self.commands = ['додати контакт', 'список контактів', 'пошук контактів', 'дні народження', 
                         'редагувати контакт', 'видалити контакт', 'сортувати файли',
                         'додати нотатку', 'пошук нотаток', 'видалити нотатку', 'список нотаток', 
                         'редагувати нотатку', 'сортувати нотатки', 'допомога', 'вихід']
        # Встановлення автодоповнення на основі доступних команд
        self.command_completer = WordCompleter(self.commands)
    
    # Додавання контакту через консоль
    def add_contact_from_console(self):
        self.contact_manager.add_contact_from_console()

    # Видалення контакту
    def delete_contact(self):
        self.contact_manager.delete_contact()

    # Список контактів
    def list_contacts(self):
        self.contact_manager.list_contacts()
    
    # Покшук контактів
    def search_contacts(self):
        self.contact_manager.search_contacts()

    # Редагування контактів
    def edit_contact(self, contact):
        self.contact_manager.edit_contact(contact)

    # Пошук наступного дня народження
    def upcoming_birthdays(self, days):
        self.contact_manager.upcoming_birthdays(days)
    
    # Додавання нотатки
    def add_note(self):
        self.notes_manager.add_note()

    # Видалення нотатки
    def delete_note(self):
        self.notes_manager.delete_note()

    # Спсок нотаток
    def list_notes(self):
        self.notes_manager.list_notes()

    # Редагування нотаток
    def edit_note(self, note_index):
        self.notes_manager.edit_note(note_index)
    
    # Пошук нотаток
    def search_notes(self):
        self.notes_manager.search_notes()

    # Сортування нотаток
    def sort_notes_by_tags(self):
        self.notes_manager.sort_notes_by_tags()

    def organize_folder(self, local_path):
        self.sorter_manager.organize_folder(local_path)
    
    # Псевдо-штучний інтелект відображення доступних команд
    def analyze_user_input(self, user_input):
        normalized_input = user_input.lower()
        if "допомога" in normalized_input:
            self.display_commands_table()
        elif "додати контакт" in normalized_input:
            console.print("[green]Пропоную вам додати новий контакт.[/green]")
        elif "видалити контакт" in normalized_input:
            console.print("[green]Для видалення контакту.[/green]")
        elif "список контактів" in normalized_input:
            console.print("[green]Ваш список контактів.[/green]")
        elif "пошук контактів" in normalized_input:
            console.print("[green]Для пошуку контактів введіть ім'я.[/green]")  
        elif "редагувати контакт" in normalized_input:
            console.print("[green]Для редагування контакту.[/green]")
        elif "дні народження" in normalized_input:
            console.print("[green]Перегляньте список контактів у кого День народження впродовж наступного тижня.[/green]")
        elif "додати нотатку" in normalized_input:
            console.print("[green]Додавання нових нотаток:[/green]")
        elif "видалити нотатку" in normalized_input:
            console.print("[green]Для видалення нотатки.[/green]") 
        elif "пошук нотаток" in normalized_input:
            console.print("[green]Для пошуку нотаток: [/green]")
        elif "список нотаток" in normalized_input:
            console.print("[green]Ваш список нотаток.[/green]")
        elif "редагувати нотатку" in normalized_input:
            console.print("[green]Для редагування нотатки:[/green]")
        elif "сортувати нотатки" in normalized_input:
            console.print("[green]Відсортовані нотатки: [/green]")
        elif "сортувати файли" in normalized_input:
            console.print("[green]Для сортування файлів: [/green]")
        elif "вихід" in normalized_input:
            console.print("[green]До нових зустрічей![/green]")
            exit()
        elif "допомога" in normalized_input:
            self.display_commands_table()
        else:
            console.print("[red]Не можу розпізнати вашу команду. Пропоную Вам список доступних команд.[/red]")
            self.display_commands_table()  

    def display_commands_table(self):
        """Створює таблицю зі списком доступних команд і виводить її в консолі"""
        # Створення об'єкта Console
        console = Console()

        # Створення таблиці зі списком команд
        table = Table(title="Доступні команди")
        table.add_column("[cyan]Команда[/cyan]", justify="center")

        for i, command in enumerate(self.commands):
            # Визначення кольору для кожного рядка
            color = "red" if i % 2 == 0 else "cyan"

            # Додавання рядка з визначеним кольором
            table.add_row(f"[{color}]{command}[/{color}]")

        # Виведення таблиці в консоль з використанням Live
        with Live(refresh_per_second=1, console=console) as live:
            console.print(table, justify="center")  # Виведення таблиці з вирівнюванням по центру
            input("Натисніть Enter для завершення перегляду команд...")  # Очікування вводу від користувача
            live.stop()
    
    def run(self):
        # Основний цикл програми, викликайте методи фасаду при введенні користувача
        pass

class PersonalAssistant:
    def __init__(self):
        self.facade = PersonalAssistantFacade()
        self.commands = ['додати контакт', 'список контактів', 'пошук контактів', 'дні народження', 
                         'редагувати контакт', 'видалити контакт', 'сортувати файли',
                         'додати нотатку', 'пошук нотаток', 'видалити нотатку', 'список нотаток', 
                         'редагувати нотатку', 'сортувати нотатки', 'допомога', 'вихід']
    

    def run(self):
        completer = WordCompleter(self.facade.commands, ignore_case=True)
        """ Основний цикл виконання програми. Полягає в тому, 
            що він виводить вітання та список команд, а потім 
            чекає на введення команди"""
        console = Console()
        console.print(
            "\n[bold yellow]Вітаю, я ваш особистий помічник![/bold yellow]\n",
            justify="center",
            style="bold",
            width=200,
        )
        self.facade.display_commands_table()
        self.facade.run()
        
        while True:
            user_input = prompt("Введіть команду: ", completer=completer).lower()
            self.facade.analyze_user_input(user_input)             # self. instead of assistant.
            # Перевірка команд і виклик відповідного методу
            
            if "допомога" in user_input.lower() :
                self.facade.display_commands_table()               # # self. instead of assistant.
            elif "додати контакт" in user_input.lower():
                self.facade.add_contact_from_console()
            elif 'видалити контакт' in user_input.lower():
                self.facade.delete_contact()
            elif "список контактів" in user_input.lower():
                self.facade.list_contacts()
            elif "пошук контактів" in user_input.lower():
                self.facade.search_contacts()
            elif "дні народження" in user_input.lower():
                self.facade.upcoming_birthdays(7)
            elif 'редагувати контакт' in user_input.lower():
                contact_to_edit = self.facade.search_contacts() 
                self.facade.edit_contact(contact=contact_to_edit)
            elif "додати нотатку" in user_input.lower():
                self.facade.add_note()
            elif "видалити нотатку" in user_input.lower():
                self.facade.delete_note()
            elif "список нотаток" in user_input.lower():
                self.facade.list_notes()
            elif "редагувати нотатку" in user_input.lower():
                if "редагувати нотатку" in user_input.lower():
                    while True:
                        try:
                            note_index = int(input("Введіть номер нотатки, яку ви хочете відредагувати: "))
                            if note_index == "":
                                raise ValueError
                            else:
                                self.facade.edit_note(note_index)
                                break
                        except ValueError: ("Не вказано номер нотатки!")
            elif "пошук нотаток" in user_input.lower():
                self.facade.search_notes()   
            elif "сортувати нотатки" in user_input.lower():
                self.facade.sort_notes_by_tags()
            elif "сортувати файли" in user_input.lower():
                local_path = input("Введіть назву папки або шлях до папки для сортування: ")
                self.facade.organize_folder(local_path)
            elif "вихід" in user_input.lower():
                self.facade.contact_manager.dump()
                self.facade.notes_manager.dump_notes()
                break
        
def main():
    assistant = PersonalAssistant()
    assistant.facade.contact_manager.load()
    assistant.facade.notes_manager.load_notes()
    assistant.run()
    return assistant


if __name__ == "__main__":
    assistant_instance = main()
    user_input = "example"
    assistant_instance.facade.analyze_user_input(user_input)