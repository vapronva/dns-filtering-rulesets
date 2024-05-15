import csv
from pathlib import Path

from domain_checker import get_domains_from_file


INPUT_FILE_PATH: Path = Path("tier0.csv")

LISTS_PATH: list[Path] = [Path("allows.txt"), Path("blocks.txt")]


def get_domains_from_csv(file: Path) -> list[str]:
    with open(file) as f:
        reader = csv.reader(f)
        rows = list(reader)
    domains = []
    for row in rows:
        for domain in row:
            domains.append(domain)
    return domains


def get_matching_domains() -> list[str]:
    csv_domains = get_domains_from_csv(INPUT_FILE_PATH)
    allowed_domains = get_domains_from_file(LISTS_PATH[0])
    blocked_domains = get_domains_from_file(LISTS_PATH[1])
    matching_domains = []
    for domain in csv_domains:
        if domain in allowed_domains or domain in blocked_domains:
            matching_domains.append(domain)
    return matching_domains


if __name__ == "__main__":
    matching_domains = get_matching_domains()
    for domain in matching_domains:
        print(domain)
