import json
import os
from datetime import datetime

from PyQt5.QtCore import QEasingCurve, QPropertyAnimation, QDate, QTime, Qt
from PyQt5.QtGui import QColor, QFont
from PyQt5.QtWidgets import (
    QApplication,
    QCheckBox,
    QComboBox,
    QDateEdit,
    QDialog,
    QDialogButtonBox,
    QFrame,
    QGraphicsDropShadowEffect,
    QGridLayout,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QListWidget,
    QListWidgetItem,
    QMainWindow,
    QMessageBox,
    QLayout,
    QPushButton,
    QProgressBar,
    QScrollArea,
    QSizePolicy,
    QSpacerItem,
    QSpinBox,
    QTimeEdit,
    QVBoxLayout,
    QWidget,
)

from logic import (
    add_deadline,
    add_modules,
    add_task,
    delete_task,
    edit_deadline,
    edit_task,
    file_exists,
    get_deadlines,
    get_event_by_date,
    get_upcoming_events,
    retrieve_deadline_details,
    retrieve_event_details,
    save_reminder_state,
    working_checkbox_path,
    working_modules_path,
    working_reminder_path,
)
from main import authentication


MODULE_LABEL_MODE_PATH = os.path.join(os.path.dirname(working_modules_path), "module_label_mode.json")


APP_STYLE = """
QMainWindow {
    background: #081912;
}
QDialog {
    background: #7fa08a;
}
QWidget {
    color: #163127;
    font-family: "Avenir Next", "Helvetica Neue", sans-serif;
}
#Root {
    background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
        stop:0 #06140e, stop:0.25 #0a1f16, stop:0.58 #113124, stop:1 #1b4a37);
}
#HeaderCard {
    background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
        stop:0 #163f2f, stop:0.35 #123526, stop:0.72 #0f2b1f, stop:1 #0a1d15);
    border-radius: 26px;
}
#ProgressCard {
    background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
        stop:0 #214f3c, stop:0.45 #173a2b, stop:1 #10261c);
    border: 1px solid rgba(86, 132, 103, 0.45);
    border-radius: 20px;
}
#Card {
    background: rgba(124, 156, 133, 0.98);
    border: 1px solid rgba(102, 134, 112, 0.7);
    border-radius: 22px;
}
#MutedCard {
    background: rgba(111, 143, 120, 0.96);
    border-radius: 18px;
}
QLabel[role="eyebrow"] {
    color: #a7d7b8;
    font-size: 13px;
    font-weight: 700;
    letter-spacing: 0.08em;
    text-transform: uppercase;
}
QLabel[role="heroTitle"] {
    color: #f3fbf5;
    font-size: 34px;
    font-weight: 700;
}
QLabel[role="heroBody"] {
    color: #c0daca;
    font-size: 13px;
}
QLabel[role="sectionTitle"] {
    color: #163127;
    font-size: 24px;
    font-weight: 600;
}
QLabel[role="sectionBody"] {
    color: #5b7468;
    font-size: 12px;
}
QProgressBar {
    border: none;
    border-radius: 999px;
    background: rgba(198, 225, 208, 0.24);
    min-height: 18px;
    max-height: 18px;
    text-align: center;
}
QProgressBar::chunk {
    border-radius: 999px;
    background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
        stop:0 #3d8f68, stop:1 #8bc08e);
}
QPushButton {
    border: none;
    border-radius: 16px;
    padding: 8px 14px;
    min-height: 38px;
    font-size: 12px;
    font-weight: 600;
}
QPushButton[variant="primary"] {
    background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
        stop:0 #3b8c64, stop:1 #72ad7f);
    color: white;
}
QPushButton[variant="primary"]:hover {
    background: #21533d;
}
QPushButton[variant="secondary"] {
    background: #92b19d;
    color: #21533d;
}
QPushButton[variant="secondary"]:hover {
    background: #84a692;
}
QPushButton:disabled {
    background: #95b3a0;
    color: #6d8476;
}
QCheckBox {
    spacing: 12px;
    font-size: 14px;
    font-weight: 500;
    color: #163127;
}
QCheckBox::indicator {
    width: 18px;
    height: 18px;
    border-radius: 9px;
    border: 2px solid #bdd1c3;
    background: transparent;
}
QCheckBox::indicator:checked {
    background: #3b8c64;
    border: 2px solid #3b8c64;
}
QLineEdit, QComboBox, QDateEdit, QTimeEdit, QListWidget, QSpinBox {
    background: #87a691;
    border: 1px solid #6c8d77;
    border-radius: 13px;
    padding: 8px 10px;
    font-size: 12px;
}
QDialog QLineEdit, QDialog QComboBox, QDialog QDateEdit, QDialog QTimeEdit, QDialog QListWidget, QDialog QSpinBox {
    background: #9fb9a8;
    border: 1px solid #7f9e8a;
    border-radius: 13px;
    padding: 8px 10px;
    font-size: 12px;
}
QDialog QComboBox QAbstractItemView,
QDialog QListView,
QDialog QCalendarWidget QWidget,
QDialog QCalendarWidget QAbstractItemView {
    background: #9fb9a8;
    color: #163127;
    selection-background-color: #86a795;
    selection-color: #163127;
}
QDialog QCalendarWidget QToolButton {
    background: #95b3a0;
    color: #163127;
    border: none;
    border-radius: 12px;
    padding: 6px 10px;
}
QDialog QCalendarWidget QMenu {
    background: #9fb9a8;
    color: #163127;
}
QDialog QCalendarWidget QSpinBox {
    background: #9fb9a8;
    color: #163127;
    border: 1px solid #7f9e8a;
    border-radius: 10px;
}
QDialogButtonBox QPushButton {
    background: #95b3a0;
    color: #163127;
    border: none;
    border-radius: 16px;
    padding: 8px 14px;
    min-height: 38px;
    font-size: 12px;
    font-weight: 600;
}
QDialogButtonBox QPushButton:hover {
    background: #a4c0af;
}
QListWidget {
    padding: 6px;
}
QScrollArea {
    border: none;
    background: transparent;
}
QScrollArea > QWidget > QWidget {
    background: transparent;
}
"""


