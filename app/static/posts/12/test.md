## Markdown with rich

**Hello world**. this is a [Markdown](https://en.wikipedia.org/wiki/Markdown) file. We love python.

```python
from rich.markdown import Markdown
from rich.console import Console

console = Console()
md = Markdown("## Hello world")

console.print(md)
```

*This is italic*
