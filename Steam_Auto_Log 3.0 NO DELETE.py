import tkinter as tk
import webbrowser
import pyautogui
import time
import json
import os
import pyperclip

def open_steam_registration():
    url = 'https://store.steampowered.com/join/'
    webbrowser.open(url)

def on_open_steam():
    open_steam_registration()

def on_submit_email():
    selected_email = email_var.get()
    if selected_email:
        time.sleep(5)
        pyautogui.click(100, 300)  # Координаты могут отличаться, настрой их под себя
        pyautogui.typewrite(selected_email)
        
        pyautogui.press('tab')
        pyautogui.typewrite(selected_email)
        
        pyautogui.press('tab')
        pyautogui.typewrite(selected_email)
        
        time.sleep(3)  # Демонстрационная задержка (можно убрать или уменьшить)
    else:
        result_label.config(text="Пожалуйста, выберите почту для заполнения.")

def load_emails():
    desktop_path = os.path.join(os.path.expanduser("~"), "Desktop")
    file_path = os.path.join(desktop_path, "emails.json")

    if os.path.exists(file_path):
        with open(file_path, "r") as f:
            try:
                emails = json.load(f)
                return emails
            except json.JSONDecodeError:
                return []
    else:
        return []

def save_emails():
    desktop_path = os.path.join(os.path.expanduser("~"), "Desktop")
    file_path = os.path.join(desktop_path, "emails.json")

    with open(file_path, "w") as f:
        json.dump(emails, f, indent=4)

def add_email():
    new_email = new_email_entry.get().strip()
    if new_email:
        if new_email not in emails:
            emails.append(new_email)
            save_emails()
            result_label.config(text="Почта добавлена.")
            new_email_entry.delete(0, tk.END)
        else:
            result_label.config(text="Такая почта уже существует.")
    else:
        result_label.config(text="Пожалуйста, введите почту для добавления.")

def show_emails():
    email_listbox.delete(0, tk.END)
    for email in emails:
        email_listbox.insert(tk.END, email)

def copy_selected_email(event):
    selected_email = email_listbox.get(email_listbox.curselection())
    pyperclip.copy(selected_email)
    result_label.config(text=f"Почта '{selected_email}' скопирована в буфер обмена.")

def get_last_number(string, prefix):
    number = string[len(prefix):]
    try:
        return int(number)
    except ValueError:
        return 0

def create_accounts():
    try:
        num_accounts = int(num_accounts_entry.get())
        accounts = {}
        new_accounts = {}

        desktop_path = os.path.join(os.path.expanduser("~"), "Desktop")
        file_path = os.path.join(desktop_path, "Steam.json")

        if os.path.exists(file_path):
            with open(file_path, "r") as f:
                try:
                    accounts = json.load(f)
                except json.JSONDecodeError:
                    accounts = {}

        base_username = "Login1Login1"
        base_password = "Pass1Pass1"

        if custom_username_entry.get():
            base_username = custom_username_entry.get()
        
        if custom_password_entry.get():
            base_password = custom_password_entry.get()

        if accounts:
            last_username_number = max(get_last_number(username, base_username) for username in accounts.keys())
            last_password_number = max(get_last_number(password, base_password) for password in accounts.values())
        else:
            last_username_number = 0
            last_password_number = 0

        for i in range(1, num_accounts + 1):
            new_username = f"{base_username}{last_username_number + i}"
            new_password = f"{base_password}{last_password_number + i}"

            if new_username not in accounts:
                accounts[new_username] = new_password
                new_accounts[new_username] = new_password

        with open(file_path, "w") as f:
            json.dump(accounts, f, indent=4)

        if new_accounts:
            for username in new_accounts.keys():
                pyperclip.copy(username)
                result_label.config(text=f"Логин скопирован в буфер обмена: {username}")
                root.update()
                time.sleep(2)
            
            global last_created_password
            last_created_password = new_password  # Сохраняем последний созданный пароль

            result_label.config(text=f"Создано {len(new_accounts)} новых аккаунтов. Логины и пароли добавлены в файл.")
        else:
            result_label.config(text="Нет новых аккаунтов для создания. Все логины уже существуют.")
            
    except ValueError:
        result_label.config(text="Пожалуйста, введите корректное количество аккаунтов.")

def copy_last_password():
    if last_created_password:
        pyperclip.copy(last_created_password)
        result_label.config(text=f"Последний пароль скопирован в буфер обмена: {last_created_password}")
    else:
        result_label.config(text="Пароль еще не создан.")

def clear_file():
    desktop_path = os.path.join(os.path.expanduser("~"), "Desktop")
    file_path = os.path.join(desktop_path, "Steam.json")
    
    if os.path.exists(file_path):
        with open(file_path, "w") as f:
            pass
        result_label.config(text="Файл Steam.json очищен.")
    else:
        result_label.config(text="Файл Steam.json не найден.")

#def delete_file():
 #   desktop_path = os.path.join(os.path.expanduser("~"), "Desktop")
  #  file_path = os.path.join(desktop_path, "Steam.json")
    
   # if os.path.exists(file_path):
    #    os.remove(file_path)
     #   result_label.config(text="Файл Steam.json удален.")
    #else:
     #   result_label.config(text="Файл Steam.json не найден.")

# Создание окна приложения
root = tk.Tk()
root.title("Steam Registration Helper")

# Интерфейс
tk.Label(root, text="Введите новую почту:").pack(pady=10)
new_email_entry = tk.Entry(root, width=30)
new_email_entry.pack(pady=5)

add_email_button = tk.Button(root, text="Добавить почту", command=add_email)
add_email_button.pack(pady=10)

show_emails_button = tk.Button(root, text="Показать все почты", command=show_emails)
show_emails_button.pack(pady=10)

email_listbox = tk.Listbox(root, width=50, height=10)
email_listbox.pack(pady=10)
email_listbox.bind("<<ListboxSelect>>", copy_selected_email)

# Поля для пользовательского логина и пароля (необязательные)
tk.Label(root, text="Введите свой логин (опционально):").pack(pady=10)
custom_username_entry = tk.Entry(root, width=30)
custom_username_entry.pack(pady=5)

tk.Label(root, text="Введите свой пароль (опционально):").pack(pady=10)
custom_password_entry = tk.Entry(root, width=30)
custom_password_entry.pack(pady=5)

# Ввод количества аккаунтов
tk.Label(root, text="Сколько аккаунтов создать:").pack(pady=10)

num_accounts_entry = tk.Entry(root, width=10)
num_accounts_entry.pack(pady=5)

create_accounts_button = tk.Button(root, text="Создать Аккаунты", command=create_accounts)
create_accounts_button.pack(pady=10)

# Кнопка для копирования последнего пароля
copy_password_button = tk.Button(root, text="Копировать последний пароль", command=copy_last_password)
copy_password_button.pack(pady=5)

# Добавление кнопок для очистки и удаления файла
#clear_file_button = tk.Button(root, text="Очистить файл", command=clear_file)
#clear_file_button.pack(pady=5)

#delete_file_button = tk.Button(root, text="Удалить файл", command=delete_file)
#delete_file_button.pack(pady=5)

# Результат
result_label = tk.Label(root, text="")
result_label.pack(pady=10)

# Переменная для хранения последнего созданного пароля
last_created_password = ""

# Загрузка почт из файла
emails = load_emails()

# Запуск основного цикла
root.mainloop()
