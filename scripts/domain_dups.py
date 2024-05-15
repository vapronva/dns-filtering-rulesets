from pathlib import Path

from domain_checker import get_domains_from_file


INPUT_HOSTS_FILE: list[Path] = [Path("allows.txt"), Path("blocks.txt")]


def find_duplicate_domains(domains: list[str]) -> list[str]:
    return list(set([domain for domain in domains if domains.count(domain) > 1]))


def main() -> None:
    for file in INPUT_HOSTS_FILE:
        domains = get_domains_from_file(file)
        duplicate_domains = find_duplicate_domains(domains)
        for domain in duplicate_domains:
            print(domain)


if __name__ == "__main__":
    main()
