import tkinter as tk
from tkinter import messagebox

# 1. Модель даних Student із механізмом Data Binding
class Student:
    def __init__(self, name: str, age: int, grade: float):
        # Використовуємо змінні Tkinter для зв'язування даних (Data Binding)
        self.name = tk.StringVar(value=name)
        self.age = tk.StringVar(value=str(age))
        self.grade = tk.StringVar(value=str(grade))
        
        # Змінна для автоматичного відображення зведеної картки студента
        self.summary = tk.StringVar()
        
        # Прив'язуємо спостерігачі (observers) до зміни кожної властивості
        self.name.trace_add("write", self._update_summary)
        self.age.trace_add("write", self._update_summary)
        self.grade.trace_add("write", self._update_summary)
        
        # Початкове формування тексту
        self._update_summary()

    def _update_summary(self, *args):
        """Автоматично оновлює рядок стану при зміні будь-якої властивості моделі."""
        self.summary.set(
            f"Студент: {self.name.get() or '—'} | "
            f"Вік: {self.age.get() or '—'} р. | "
            f"Оцінка: {self.grade.get() or '—'} балів"
        )

# 2. Графічний інтерфейс (GUI)
root = tk.Tk()
root.title("Практична робота №12 — Data Binding")
root.geometry("460x330")
root.resizable(False, False)

# Створюємо екземпляр моделі з початковими даними
student = Student("Олександр Коваленко", 19, 92.5)

# Блок автоматичного відображення даних (One-Way Binding до Label)
info_frame = tk.LabelFrame(root, text="Поточний стан об'єкта (оновлюється автоматично)", padx=10, pady=10)
info_frame.pack(fill=tk.X, padx=15, pady=10)

# Елемент Label напряму зв'язаний із властивістю student.summary через textvariable
lbl_summary = tk.Label(info_frame, textvariable=student.summary, font=("Arial", 10, "bold"), fg="#1a5276")
lbl_summary.pack()

# Блок редагування властивостей (Two-Way Binding через Entry)
edit_frame = tk.LabelFrame(root, text="Редагування властивостей моделі (Two-Way Binding)", padx=10, pady=10)
edit_frame.pack(fill=tk.X, padx=15, pady=5)

tk.Label(edit_frame, text="Ім'я (Name):").grid(row=0, column=0, sticky=tk.W, pady=5)
entry_name = tk.Entry(edit_frame, textvariable=student.name, width=32)
entry_name.grid(row=0, column=1, padx=10, pady=5)

tk.Label(edit_frame, text="Вік (Age):").grid(row=1, column=0, sticky=tk.W, pady=5)
entry_age = tk.Entry(edit_frame, textvariable=student.age, width=32)
entry_age.grid(row=1, column=1, padx=10, pady=5)

tk.Label(edit_frame, text="Оцінка (Grade 0-100):").grid(row=2, column=0, sticky=tk.W, pady=5)
entry_grade = tk.Entry(edit_frame, textvariable=student.grade, width=32)
entry_grade.grid(row=2, column=1, padx=10, pady=5)

# 3. Перевірка коректності введених значень (валідація)
def validate_and_confirm():
    name_val = student.name.get().strip()
    age_str = student.age.get().strip()
    grade_str = student.grade.get().strip()

    if not name_val:
        messagebox.showerror("Помилка валідації", "Ім'я студента не може бути порожнім!")
        return

    try:
        age_val = int(age_str)
        if not (14 <= age_val <= 100):
            raise ValueError
    except ValueError:
        messagebox.showerror("Помилка валідації", "Вік має бути цілим числом від 14 до 100!")
        return

    try:
        grade_val = float(grade_str)
        if not (0 <= grade_val <= 100):
            raise ValueError
    except ValueError:
        messagebox.showerror("Помилка валідації", "Оцінка має бути числом у межах від 0 до 100!")
        return

    messagebox.showinfo("Успіх", "Усі дані моделі коректні та збережені!")

def reset_data():
    """Програмна зміна властивостей моделі — GUI оновиться сам."""
    student.name.set("Марія Шевченко")
    student.age.set("20")
    student.grade.set("98.0")

btn_frame = tk.Frame(root, pady=10)
btn_frame.pack()

tk.Button(btn_frame, text="Перевірити дані", command=validate_and_confirm, width=18, bg="#d4efdf").grid(row=0, column=0, padx=8)
tk.Button(btn_frame, text="Змінити модель кодом", command=reset_data, width=20).grid(row=0, column=1, padx=8)

root.mainloop()