class PlannerWindow(QMainWindow):
    MODULE_COLOURS = {
        "1": "#7986CB",
        "2": "#33B679",
        "3": "#8E24AA",
        "4": "#E67C73",
        "5": "#F6BF26",
        "10": "#2F6FE4",
        "9": "#C45B14",
        "6": "#A13FA0",
        "8": "#7A5FE0",
        "7": "#039BE5",
        "11": "#D50000",
    }

    MODULE_BACKGROUNDS = {
        "1": "#96A0C4",
        "2": "#86B99E",
        "3": "#A88CB1",
        "4": "#B99A96",
        "5": "#BDB174",
        "10": "#87A892",
        "9": "#8FAE99",
        "6": "#97B59F",
        "8": "#9FBAA6",
        "7": "#8AB0BF",
        "11": "#B98989",
    }

    def __init__(self):
        super().__init__()
        self.creds = authentication()
        self.events = []
        self.deadlines = []
        self.upcoming_deadlines = []
        self.task_checkboxes = []
        self.progress_animation = None
        self.module_label_mode = self.load_module_label_mode()

        self.setWindowTitle("Desktop Planner")
        self.resize(1200, 820)
        self.setMinimumSize(1120, 760)
        self.setStyleSheet(APP_STYLE)

        self.root = QWidget(objectName="Root")
        self.setCentralWidget(self.root)
        self.main_layout = QVBoxLayout(self.root)
        self.main_layout.setContentsMargins(22, 18, 22, 18)
        self.main_layout.setSpacing(22)

        self.build_ui()
        self.refresh_dashboard(initial=True)

    def build_ui(self):
        self.header_card = self.create_card(hero=True)
        self.main_layout.addWidget(self.header_card)

        content = QHBoxLayout()
        content.setSpacing(22)
        self.main_layout.addLayout(content, 1)

        self.tasks_card = self.create_card()
        self.sidebar = QVBoxLayout()
        self.sidebar.setContentsMargins(0, 0, 0, 0)
        self.sidebar.setSpacing(22)

        content.addWidget(self.tasks_card, 3)

        sidebar_host = QWidget()
        sidebar_host.setLayout(self.sidebar)
        content.addWidget(sidebar_host, 2)
        content.setStretch(0, 3)
        content.setStretch(1, 2)

        self.actions_card = self.create_card()
        self.modules_card = self.create_card()
        self.sidebar.addWidget(self.actions_card, 1)
        self.sidebar.addWidget(self.modules_card, 1)

        self.build_header_card()
        self.build_tasks_card()
        self.build_actions_card()
        self.build_modules_card()

    def create_card(self, hero=False):
        card = QFrame()
        card.setObjectName("HeaderCard" if hero else "Card")
        shadow = QGraphicsDropShadowEffect()
        shadow.setBlurRadius(34)
        shadow.setOffset(0, 12)
        shadow.setColor(QColor(5, 18, 12, 90))
        card.setGraphicsEffect(shadow)
        return card

    def make_button(self, text, variant, handler, enabled=True):
        button = QPushButton(text)
        button.setProperty("variant", variant)
        button.setEnabled(enabled)
        button.clicked.connect(handler)
        button.style().unpolish(button)
        button.style().polish(button)
        return button

    def make_section_header(self, title, body):
        wrapper = QWidget()
        layout = QVBoxLayout(wrapper)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(4)

        title_label = QLabel(title)
        title_label.setProperty("role", "sectionTitle")
        body_label = QLabel(body)
        body_label.setProperty("role", "sectionBody")
        body_label.setWordWrap(True)

        layout.addWidget(title_label)
        layout.addWidget(body_label)
        return wrapper

    def build_header_card(self):
        layout = QHBoxLayout(self.header_card)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(22)

        left_wrap = QWidget()
        left = QVBoxLayout(left_wrap)
        left.setContentsMargins(18, 18, 18, 18)
        left.setSpacing(6)
        right_wrap = QFrame()
        right_wrap.setObjectName("ProgressCard")
        right_layout = QVBoxLayout(right_wrap)
        right_layout.setContentsMargins(18, 18, 18, 18)
        right_layout.setSpacing(8)

        eyebrow = QLabel("Desktop Planner")
        eyebrow.setProperty("role", "eyebrow")
        self.hero_title = QLabel("")
        self.hero_title.setProperty("role", "heroTitle")
        self.hero_subtitle = QLabel("")
        self.hero_subtitle.setProperty("role", "heroBody")
        self.hero_subtitle.setWordWrap(True)

        left.addWidget(eyebrow)
        left.addWidget(self.hero_title)
        left.addWidget(self.hero_subtitle)
        left.addStretch(1)

        progress_header = QHBoxLayout()
        progress_label = QLabel("Today's progress")
        progress_label.setStyleSheet("font-size: 12px; font-weight: 600; color: #E7F4EA;")
        self.progress_percent = QLabel("0%")
        self.progress_percent.setStyleSheet("font-size: 16px; font-weight: 600; color: #9FDCB3;")
        progress_header.addWidget(progress_label)
        progress_header.addStretch(1)
        progress_header.addWidget(self.progress_percent)

        self.progress_bar = QProgressBar()
        self.progress_bar.setRange(0, 100)
        self.progress_bar.setTextVisible(False)
        self.progress_note = QLabel("Check off tasks as you finish them.")
        self.progress_note.setProperty("role", "sectionBody")
        self.progress_note.setStyleSheet("color: #C7DFCF; font-size: 12px;")
        self.progress_note.setWordWrap(True)

        right_layout.addLayout(progress_header)
        right_layout.addWidget(self.progress_bar)
        right_layout.addWidget(self.progress_note)
        right_layout.addStretch(1)

        layout.addWidget(left_wrap, 3)
        layout.addWidget(right_wrap, 2)
        layout.setStretch(0, 3)
        layout.setStretch(1, 2)

    def build_tasks_card(self):
        layout = QVBoxLayout(self.tasks_card)
        layout.setContentsMargins(18, 18, 18, 18)
        layout.setSpacing(10)

        top = QHBoxLayout()
        heading = self.make_section_header("Today's focus", "Your day, surfaced in a cleaner dashboard.")
        top.addWidget(heading)
        top.addStretch(1)

        self.task_scroll = QScrollArea()
        self.task_scroll.setWidgetResizable(True)
        self.task_scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.task_scroll.setFrameShape(QFrame.NoFrame)

        self.task_container = QWidget()
        self.task_container.setStyleSheet("background: transparent;")
        self.task_list_layout = QVBoxLayout(self.task_container)
        self.task_list_layout.setContentsMargins(0, 0, 0, 0)
        self.task_list_layout.setSpacing(8)
        self.task_scroll.setWidget(self.task_container)

        layout.addLayout(top)
        layout.addWidget(self.task_scroll, 1)

    def build_actions_card(self):
        layout = QVBoxLayout(self.actions_card)
        layout.setContentsMargins(18, 18, 18, 18)
        layout.setSpacing(12)
        title = QLabel("Task actions")
        title.setProperty("role", "sectionTitle")
        layout.addWidget(title)

        self.actions_grid = QGridLayout()
        self.actions_grid.setHorizontalSpacing(8)
        self.actions_grid.setVerticalSpacing(8)
        layout.addLayout(self.actions_grid)

    def build_modules_card(self):
        layout = QVBoxLayout(self.modules_card)
        layout.setContentsMargins(18, 18, 18, 18)
        layout.setSpacing(12)
        self.modules_title = QLabel("")
        self.modules_title.setProperty("role", "sectionTitle")
        layout.addWidget(self.modules_title)

        terminology_row = QHBoxLayout()
        terminology_label = QLabel("Terminology")
        terminology_label.setProperty("role", "sectionBody")
        self.module_label_toggle = QCheckBox("Use categories")
        self.module_label_toggle.setChecked(self.module_label_mode == "categories")
        self.module_label_toggle.stateChanged.connect(self.toggle_module_label_mode)
        terminology_row.addWidget(terminology_label)
        terminology_row.addStretch(1)
        terminology_row.addWidget(self.module_label_toggle)
        layout.addLayout(terminology_row)

        self.module_actions_grid = QGridLayout()
        self.module_actions_grid.setHorizontalSpacing(8)
        self.module_actions_grid.setVerticalSpacing(8)
        layout.addLayout(self.module_actions_grid)

        self.module_preview = QFrame()
        self.module_preview.setObjectName("MutedCard")
        self.module_preview_layout = QVBoxLayout(self.module_preview)
        self.module_preview_layout.setContentsMargins(12, 12, 12, 12)
        self.module_preview_layout.setSpacing(6)
        layout.addWidget(self.module_preview)
        self.update_module_labels()

    def clear_layout(self, layout):
        while layout.count():
            item = layout.takeAt(0)
            widget = item.widget()
            child_layout = item.layout()
            if widget is not None:
                widget.deleteLater()
            elif child_layout is not None:
                self.clear_layout(child_layout)

    def load_module_label_mode(self):
        try:
            with open(MODULE_LABEL_MODE_PATH, "r") as file:
                mode = json.load(file).get("mode")
                if mode in ("modules", "categories"):
                    return mode
        except (FileNotFoundError, json.JSONDecodeError):
            pass
        return "modules"

    def save_module_label_mode(self):
        with open(MODULE_LABEL_MODE_PATH, "w") as file:
            json.dump({"mode": self.module_label_mode}, file, indent=4)

    def module_label_singular(self):
        return "Category" if self.module_label_mode == "categories" else "Module"

    def module_label_plural(self):
        return "Categories" if self.module_label_mode == "categories" else "Modules"

    def update_module_labels(self):
        if hasattr(self, "modules_title"):
            self.modules_title.setText(self.module_label_plural())

    def toggle_module_label_mode(self, checked=None):
        self.module_label_mode = "categories" if self.module_label_toggle.isChecked() else "modules"
        self.save_module_label_mode()
        self.update_module_labels()
        self.populate_modules()

    def refresh_dashboard(self, initial=False):
        now = datetime.now()
        today = now.strftime("%Y-%m-%d")
        self.events = get_upcoming_events(self.creds)
        self.upcoming_deadlines = get_deadlines(self.creds, True)
        self.deadlines = get_deadlines(self.creds, False)

        task_total = 0 if self.is_placeholder_tasks() else len(self.events)
        deadline_total = 0 if self.is_placeholder_deadlines() else len(self.upcoming_deadlines)

        self.hero_title.setText(now.strftime("%A %d %B"))
        self.hero_subtitle.setText(
            f"{task_total} task{'s' if task_total != 1 else ''} and "
            f"{deadline_total} deadline{'s' if deadline_total != 1 else ''} lined up for today."
        )

        self.populate_tasks()
        self.populate_actions()
        self.populate_modules()
        self.handle_deadline_reminder(today)

        if initial:
            self.fade_in_cards()

    def fade_in_cards(self):
        for index, card in enumerate([self.header_card, self.tasks_card, self.actions_card, self.modules_card]):
            effect = card.graphicsEffect()
            if effect:
                effect.setEnabled(True)
            card.setWindowOpacity(0.0)
            animation = QPropertyAnimation(card, b"windowOpacity", self)
            animation.setStartValue(0.0)
            animation.setEndValue(1.0)
            animation.setDuration(350 + (index * 70))
            animation.setEasingCurve(QEasingCurve.OutCubic)
            animation.start()

    def is_placeholder_tasks(self):
        return len(self.events) == 1 and self.events[0][1] == "No tasks today"

    def is_placeholder_deadlines(self):
        return len(self.upcoming_deadlines) == 1 and self.upcoming_deadlines[0][1] == "No deadlines"

    def populate_tasks(self):
        self.clear_layout(self.task_list_layout)
        self.task_checkboxes = []
        states = self.load_checkbox_states()

        if self.is_placeholder_tasks():
            empty = self.create_soft_panel("Nothing scheduled right now", "Use the action panel to add a task or deadline for today.")
            self.task_list_layout.addWidget(empty)
            self.animate_progress(0)
            return

        for event_id, summary, colour_id in self.events:
            row = self.create_task_row(event_id, summary, colour_id, states.get(event_id, False))
            self.task_list_layout.addWidget(row)

        self.task_list_layout.addStretch(1)
        self.update_progress()

    def create_soft_panel(self, title, body):
        panel = QFrame()
        panel.setObjectName("MutedCard")
        layout = QVBoxLayout(panel)
        layout.setContentsMargins(14, 14, 14, 14)
        layout.setSpacing(5)

        title_label = QLabel(title)
        title_label.setStyleSheet("font-size: 16px; font-weight: 600; color: #163127;")
        body_label = QLabel(body)
        body_label.setProperty("role", "sectionBody")
        body_label.setWordWrap(True)

        layout.addWidget(title_label)
        layout.addWidget(body_label)
        return panel

    def create_task_row(self, event_id, summary, colour_id, checked):
        row = QFrame()
        colour = self.MODULE_COLOURS.get(colour_id, "#2F7D5B")
        background = self.MODULE_BACKGROUNDS.get(colour_id, "#ECF4EE")
        row.setStyleSheet(
            f"background: {background}; border: none; border-radius: 18px;"
        )
        layout = QHBoxLayout(row)
        layout.setContentsMargins(14, 12, 14, 12)
        layout.setSpacing(6)

        checkbox = QCheckBox(summary)
        checkbox.setChecked(checked)
        checkbox.stateChanged.connect(self.update_progress)
        checkbox.setStyleSheet(
            f"""
            QCheckBox {{
                spacing: 10px;
                font-size: 13px;
                font-weight: 500;
                color: {colour};
                background: transparent;
                border: none;
            }}
            QCheckBox::indicator {{
                width: 18px;
                height: 18px;
                border-radius: 9px;
                border: 2px solid #bdd1c3;
                background: transparent;
            }}
            QCheckBox::indicator:checked {{
                background: #3b8c64;
                border: 2px solid #3b8c64;
            }}
            """
        )
        self.task_checkboxes.append((event_id, checkbox))

        layout.addWidget(checkbox, 1)
        return row

    def load_checkbox_states(self):
        try:
            with open(working_checkbox_path, "r") as file:
                return json.load(file)
        except FileNotFoundError:
            return {}

    def update_progress(self):
        total = len(self.task_checkboxes)
        checked = sum(1 for _, checkbox in self.task_checkboxes if checkbox.isChecked())
        progress = int((checked / total) * 100) if total else 0
        self.progress_note.setText(
            f"{checked} of {total} task{'s' if total != 1 else ''} completed." if total else "Check off tasks as you finish them."
        )
        self.animate_progress(progress)

    def animate_progress(self, target):
        self.progress_percent.setText(f"{target}%")
        self.progress_animation = QPropertyAnimation(self.progress_bar, b"value", self)
        self.progress_animation.setStartValue(self.progress_bar.value())
        self.progress_animation.setEndValue(target)
        self.progress_animation.setDuration(280)
        self.progress_animation.setEasingCurve(QEasingCurve.OutCubic)
        self.progress_animation.start()

    def populate_actions(self):
        self.clear_layout(self.actions_grid)
        modules_exist = file_exists(working_modules_path)

        add_task_button = self.make_button("Add Task", "primary", self.open_add_task_dialog, modules_exist)
        edit_task_button = self.make_button("Edit Task", "secondary", self.open_edit_task_dialog, modules_exist)
        add_deadline_button = self.make_button("Add Deadline", "primary", self.open_add_deadline_dialog, modules_exist)
        edit_deadline_button = self.make_button("Edit Deadline", "secondary", self.open_edit_deadline_dialog, modules_exist)
        delete_button = self.make_button("Delete Item", "secondary", self.open_delete_dialog, True)

        self.actions_grid.addWidget(add_task_button, 0, 0)
        self.actions_grid.addWidget(edit_task_button, 0, 1)
        self.actions_grid.addWidget(add_deadline_button, 1, 0)
        self.actions_grid.addWidget(edit_deadline_button, 1, 1)
        self.actions_grid.addWidget(delete_button, 2, 0, 1, 2)

    def populate_modules(self):
        self.clear_layout(self.module_actions_grid)
        self.clear_layout(self.module_preview_layout)

        modules_exist = file_exists(working_modules_path)
        label_plural = self.module_label_plural()
        add_modules_button = self.make_button(f"Add {label_plural}", "primary", self.open_modules_dialog, not modules_exist)
        edit_modules_button = self.make_button(f"Edit {label_plural}", "secondary", self.open_edit_modules_dialog, modules_exist)
        clear_modules_button = self.make_button(f"Clear {label_plural}", "secondary", self.clear_modules, modules_exist)

        self.module_actions_grid.addWidget(add_modules_button, 0, 0)
        self.module_actions_grid.addWidget(edit_modules_button, 0, 1)
        self.module_actions_grid.addWidget(clear_modules_button, 1, 0, 1, 2)

        if not modules_exist:
            self.module_preview_layout.addWidget(
                QLabel(f"Add your {label_plural.lower()} to unlock colour coding across the planner.")
            )
            return

        with open(working_modules_path, "r") as file:
            modules_data = json.load(file)

        for key, module in modules_data.items():
            row = QWidget()
            layout = QHBoxLayout(row)
            layout.setContentsMargins(0, 0, 0, 0)
            layout.setSpacing(10)

            dot = QLabel()
            dot.setFixedSize(14, 14)
            dot.setStyleSheet(f"background: {self.MODULE_COLOURS.get(key, '#3C8D65')}; border-radius: 7px;")
            label = QLabel(module)
            label.setStyleSheet("font-size: 12px; font-weight: 700; color: #163127;")

            layout.addWidget(dot)
            layout.addWidget(label)
            layout.addStretch(1)
            self.module_preview_layout.addWidget(row)

        self.module_preview_layout.addStretch(1)

    def handle_deadline_reminder(self, today):
        with open(working_reminder_path, "r") as file:
            reminder = json.load(file)
            reminded = reminder["reminded"]
            reminder_date = reminder["date"]

        for deadline in self.upcoming_deadlines:
            if deadline[1] != "No deadlines" and reminded == "False":
                QMessageBox.information(self, "Reminder", f"You have an upcoming deadline for {deadline[1]} today")
                reminded = "True"
                reminder_date = today
                break

        if reminded == "True":
            try:
                reminder_dt = datetime.strptime(reminder_date, "%Y-%m-%d").date()
                today_dt = datetime.strptime(today, "%Y-%m-%d").date()
                if reminder_dt < today_dt:
                    reminded = "False"
            except ValueError:
                reminded = "False"
                reminder_date = today

        save_reminder_state(reminded, reminder_date)

    def save_states(self):
        with open(working_checkbox_path, "w") as file:
            json.dump({event_id: checkbox.isChecked() for event_id, checkbox in self.task_checkboxes}, file)

    def closeEvent(self, event):
        self.save_states()
        super().closeEvent(event)

    def time_values(self):
        times = []
        for minute in range(0, 1440):
            moment = datetime.strptime(f"{minute // 60:02d}:{minute % 60:02d}", "%H:%M")
            times.append(moment.strftime("%I:%M %p"))
        return times

    def validate_common(self, title, module):
        if not title.strip():
            QMessageBox.warning(self, "Error", "Title must be filled")
            return False
        if not module.strip():
            QMessageBox.warning(self, "Error", f"{self.module_label_singular()} must be selected")
            return False
        return True

    def open_add_task_dialog(self):
        dialog = TaskDialog(self, "Add Task")
        if dialog.exec_() == QDialog.Accepted:
            title, module, date_text, start_text, end_text = dialog.values()
            if not self.validate_common(title, module):
                return
            if datetime.strptime(start_text, "%I:%M %p") > datetime.strptime(end_text, "%I:%M %p"):
                QMessageBox.warning(self, "Error", "Start time must be earlier than end time")
                return
            add_task(self.creds, title, module, start_text, end_text, date_text)
            self.save_states()
            self.refresh_dashboard()

    def open_edit_task_dialog(self):
        if self.is_placeholder_tasks():
            QMessageBox.information(self, "Edit Task", "No tasks to edit.")
            return

        chooser = ItemChooserDialog(self, "Edit Task", [summary for _, summary, _ in self.events], "Choose a task")
        if chooser.exec_() != QDialog.Accepted:
            return

        summary = chooser.selected_text()
        task_id = next(event_id for event_id, text, _ in self.events if text == summary)
        details = retrieve_event_details(self.creds, task_id)
        dialog = TaskDialog(self, "Edit Task", details)
        if dialog.exec_() == QDialog.Accepted:
            title, module, date_text, start_text, end_text = dialog.values()
            if not self.validate_common(title, module):
                return
            if datetime.strptime(start_text, "%I:%M %p") > datetime.strptime(end_text, "%I:%M %p"):
                QMessageBox.warning(self, "Error", "Start time must be earlier than end time")
                return
            edit_task(self.creds, task_id, title, module, start_text, end_text, date_text)
            self.save_states()
            self.refresh_dashboard()

    def open_add_deadline_dialog(self):
        dialog = DeadlineDialog(self, "Add Deadline")
        if dialog.exec_() == QDialog.Accepted:
            title, module, due_date, due_time = dialog.values()
            if not self.validate_common(title, module):
                return
            add_deadline(self.creds, title, module, due_date, due_time)
            self.save_states()
            self.refresh_dashboard()

    def open_edit_deadline_dialog(self):
        if len(self.deadlines) == 1 and self.deadlines[0][1] == "No deadlines":
            QMessageBox.information(self, "Edit Deadline", "No deadlines to edit.")
            return

        chooser = ItemChooserDialog(self, "Edit Deadline", [summary for _, summary, _ in self.deadlines], "Choose a deadline")
        if chooser.exec_() != QDialog.Accepted:
            return

        summary = chooser.selected_text()
        deadline_id = next(item_id for item_id, text, _ in self.deadlines if text == summary)
        details = retrieve_deadline_details(self.creds, deadline_id)
        dialog = DeadlineDialog(self, "Edit Deadline", details)
        if dialog.exec_() == QDialog.Accepted:
            title, module, due_date, due_time = dialog.values()
            if not self.validate_common(title, module):
                return
            edit_deadline(self.creds, deadline_id, title, module, due_date, due_time)
            self.save_states()
            self.refresh_dashboard()

    def open_delete_dialog(self):
        dialog = DeleteDialog(self)
        if dialog.exec_() != QDialog.Accepted:
            return

        chosen_date = dialog.selected_date()
        items = get_event_by_date(self.creds, chosen_date)
        if len(items) == 1 and items[0][1] == "No tasks/deadlines to delete":
            QMessageBox.information(self, "Delete Item", "No tasks or deadlines to delete for that date.")
            return

        chooser = ItemChooserDialog(self, "Delete Item", [summary for _, summary in items], "Choose an item to delete")
        if chooser.exec_() != QDialog.Accepted:
            return

        summary = chooser.selected_text()
        task_id = next(item_id for item_id, text in items if text == summary)
        delete_task(self.creds, task_id)
        self.save_states()
        self.refresh_dashboard()

    def open_modules_dialog(self):
        dialog = ModulesDialog(self, self.module_label_singular(), self.module_label_plural())
        if dialog.exec_() == QDialog.Accepted:
            modules = dialog.values()
            if not all(text.strip() for text in modules):
                QMessageBox.warning(self, "Error", f"All {self.module_label_singular().lower()} fields must be filled")
                return
            add_modules(modules)
            self.refresh_dashboard()

    def open_edit_modules_dialog(self):
        if not file_exists(working_modules_path):
            QMessageBox.information(self, f"Edit {self.module_label_plural()}", f"No {self.module_label_plural().lower()} added yet.")
            return

        with open(working_modules_path, "r") as file:
            modules_data = json.load(file)

        dialog = ModulesDialog(self, self.module_label_singular(), self.module_label_plural(), modules_data)
        if dialog.exec_() == QDialog.Accepted:
            modules = dialog.values()
            if not all(text.strip() for text in modules):
                QMessageBox.warning(self, "Error", f"All {self.module_label_singular().lower()} fields must be filled")
                return
            add_modules(modules)
            self.refresh_dashboard()

    def clear_modules(self):
        if file_exists(working_modules_path):
            os.remove(working_modules_path)
            self.refresh_dashboard()
        else:
            QMessageBox.warning(self, "Error", f"There are no {self.module_label_plural().lower()} to delete")

    def open_key_dialog(self):
        if not file_exists(working_modules_path):
            QMessageBox.information(self, f"{self.module_label_singular()} Key", f"No {self.module_label_plural().lower()} added yet.")
            return
        with open(working_modules_path, "r") as file:
            modules_data = json.load(file)
        dialog = KeyDialog(self, modules_data, self.MODULE_COLOURS, self.module_label_singular())
        dialog.exec_()


