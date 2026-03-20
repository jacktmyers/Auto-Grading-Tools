import os
import sys

RAINBOW_COLORS = [
    "\033[31m",  # Red
    "\033[38;5;208m",  # Orange
    "\033[33m",  # Yellow
    "\033[32m",  # Green
    "\033[34m",  # Blue
    "\033[35m",  # Purple
]

_current_color_index = 0
_header_lines = []
_log_lines = []


def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')


def get_terminal_size():
    try:
        size = os.get_terminal_size()
        return size.columns, size.lines
    except:
        return 80, 24


def update_display():
    clear_screen()

    for line in _header_lines:
        print(line)
    
    _, terminal_height = get_terminal_size()
    header_height = len(_header_lines)
    max_log_lines = max(0, terminal_height - header_height - 1)
    
    for line in _log_lines[-max_log_lines:]:
        print(line)


def set_header(student_progress: str, student_name: str, file_progress: str):
    global _header_lines
    terminal_cols,_ = get_terminal_size()
    

    WHITE_BG_BLACK_FG = "\033[40;97m"
    RESET = "\033[0m"

    _header_lines = [
        f"▌Student Progress: {student_progress}",
        f"▌Student: {student_name}",
        f"▌File Progress: {file_progress}",
    ]


    _header_lines = [
        f"{WHITE_BG_BLACK_FG}{line}{' ' * (terminal_cols - len(line)-1)}▐{RESET}"
        for line in _header_lines
    ]

    update_display()


def rainbow_print(text: str) -> None:
    global _current_color_index, _log_lines
    
    color = RAINBOW_COLORS[_current_color_index]
    reset = "\033[0m"
    
    colored_text = f"{color}{text}{reset}"
    _log_lines.append(colored_text)
    
    _current_color_index = (_current_color_index + 1) % len(RAINBOW_COLORS)
    
    update_display()
