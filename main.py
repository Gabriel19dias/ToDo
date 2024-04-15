import flet
from flet import (
    Checkbox,
    FloatingActionButton,
    IconButton,
    OutlinedButton,
    Column,
    Page,
    Row,
    Tabs,
    Tab,
    Text,
    TextField,
    UserControl,
    colors,
    icons,
)

class Task(UserControl):
    def __init__(self, task_name, task_status_change, task_delete):
        super().__init__()
        self.completed = False
        self.task_name = task_name
        self.task_status_change = task_status_change
        self.task_delete = task_delete

    def build(self):
        self.display_task = Checkbox(
            value=self.completed, label=self.task_name, on_change=self.status_changed
        )
        self.edit_name = TextField(expand=1)  # Caixa de texto para edição da tarefa

        self.display_view = Row(
            alignment="spaceBetween",
            vertical_alignment="center",
            controls=[
                self.display_task,
                Row(
                    spacing=0,
                    controls=[
                        IconButton(
                            icon=icons.CREATE_OUTLINED,
                            tooltip="Editar Tarefa",
                            on_click=self.edit_clicked,
                            icon_color=colors.GREEN,
                        ),
                        IconButton(
                            icon=icons.DELETE_OUTLINED,
                            tooltip="Deletar Tarefa",
                            on_click=self.delete_clicked,
                            icon_color=colors.RED,
                        ),
                    ],
                ),
            ],
        )

        self.edit_view = Row(
            visible=False,
            alignment="spaceBetween",
            vertical_alignment="Center",
            controls=[
                IconButton(
                    icon=icons.DONE_OUTLINED,
                    icon_color=colors.GREEN,
                    tooltip="Atualizar tarefa",
                    on_click=self.save_clicked,
                )
            ]
        )
        return Column(controls=[self.display_view, self.edit_view])

    def edit_clicked(self, e):
        self.edit_name.value = self.task_name
        self.display_view.visible = False
        self.edit_view.visible = True
        self.edit_name.focus()  # Focar na caixa de texto para edição
        self.update()

    def save_clicked(self, e):
        self.task_name = self.edit_name.value
        self.display_task.label = self.task_name
        self.display_view.visible = True
        self.edit_view.visible = False
        self.update()

    def delete_clicked(self, e):
        self.task_delete(self)

    def status_changed(self, e):
        self.completed = self.display_task.value
        self.task_status_change(self)
        self.update()


class TodoApp(UserControl):
    def build(self):
        self.new_task = TextField(
            hint_text="Escreva a tarefa que deseja adicionar",
            expand=True,
            on_submit=self.add_clicked,
        )
        self.tasks = Column()
        self.filter = Tabs(
            selected_index=0,
            on_change=self.tabs_changed,
            tabs=[
                Tab(text="Todas tarefas"),
                Tab(text="Tarefas Ativas"),
                Tab(text="Tarefas completadas"),
            ],
        )
        self.items_left = Text("0 tarefas adicionadas")

        return Column(
            width=600,
            controls=[
                # Título da aplicação
                Row(
                    [Text(value="Tarefas", style="headlineMedium")],
                    alignment="center"
                ),
                Row(
                    # Input para adicionar tarefa
                    controls=[
                        self.new_task,
                        FloatingActionButton(
                            icon=icons.ADD, on_click=self.add_clicked
                        ),
                    ]
                ),
                Column(
                    spacing=20,
                    controls=[
                        self.filter,
                        self.tasks,
                        Row(
                            alignment="spaceBetween",
                            vertical_alignment="center",
                            controls=[
                                self.items_left,
                                OutlinedButton(
                                    text="Limpar as tarefas completadas".upper(),
                                    on_click=self.clear_clicked,
                                ),
                            ],
                        ),
                    ],
                ),
            ],
        )

    def add_clicked(self, e):
        task_name = self.new_task.value
        if task_name:
            task = Task(task_name, self.task_status_change, self.task_delete)
            self.tasks.controls.append(task)
            self.new_task.value = ""
            self.new_task.focus()
            self.update()

    def task_status_change(self, task):
        self.update()

    def task_delete(self, task):
        self.tasks.controls.remove(task)
        self.update()

    def tabs_changed(self, e):
        self.update()

    def clear_clicked(self, e):
        for task in self.tasks.controls[:]:
            if task.completed:
                self.task_delete(task)

    def update(self):
        status = self.filter.tabs[self.filter.selected_index].text.lower()
        count = sum(1 for task in self.tasks.controls if self.filter_task(task, status))
        self.items_left.value = f"{count} tarefas adicionadas"
        super().update()

    def filter_task(self, task, status):
        if status == "todas tarefas":
            return True
        elif status == "tarefas ativas":
            return not task.completed
        elif status == "tarefas completadas":
            return task.completed
        return False


def main(page: Page):
    page.title = "Tarefas"
    page.horizontal_alignment = "center"
    page.scroll = "adaptive"
    page.update()

    app = TodoApp()
    page.add(app)


flet.app(target=main)
