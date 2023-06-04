__all__ = ()

from scarletio import create_ansi_format_code


COLOR_FAIL = create_ansi_format_code(foreground_color = (255, 0, 0))
COLOR_PASS = create_ansi_format_code(foreground_color = (0, 255, 0))
COLOR_SKIP = create_ansi_format_code(foreground_color = (0, 255, 255))
COLOR_UNKNOWN = create_ansi_format_code(foreground_color = (255, 0, 255))
COLOR_RESET = create_ansi_format_code()

COLOR_PATH = create_ansi_format_code(foreground_color = (226, 153, 255))
