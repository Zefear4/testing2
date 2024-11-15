import unittest
from datetime import datetime, timedelta
from main import Task, TaskManager

class TestTask(unittest.TestCase):

    def test_task_creation(self):
        # Тестируем создание задачи с корректными данными
        task = Task(name='Тестовая задача', due_date='2023-12-31')
        self.assertEqual(task.name, 'Тестовая задача')
        self.assertEqual(task.description, '')
        self.assertEqual(task.due_date, '2023-12-31')
        self.assertFalse(task.completed)

    def test_task_due_date_validation(self):
        # Тестируем валидацию даты выполнения
        with self.assertRaises(ValueError):
            Task(name='Некорректная дата', due_date='31-12-2023')

    def test_task_complete(self):
        # Тестируем метод complete
        task = Task(name='Выполнить задачу')
        task.complete()
        self.assertTrue(task.completed)

    def test_task_is_completed(self):
        # Тестируем метод is_completed
        task = Task(name='Проверить выполнение')
        self.assertFalse(task.is_completed())
        task.complete()
        self.assertTrue(task.is_completed())

    def test_task_postpone(self):
        # Тестируем метод postpone
        original_date = '2023-12-01'
        task = Task(name='Отложить задачу', due_date=original_date)
        task.postpone(5)
        new_due_date = (datetime.strptime(original_date, '%Y-%m-%d') + timedelta(days=5)).strftime('%Y-%m-%d')
        self.assertEqual(task.due_date, new_due_date)

    def test_task_postpone_without_due_date(self):
        # Тестируем откладывание задачи без установленной даты выполнения
        task = Task(name='Без даты')
        with self.assertRaises(ValueError):
            task.postpone(3)

class TestTaskManager(unittest.TestCase):

    def setUp(self):
        # Создаем несколько задач для использования в тестах
        self.task1 = Task(name='Задача 1', due_date='2023-12-01')
        self.task2 = Task(name='Задача 2', due_date='2023-12-02')
        self.manager = TaskManager()
        self.manager.add_task(self.task1)
        self.manager.add_task(self.task2)

    def test_add_task(self):
        # Тестируем добавление задачи
        task = Task(name='Новая задача')
        self.manager.add_task(task)
        self.assertIn(task, self.manager.get_tasks())

    def test_get_tasks(self):
        # Тестируем получение списка задач
        tasks = self.manager.get_tasks()
        self.assertEqual(len(tasks), 2)
        self.assertIn(self.task1, tasks)
        self.assertIn(self.task2, tasks)

    def test_remove_task(self):
        # Тестируем удаление задачи
        self.manager.remove_task('Задача 1')
        tasks = self.manager.get_tasks()
        self.assertEqual(len(tasks), 1)
        self.assertNotIn(self.task1, tasks)

    def test_from_task_names(self):
        # Тестируем создание менеджера задач из списка имен
        names = ['Задача А', 'Задача Б']
        manager = TaskManager.from_task_names(names)
        tasks = manager.get_tasks()
        self.assertEqual(len(tasks), 2)
        self.assertEqual(tasks[0].name, 'Задача А')
        self.assertEqual(tasks[1].name, 'Задача Б')

    def test_save_to_file_and_load_from_file(self):
        # Тестируем сохранение в файл и загрузку из файла
        filename = '../test_tasks.json'
        self.manager.save_to_file(filename)
        new_manager = TaskManager.load_from_file(filename)
        tasks = new_manager.get_tasks()
        self.assertEqual(len(tasks), 2)
        self.assertEqual(tasks[0].name, self.task1.name)
        self.assertEqual(tasks[1].name, self.task2.name)

    def test_load_from_nonexistent_file(self):
        # Тестируем загрузку из несуществующего файла
        filename = 'nonexistent.json'
        manager = TaskManager.load_from_file(filename)
        self.assertEqual(len(manager.get_tasks()), 0)

    def test_complete_task_in_manager(self):
        # Тестируем выполнение задачи через менеджер
        self.task1.complete()
        self.assertTrue(self.task1.completed)

    def test_postpone_task_in_manager(self):
        # Тестируем откладывание задачи через менеджер
        original_date = self.task2.due_date
        self.task2.postpone(2)

        tasks = self.manager.get_tasks()
        updated_task = next((task for task in tasks if task.name == self.task2.name), None)
        self.assertIsNotNone(updated_task)

        new_due_date = (datetime.strptime(original_date, '%Y-%m-%d') + timedelta(days=2)).strftime('%Y-%m-%d')
        self.assertEqual(updated_task.due_date, new_due_date)

class TestAcceptance(unittest.TestCase):

    def test_create_postpone_and_complete_task(self):
        """Создать, отложить и отметить задачу как выполненную."""
        manager = TaskManager()
        task_name = "Тестовая задача"
        due_date = "2024-03-10"

        manager.add_task(Task(name=task_name, due_date=due_date))
        task = manager.get_tasks()[0]

        self.assertEqual(task.name, task_name)
        self.assertEqual(task.due_date, due_date)
        self.assertFalse(task.completed)

        manager.get_tasks()[0].postpone(5)
        updated_due_date = (datetime.strptime(due_date, '%Y-%m-%d') + timedelta(days=5)).strftime('%Y-%m-%d')
        self.assertEqual(task.due_date, updated_due_date)


        manager.get_tasks()[0].complete()
        self.assertTrue(task.completed)


    def test_load_large_number_of_tasks(self):
        """Загрузить большое количество задач."""
        num_tasks = 1000
        filename = "large_tasks.json"
        manager = TaskManager()

        # Создаем и сохраняем большое количество задач
        for i in range(num_tasks):
            manager.add_task(Task(name=f"Задача {i+1}"))
        manager.save_to_file(filename)


        start_time = datetime.now()
        loaded_manager = TaskManager.load_from_file(filename)
        end_time = datetime.now()
        load_time = end_time - start_time

        self.assertEqual(len(loaded_manager.get_tasks()), num_tasks)
        self.assertLess(load_time, timedelta(seconds=5), "Загрузка заняла слишком много времени")

class TestAcceptance(unittest.TestCase):

    def test_load_large_number_of_tasks(self):
        """Загрузить большое количество задач."""
        num_tasks = 1000
        filename = "large_tasks.json"
        manager = TaskManager()

        # Создаем и сохраняем большое количество задач
        for i in range(num_tasks):
            manager.add_task(Task(name=f"Задача {i+1}"))
        manager.save_to_file(filename)


        start_time = datetime.now()
        loaded_manager = TaskManager.load_from_file(filename)
        end_time = datetime.now()
        load_time = end_time - start_time

        self.assertEqual(len(loaded_manager.get_tasks()), num_tasks)
        self.assertLess(load_time, timedelta(seconds=5), "Загрузка заняла слишком много времени")

if __name__ == '__main__':
    unittest.main()