class BaseDialog(QDialog):
    def __init__(self, parent, title):
        super().__init__(parent)
        self.setWindowTitle(title)
        self.setModal(True)
        self.resize(430, 320)
        self.setStyleSheet(APP_STYLE)
        self.layout = QVBoxLayout(self)
        self.layout.setContentsMargins(24, 24, 24, 24)
        self.layout.setSpacing(16)

        title_label = QLabel(title)
        title_label.setProperty("role", "sectionTitle")
        self.layout.addWidget(title_label)


class TaskDialog(BaseDialog):
    def __init__(self, parent, title, details=None):
        super().__init__(parent, title)
        self.resize(460, 420)
        module_label = parent.module_label_singular()

        self.title_input = QLineEdit()
        self.module_input = QComboBox()
        self.module_input.setEditable(False)
        self.date_input = QDateEdit()
        self.date_input.setCalendarPopup(True)
        self.time_start = QTimeEdit()
        self.time_end = QTimeEdit()

        self.populate_modules()
        self.time_start.setDisplayFormat("hh:mm AP")
        self.time_end.setDisplayFormat("hh:mm AP")
        self.date_input.setDisplayFormat("dd MMM yyyy")
        self.time_start.setTime(QTime.currentTime())
        self.time_end.setTime(QTime.currentTime().addSecs(3600))
        self.date_input.setDate(QDate.currentDate())

        form = QGridLayout()
        form.setHorizontalSpacing(12)
        form.setVerticalSpacing(12)
        form.addWidget(QLabel("Title"), 0, 0)
        form.addWidget(self.title_input, 0, 1)
        form.addWidget(QLabel(module_label), 1, 0)
        form.addWidget(self.module_input, 1, 1)
        form.addWidget(QLabel("Date"), 2, 0)
        form.addWidget(self.date_input, 2, 1)
        form.addWidget(QLabel("Start"), 3, 0)
        form.addWidget(self.time_start, 3, 1)
        form.addWidget(QLabel("End"), 4, 0)
        form.addWidget(self.time_end, 4, 1)
        self.layout.addLayout(form)

        if details:
            self.title_input.setText(details["summary"])
            self.select_module(details["colorId"])
            start_dt = datetime.fromisoformat(details["start"])
            end_dt = datetime.fromisoformat(details["end"])
            self.date_input.setDate(QDate(start_dt.year, start_dt.month, start_dt.day))
            self.time_start.setTime(QTime(start_dt.hour, start_dt.minute))
            self.time_end.setTime(QTime(end_dt.hour, end_dt.minute))

        buttons = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        buttons.accepted.connect(self.accept)
        buttons.rejected.connect(self.reject)
        self.layout.addWidget(buttons)

    def populate_modules(self):
        self.module_input.clear()
        if file_exists(working_modules_path):
            with open(working_modules_path, "r") as file:
                modules = json.load(file)
            self.module_input.addItems(list(modules.values()))

    def select_module(self, colour_id):
        if file_exists(working_modules_path):
            with open(working_modules_path, "r") as file:
                modules = json.load(file)
            module = modules.get(str(colour_id), modules.get("8", "General"))
            index = self.module_input.findText(module)
            if index >= 0:
                self.module_input.setCurrentIndex(index)

    def values(self):
        return (
            self.title_input.text(),
            self.module_input.currentText(),
            self.date_input.date().toString("yyyy-MM-dd"),
            self.time_start.time().toString("hh:mm AP"),
            self.time_end.time().toString("hh:mm AP"),
        )


