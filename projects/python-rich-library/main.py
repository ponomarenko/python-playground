from rich.console import Console
from rich.table import Table

table = Table(title="People")
rows = [
    ["John", "Doe", "45"],
    ["Jane", "Doe", "32"],
    ["Mary", "Smith", "25"],
]
columns = ["First Name", "Last Name", "Age"]

for column in columns:
    table.add_column(column)

for row in rows:
    table.add_row(*row, style='bright_green')

console = Console()
console.print(table)