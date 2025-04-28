from datetime import datetime, timedelta


class Homework:
    def __init__(self, text, days):
        self.text = text
        self.deadline = timedelta(days=days)
        self.created = datetime.now()

    def is_active(self):
        return datetime.now() < self.created + self.deadline


class Student:
    def __init__(self, last_name, first_name):
        self.last_name = last_name
        self.first_name = first_name

    def do_homework(self, homework):
        if homework.is_active():
            print(f"{self.first_name} {self.last_name} сделал задание: {homework.text}")
            return homework
        else:
            print("You are late")
            return None


class Teacher:
    def __init__(self, last_name, first_name):
        self.last_name = last_name
        self.first_name = first_name

    @staticmethod
    def create_homework(text, days):
        return Homework(text, days)


# Пример использования

teacher = Teacher("Иванов", "Иван")
student = Student("Петров", "Роман")

hw1 = teacher.create_homework("Сделать упражнение 1", 3)
hw2 = teacher.create_homework("Сделать упражнение 2", 0)  # Просроченное

hw2.created -= timedelta(days=1)

student.do_homework(hw1)  # активное задание
student.do_homework(hw2)  # просроченное