class DeadlineDialog(BaseDialog):
    def __init__(self, parent, title, details=None):
        super().__init__(parent, title)
        self.resize(460, 360)
        module_label = parent.module_label_singular()

        self.title_input = QLineEdit()
        self.module_input = QComboBox()
        self.module_input.setEditable(False)
        self.date_input = QDateEdit()
        self.time_input = QTimeEdit()

        self.populate_modules()
        self.date_input.setCalendarPopup(True)
        self.date_input.setDisplayFormat("dd MMM yyyy")
        self.time_input.setDisplayFormat("hh:mm AP")
        self.date_input.setDate(QDate.currentDate())
        self.time_input.setTime(QTime.currentTime())

        form = QGridLayout()
        form.setHorizontalSpacing(12)
        form.setVerticalSpacing(12)
        form.addWidget(QLabel("Title"), 0, 0)
        form.addWidget(self.title_input, 0, 1)
        form.addWidget(QLabel(module_label), 1, 0)
        form.addWidget(self.module_input, 1, 1)
        form.addWidget(QLabel("Date Due"), 2, 0)
        form.addWidget(self.date_input, 2, 1)
        form.addWidget(QLabel("Time Due"), 3, 0)
        form.addWidget(self.time_input, 3, 1)
        self.layout.addLayout(form)

        if details:
            self.title_input.setText(details["summary"])
            self.select_module(details["colorId"])
            due_dt = datetime.fromisoformat(details["start"])
            self.date_input.setDate(QDate(due_dt.year, due_dt.month, due_dt.day))
            self.time_input.setTime(QTime(due_dt.hour, due_dt.minute))

        buttons = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        buttons.accepted.connect(self.accept)
        buttons.rejected.connect(self.reject)
        self.layout.addWidget(buttons)

    def populate_modules(self):
        self.module_input.clear()
        if file_exists(working_modules_path):
            with open(working_modules_path, "r") as file:
                modules = json.load(file)
            self.module_input.addItems(list(modules.values()))

    def select_module(self, colour_id):
        if file_exists(working_modules_path):
            with open(working_modules_path, "r") as file:
                modules = json.load(file)
            module = modules.get(str(colour_id), modules.get("8", "General"))
            index = self.module_input.findText(module)
            if index >= 0:
                self.module_input.setCurrentIndex(index)

    def values(self):
        return (
            self.title_input.text(),
            self.module_input.currentText(),
            self.date_input.date().toString("yyyy-MM-dd"),
            self.time_input.time().toString("hh:mm AP"),
        )


