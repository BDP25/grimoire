import typer
from pydantic import ValidationError


def blue_text(text: str, bold: bool = True) -> str:
    """
    Returns the text in blue color

    :param text: text to color
    :param bold: whether to make the text bold
    :return: colored text
    """
    return typer.style(text, fg=typer.colors.BLUE, bold=bold)


def red_text(text: str, bold: bool = True) -> str:
    """
    Returns the text in red color

    :param text: text to color
    :param bold: whether to make the text bold
    :return: colored text
    """
    return typer.style(text, fg=typer.colors.RED, bold=bold)


def green_text(text: str, bold: bool = True) -> str:
    """
    Returns the text in green color

    :param text: text to color
    :param bold: whether to make the text bold
    :return: colored text
    """
    return typer.style(text, fg=typer.colors.GREEN, bold=bold)


def validation_error(error: ValidationError) -> str:
    """
    Returns the validation error in red color

    :param error: validation error
    :return: colored error message
    """
    prefix = red_text("Error in configuration file")
    return f"{prefix}: {error}"
