from pathlib import Path
import dns.resolver
import dns.rdtypes
import httpx
import subprocess


INPUT_HOSTS_FILE: list[Path] = [Path("allows.txt"), Path("blocks.txt")]
RESOLVER = dns.resolver.Resolver(configure=False)
RESOLVER.nameservers = ["1.1.1.1"]


def get_domains_from_file(file: Path) -> list[str]:
    with open(file, "r") as f:
        lines = f.readlines()
    domains = []
    for line in lines:
        if not (line.startswith("#") or line == "\n"):
            line = (
                line.replace("@@", "")
                .replace("||", "")
                .replace("^", "")
                .replace("\n", "")
            )
            domains.append(line)
    return domains


def get_a_record(domain: str) -> list[str]:
    answers: list[dns.resolver.Answer] = RESOLVER.resolve(qname=domain, rdtype="A")
    return [answer.__str__() for answer in answers]


def ping_ip_address(ip_address: str) -> bool:
    result = subprocess.run(["ping", "-c", "1", ip_address], capture_output=True)
    return result.returncode == 0


def get_http_status_code(domain: str) -> int:
    try:
        response = httpx.get(
            domain if domain.startswith("http") else f"http://{domain}"
        )
        return response.status_code
    except httpx.ConnectError:
        return 0
    except httpx.ReadTimeout:
        return 0
    except httpx.RemoteProtocolError:
        return 0
    except httpx.ConnectTimeout:
        return 0


def get_https_status_code(domain: str) -> int:
    try:
        response = httpx.get(
            domain if domain.startswith("http") else f"https://{domain}"
        )
        return response.status_code
    except httpx.ConnectError:
        return 0
    except httpx.ReadTimeout:
        return 0
    except httpx.RemoteProtocolError:
        return 0
    except httpx.ConnectTimeout:
        return 0


def parse_http_status_code(status_code: int) -> bool:
    if status_code == 0:
        return False
    if status_code >= 200 and status_code < 599:
        return True
    return False


def check_domain(domain: str) -> tuple[bool, bool, bool]:
    resolveable, pingable, _ = False, False, False
    ip_addresses: list[str] = []
    try:
        ip_addresses = get_a_record(domain)
        resolveable = True
    except dns.resolver.NXDOMAIN:
        resolveable = False
    except dns.resolver.NoAnswer:
        resolveable = False
    except dns.resolver.NoNameservers:
        resolveable = False
    except Exception as e:
        print(e)
    for ip_address in ip_addresses:
        if ping_ip_address(ip_address):
            pingable = True
    status_code_http = get_http_status_code(domain)
    status_code_https = get_https_status_code(domain)
    return (
        resolveable,
        pingable,
        parse_http_status_code(status_code_http)
        or parse_http_status_code(status_code_https),
    )


def main():
    for file in INPUT_HOSTS_FILE:
        domains = get_domains_from_file(file)
        for domain in domains:
            resolveable, pingable, reachable = check_domain(domain)
            print(f"{domain}: {resolveable}, {pingable}, {reachable}") if not (
                resolveable and pingable and reachable
            ) else None


if __name__ == "__main__":
    main()