class ModulesDialog(BaseDialog):
    MODULE_COLOUR_IDS = ["10", "9", "6", "11", "5", "4", "3", "2", "1", "7"]

    def __init__(self, parent, label_singular, label_plural, modules=None):
        super().__init__(parent, f"{'Edit' if modules else 'Add'} {label_plural}")
        self.resize(460, 560)
        self.label_singular = label_singular
        self.inputs = []
        self.existing_values = []
        if modules:
            self.existing_values = [
                modules[colour_id]
                for colour_id in self.MODULE_COLOUR_IDS
                if colour_id in modules
            ]

        count_row = QHBoxLayout()
        count_label = QLabel(f"Number of {label_plural.lower()}")
        self.count_input = QSpinBox()
        self.count_input.setRange(1, len(self.MODULE_COLOUR_IDS))
        self.count_input.setValue(max(1, len(self.existing_values) or 3))
        self.count_input.valueChanged.connect(self.rebuild_inputs)
        count_row.addWidget(count_label)
        count_row.addStretch(1)
        count_row.addWidget(self.count_input)
        self.layout.addLayout(count_row)

        helper_label = QLabel('"General" is included as a default category.')
        helper_label.setProperty("role", "sectionBody")
        helper_label.setWordWrap(True)
        self.layout.addWidget(helper_label)

        self.form = QGridLayout()
        self.form.setHorizontalSpacing(12)
        self.form.setVerticalSpacing(12)
        self.layout.addLayout(self.form)
        self.rebuild_inputs(self.count_input.value())

        buttons = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        buttons.accepted.connect(self.accept)
        buttons.rejected.connect(self.reject)
        self.layout.addWidget(buttons)

    def rebuild_inputs(self, count):
        current_values = [widget.text() for widget in self.inputs]
        while self.form.count():
            item = self.form.takeAt(0)
            widget = item.widget()
            if widget is not None:
                widget.deleteLater()

        self.inputs = []
        for index in range(count):
            widget = QLineEdit()
            if index < len(current_values):
                widget.setText(current_values[index])
            elif index < len(self.existing_values):
                widget.setText(self.existing_values[index])

            self.inputs.append(widget)
            self.form.addWidget(QLabel(f"{self.label_singular} {index + 1}"), index, 0)
            self.form.addWidget(widget, index, 1)

    def values(self):
        return [widget.text() for widget in self.inputs]


