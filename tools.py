from datetime import datetime


def get_current_time() -> str:
    return datetime.now().isoformat()


def add_numbers(a: float, b: float) -> float:
    return a + b


TOOLS = {
    "get_current_time": get_current_time,
    "add_numbers": add_numbers,
}