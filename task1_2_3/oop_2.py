from datetime import datetime, timedelta
from collections import defaultdict


class DeadlineError(Exception):
    """Вызывается, если задание просрочено."""
    pass


class Person:
    def __init__(self, last_name: str, first_name: str) -> None:
        self.last_name = last_name
        self.first_name = first_name


class Homework:
    def __init__(self, text: str, days: int) -> None:
        self.text = text
        self.deadline = timedelta(days=days)
        self.created = datetime.now()

    def is_active(self) -> bool:
        return datetime.now() < self.created + self.deadline


class HomeworkResult:
    def __init__(self, author: Person, homework: Homework, solution: str) -> None:
        if not isinstance(homework, Homework):
            raise TypeError('You gave a not Homework object')
        self.author = author
        self.homework = homework
        self.solution = solution
        self.created = datetime.now()


class Student(Person):
    def do_homework(self, homework: Homework, solution: str) -> HomeworkResult:
        if not homework.is_active():
            raise DeadlineError('You are late')
        return HomeworkResult(self, homework, solution)


class Teacher(Person):
    homework_done = defaultdict(set)

    @staticmethod
    def create_homework(text: str, days: int) -> Homework:
        return Homework(text, days)

    @classmethod
    def check_homework(cls, result: HomeworkResult) -> bool:
        if len(result.solution) > 5:
            cls.homework_done[result.homework].add(result)
            return True
        return False

    @classmethod
    def reset_results(cls, homework: Homework = None) -> None:
        if homework is None:
            cls.homework_done.clear()
        else:
            cls.homework_done.pop(homework, None)


if __name__ == '__main__':
    opp_teacher = Teacher('Daniil', 'Shadrin')
    advanced_teacher = Teacher('Aleksandr', 'Smetanin')

    lazy_student = Student('Roman', 'Petrov')
    good_student = Student('Lev', 'Sokolov')

    oop_hw = opp_teacher.create_homework('Learn OOP', 1)
    docs_hw = opp_teacher.create_homework('Read documentation', 5)

    try:
        result_1 = good_student.do_homework(oop_hw, 'I have done this hw')
        result_2 = good_student.do_homework(docs_hw, 'I have done this hw too')
        result_3 = lazy_student.do_homework(docs_hw, 'done')
    except DeadlineError as e:
        print(e)

    try:
        HomeworkResult(good_student, 'not_homework_object', 'solution')
    except Exception as e:
        print(e)

    opp_teacher.check_homework(result_1)
    temp_1 = opp_teacher.homework_done

    advanced_teacher.check_homework(result_1)
    temp_2 = Teacher.homework_done

    assert temp_1 == temp_2

    opp_teacher.check_homework(result_2)
    opp_teacher.check_homework(result_3)

    print('\nСохранённые результаты:')
    for hw, results in Teacher.homework_done.items():
        print(f"{hw.text}:")
        for res in results:
            print(f"  {res.author.first_name} {res.author.last_name} -> {res.solution}")

    Teacher.reset_results()

    print('\nПосле сброса:')
    print(Teacher.homework_done)