class DeleteDialog(BaseDialog):
    def __init__(self, parent):
        super().__init__(parent, "Choose a Date")
        self.resize(380, 220)
        self.date_input = QDateEdit()
        self.date_input.setCalendarPopup(True)
        self.date_input.setDisplayFormat("dd MMM yyyy")
        self.date_input.setDate(QDate.currentDate())
        self.layout.addWidget(self.date_input)

        buttons = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        buttons.accepted.connect(self.accept)
        buttons.rejected.connect(self.reject)
        self.layout.addWidget(buttons)

    def selected_date(self):
        return self.date_input.date().toPyDate()


class ItemChooserDialog(BaseDialog):
    def __init__(self, parent, title, items, helper):
        super().__init__(parent, title)
        self.resize(420, 340)
        helper_label = QLabel(helper)
        helper_label.setProperty("role", "sectionBody")
        self.layout.addWidget(helper_label)

        self.list_widget = QListWidget()
        self.list_widget.addItems(items)
        if items:
            self.list_widget.setCurrentRow(0)
        self.layout.addWidget(self.list_widget)

        buttons = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        buttons.accepted.connect(self.accept)
        buttons.rejected.connect(self.reject)
        self.layout.addWidget(buttons)

    def selected_text(self):
        item = self.list_widget.currentItem()
        return item.text() if item else ""


class KeyDialog(BaseDialog):
    def __init__(self, parent, modules, colours, label_singular):
        super().__init__(parent, f"{label_singular} Key")
        self.resize(380, 320)
        for key, module in modules.items():
            row = QWidget()
            layout = QHBoxLayout(row)
            layout.setContentsMargins(0, 0, 0, 0)
            layout.setSpacing(10)
            dot = QLabel()
            dot.setFixedSize(14, 14)
            dot.setStyleSheet(f"background: {colours.get(key, '#3C8D65')}; border-radius: 7px;")
            label = QLabel(module)
            label.setStyleSheet("font-size: 13px; font-weight: 700;")
            layout.addWidget(dot)
            layout.addWidget(label)
            layout.addStretch(1)
            self.layout.addWidget(row)

        buttons = QDialogButtonBox(QDialogButtonBox.Close)
        buttons.rejected.connect(self.reject)
        buttons.accepted.connect(self.accept)
        self.layout.addWidget(buttons)


if __name__ == "__main__":
    app = QApplication([])
    app.setFont(QFont("Avenir Next", 11))
    window = PlannerWindow()
    window.show()
    app.exec_()
