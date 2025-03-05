from page.core import task_manager, task, execute_task, get_all_tasks

@task()
def task_a():
    print("This is task A")
