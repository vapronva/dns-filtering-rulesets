from pathlib import Path

import dns.rdtypes
import dns.resolver
from domain_checker import get_domains_from_file


INPUT_HOSTS_FILE: list[Path] = [Path("allows.txt"), Path("blocks.txt")]
RESOLVER = dns.resolver.Resolver(configure=False)
RESOLVER.nameservers = [""]


def get_a_record(domain: str) -> list[str]:
    answers: dns.resolver.Answer = RESOLVER.resolve(qname=domain, rdtype="A")
    return [answer.__str__() for answer in answers.rrset] if answers.rrset else []


def main():
    for file in INPUT_HOSTS_FILE:
        domains = get_domains_from_file(file)
        for domain in domains:
            try:
                addr: list[str] = get_a_record(domain)
                if "0.0.0.0" in addr:
                    print(domain)
            except Exception as e:
                print(e)


if __name__ == "__main__":
    main()
