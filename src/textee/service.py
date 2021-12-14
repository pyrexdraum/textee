from pygments import highlight
from pygments.formatters import HtmlFormatter
from pygments.lexers import get_lexer_by_name


def highlight_code(code: str, syntax: str) -> str:
    """Возвращает `подсвеченный` html-тегами code."""
    lexer = get_lexer_by_name(syntax, encoding="utf-8", stripall=True)
    formatter = HtmlFormatter(linenos="table")
    return highlight(code, lexer, formatter)
