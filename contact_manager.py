import os
import csv
import re
from rich.console import Console
from datetime import datetime, date, timedelta
from rich.table import Table
from rich.text import Text
from dateutil import parser

console = Console()

class Contact:
    def __init__(self, name, address, phone, email, birthday):
        self.name = name
        self.address = address
        self.phone = phone
        self.email = email
        self.birthday = birthday


class ContactManager:
    def __init__(self):
        self.contacts = []
    
    def dump(self):
        """
        Зберігає книгу контактів у файл CSV.
        """
        with open('addressbook.csv', 'w', newline='\n', encoding='UTF-8') as fh:
            field_names = ['name', 'address', 'phone', 'email', 'birthday']
            writer = csv.DictWriter(fh, fieldnames=field_names)
            writer.writeheader()
            for contact in self.contacts:
                writer.writerow({'name': contact.name, 'address': contact.address,
                                 'phone': contact.phone, 'email': contact.email, 'birthday': contact.birthday.strftime('%d-%m-%Y')})

    def load(self):
        """
        Завантажує книгу контактів з файлу CSV.
        """
        file_path = 'addressbook.csv'
        if os.path.exists(file_path):
            with open(file_path, newline='\n', encoding='UTF-8') as fh:
                reader = csv.DictReader(fh)
                for row in reader:
                    name = row['name']
                    address = row['address']
                    phone = row['phone']
                    email = row['email']

                    # Перетворення рядка дати у об'єкт datetime.date
                    birthday_str = row['birthday']
                    birthday = datetime.strptime(birthday_str, '%d-%m-%Y').date()

                    new_contact = Contact(
                        name, address, phone, email, birthday)
                    self.contacts.append(new_contact)

            if self.contacts:
                print("Контакти успішно завантажені.")
            else:
                print("Не вдалося завантажити контакти або файл порожній.")
        else:
            print(f"Файл '{file_path}' не знайдено. Спробуйте створити файл або перевірити шлях.")

    def is_valid_phone(self, phone):
        """
        Перевіряє, чи відповідає формат номера телефону встановленим правилам.
        Args:
            phone (str): Номер телефону для перевірки.
        Returns:
            bool: True, якщо номер телефону відповідає формату, False - інакше.
        """
        # Перевірка правильності формату номера телефону
        # Допустимі формати: +380501234567, 050-123-45-67, 0501234567, (050)123-45-67, 0989898989
        phone_pattern = re.compile(r'^\+?\d{1,3}?[-.\s]?\(?\d{1,4}\)?[-.\s]?\d{1,4}[-.\s]?\d{1,9}$')
        return bool(re.fullmatch(phone_pattern, phone))


    def is_valid_email(self, email):
        """
        Перевіряє, чи відповідає формат електронної пошти встановленим правилам.
        Args:
            email (str): Адреса електронної пошти для перевірки.
        Returns:
            bool: True, якщо адреса електронної пошти відповідає формату, False - інакше.
        """
        # Перевірка правильності формату електронної пошти
        email_pattern = re.compile(r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$')
        return bool(re.match(email_pattern, email))
        
    def add_contact_from_console(self):
        console.print("[bold]Додавання нового контакту:[/bold]")
        name = input("Ім'я: ")
        address = input("Адреса: ")
        while True:
            try:
                phone_input = input("Телефон (формати вводу +380501234567, 050-123-45-67, 0501234567, (050)123-45-67): ")
                if self.is_valid_phone(phone_input):
                    phone = phone_input
                    break
                else:
                    raise ValueError
            except ValueError:
                console.print("[bold red]Помилка:[/bold red] Некоректний формат номера телефону. Використовуйте наступний формат: +380501234567, 050-123-45-67, 0501234567 або (050)123-45-67.")
        while True:
            try:
                email_input = input("Електронна пошта: ")
                if self.is_valid_email(email_input):
                    email = email_input
                    break
                else:
                    raise ValueError
            except ValueError:
                console.print("[bold red]Помилка:[/bold red] Некоректна електронна пошта. Спробуйте ще раз.")
        # Додатково: питаємо користувача про день народження і дозволяємо різні формати
        while True:
            try:
                birthday = input("Дата народження (день-місяць-рік): ")
                birthday_date = parser.parse(birthday).date()
                break  # Якщо парсинг відбувся успішно, виходимо з циклу
            except ValueError:
                console.print("[bold red]Помилка:[/bold red] Некоректний формат дати. Спробуйте ще раз.")
        self.add_contact(name, address, phone, email, birthday_date)
        self.dump()

    # Додавання контакту
    def add_contact(self, name, address, phone, email, birthday):
        # Перевірка наявності контакту з такими номерами телефонів в книзі контактів
        existing_contact = next((contact for contact in self.contacts if set(contact.phone) == set(phone)), None)
        if existing_contact:
            console.print(f"[bold red]Помилка:[/bold red] Контакт з такими номерами телефонів вже існує.")
            return
        # Додавання нового контакту до книги контактів
        new_contact = Contact(name, address, phone, email, birthday)
        self.contacts.append(new_contact)
        console.print(f"[green]Контакт {name} успішно доданий до книги контактів.[/green]")
        self.dump()

    #Список контактів 
    def list_contacts(self):
        """
        Виводить список контактів у вигляді таблиці.
        """
        if not self.contacts:
            console.print("[red]У вас немає жодних контактів в книзі.[/red]")
        else:
            table = Table(title="Список контактів")
            table.add_column("[blue]Ім'я[/blue]")
            table.add_column("[green]Адреса[/green]")
            table.add_column("[yellow]Телефон[/yellow]")
            table.add_column("[cyan]Електронна пошта[/cyan]")
            table.add_column("[magenta]День народження[/magenta]")

            for contact in self.contacts:
                birthday_str = contact.birthday.strftime('%d-%m-%Y')
                table.add_row(
                    Text(contact.name, style="blue"),
                    Text(contact.address, style="green"),
                    Text(contact.phone, style="yellow"), 
                    Text(contact.email, style="cyan"),
                    Text(birthday_str, style="magenta")
                )

            # Встановлення відстані від верхнього краю екрану
            console.print("\n" * 2)
            console.print(table, justify="center") 
                       
    def search_contacts(self, query=None):
        """
        Шукає контакти, які відповідають введеному запиту.
        Args:
            query (str, optional): Запит для пошуку контактів. За замовчуванням - None.
        Returns:
            Contact or None: Знайдений контакт або None, якщо нічого не знайдено.
        """

        if query is None:
            query = input("Введіть запит для пошуку контактів: ")

        matching_contacts = [contact for contact in self.contacts if query.lower() in contact.name.lower()]

        if matching_contacts:
            console.print(f"[bold green]Результати пошуку:[/bold green]")

            # Виведення знайдених контактів в таблицю
            table = Table(title="Знайдені контакти")
            table.add_column("[blue]Ім'я[/blue]", justify="center")
            table.add_column("[green]Адреса[/green]", justify="center")
            table.add_column("[yellow]Телефон[/yellow]", justify="center")
            table.add_column("[cyan]Електронна пошта[/cyan]", justify="center")
            table.add_column("[magenta]День народження[/magenta]", justify="center")

            for contact in matching_contacts:
                table.add_row(
                    Text(contact.name, style="blue"),
                    Text(contact.address, style="green"),
                    Text(contact.phone, style="yellow"),
                    Text(contact.email, style="cyan"),
                    Text(contact.birthday.strftime('%d-%m-%Y'), style="magenta")
                )

            # Центрування таблиці
            console.print(table, justify="center")

            # Повернення першого знайденого контакту
            return matching_contacts[0] if matching_contacts else None
        else:
            console.print(f"[red]Немає результатів пошуку для запиту: {query}[/red]")
            return None


    def edit_contact(self, contact):
        if contact is None:
            console.print("[bold red]Помилка:[/bold red] Контакт не знайдено.")
            return

        console.print(f"[bold]Редагування контакту: {contact.name}[/bold]")

        # Редагування імені
        new_name = input(f"Теперішнє ім'я: {contact.name}\nВведіть нове ім'я (або Enter, щоб залишити без змін): ")
        if new_name:
            contact.name = new_name

        # Редагування адреси
        new_address = input(f"Теперішня адреса: {contact.address}\nВведіть нову адресу (або Enter, щоб залишити без змін): ")
        if new_address:
            contact.address = new_address

        # Редагування номеру телефону
        new_phone = input(f"Теперішній телефон: {contact.phone}\nВведіть новий телефон (або Enter, щоб залишити без змін): ")
        if new_phone:
            if self.is_valid_phone(new_phone):
                contact.phone = new_phone   
            else:
                console.print("[bold red]Помилка:[/bold red] Некоректний номер телефону.")

        # Редагування пошти
        new_email = input(f"Теперішня електронна пошта: {contact.email}\nВведіть нову пошту (або Enter, щоб залишити без змін): ")
        if new_email:
            if self.is_valid_email(new_email):
                contact.email = new_email
            else:
                console.print("[bold red]Помилка:[/bold red] Некоректна електронна пошта.")

        # Редагування дня народження
        new_birthday = input(
            f"Теперішній день народження: {contact.birthday.strftime('%d-%m-%Y')}\nВведіть новий день народження (або Enter, щоб залишити без змін): ")
        if new_birthday:     
            try:
                new_birthday_date = parser.parse(new_birthday).date()   
                contact.birthday = new_birthday_date
            except ValueError:
                console.print("[bold red]Помилка:[/bold red] Некоректний формат дати. Залишено попередню дату.")
        console.print(f"[green]Контакт {contact.name} успішно відредаговано.[/green]")
        self.dump()


    # Видалення контакту
    def delete_contact(self, contact=None):
        """
        Видаляє вказаний контакт або викликає search_contacts для вибору контакту.
        Args:
            contact (Contact, optional): Контакт для видалення. За замовчуванням - None.
        """
        if contact is None:
            # Якщо contact не передано, спробуйте викликати search_contacts для вибору контакту
            contact = self.search_contacts()

        if contact in self.contacts:
            contact_name = contact.name
            self.contacts.remove(contact)
            console.print(f"[green]Контакт {contact_name} успішно видалено.[/green]")
        else:
            console.print("[red]Помилка: Контакт не знайдено або не вибрано для видалення.[/red]")
        self.dump()

    def upcoming_birthdays(self, days):
        """
        Виводить інформацію про найближчі дні народження у наступні визначені дні.
        Args:
            days (int): Кількість днів для виводу інформації про найближчі дні народження.
        """
        today = datetime.today().date()
        upcoming_birthdays = [contact for contact in self.contacts if today < self.get_next_birthday(contact) <= today + timedelta(days)]
        if not upcoming_birthdays:
            console.print(f'[yellow]У {days} днів немає найближчих днів народження.[/yellow]')
        else:
            table = Table(title=f'Дні народження у наступні {days} днів')
            table.add_column("[blue]Ім'я[/blue]")
            table.add_column("[magenta]Дата народження[/magenta]")
            table.add_column("[yellow]Залишилося днів[/yellow]")
            table.add_column("[green]Вік[/green]")

            for contact in upcoming_birthdays:
                remaining_days = (self.get_next_birthday(contact) - today).days
                birthday_str = contact.birthday.strftime('%d-%m-%Y')

                age = today.year - contact.birthday.year + 1 - ((today.month, today.day) < (contact.birthday.month, contact.birthday.day))

                table.add_row(
                Text(contact.name, style="blue"),
                Text(birthday_str, style="magenta"),
                Text(str(remaining_days), style="yellow"),
                Text(str(age), style="green")
                )
            # Встановлення відстані від верхнього краю екрану
            console.print("\n" * 2)
            console.print(table, justify="center")
            
            
    def get_next_birthday(self, contact):
        """
        Отримує дату наступного дня народження для вказаного контакту.
        Args:
            contact (Contact): Контакт, для якого потрібно отримати наступний день народження.
        Returns:
            datetime.date: Дата наступного дня народження.
        """
        today = datetime.today().date()

        # Перевірка, чи birthday є рядком, і якщо так, конвертувати його у datetime.date
        if isinstance(contact.birthday, str):
            birthday = datetime.strptime(contact['birthday'], "%d-%m-%Y").date()
        else:
            birthday = contact.birthday
        next_birthday = birthday.replace(year=today.year)

        if today > date(today.year, birthday.month, birthday.day):
            next_birthday = next_birthday.replace(year=today.year + 1)

        return next_birthday