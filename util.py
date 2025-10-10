from pathlib import Path


def prompt(msg: str) -> bool:
    print(f"{msg} [(y)es/(n)o]")
    return not input("> ").lower().startswith("n")
