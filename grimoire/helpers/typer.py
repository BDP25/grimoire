import typer


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
