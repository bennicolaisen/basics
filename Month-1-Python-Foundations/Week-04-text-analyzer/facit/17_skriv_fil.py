# Facit: Övning 4.17 – Skriv en fil

def save_lines(path, lines: list[str]) -> None:
    with open(path, "w", encoding="utf-8") as file:
        for line in lines:
            file.write(line + "\n")
