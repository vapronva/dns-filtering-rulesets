from datetime import datetime
from json import loads as json_loads
from pathlib import Path

from pydantic import BaseModel, HttpUrl, NonNegativeInt, TypeAdapter


class AdguardFilter(BaseModel):
    url: HttpUrl
    name: str
    last_updated: datetime
    id: int
    rules_count: NonNegativeInt
    enabled: bool


class AdguardResponseStatus(BaseModel):
    filters: list[AdguardFilter]
    whitelist_filters: list[AdguardFilter]
    user_rules: list[str]
    interval: NonNegativeInt
    enabled: bool


ADGUARD_RESPONSE_STATUS_ADAPTER: TypeAdapter = TypeAdapter(AdguardResponseStatus)

INPUT_FILE_PATH: Path = Path("adguard-control-filtering-status.json")
OUTPUT_FILE_PATH: Path = Path("filters-table.md")


def generate_table_from_filters(list_of_filters: list[AdguardFilter]) -> str:
    table = "| Name | Enabled | Rules Count | URL |\n"
    table += "| --- | --- | --- | --- |\n"
    for filter in list_of_filters:
        table += f"| {filter.name} | {"✅" if filter.enabled else "❌"} | {filter.rules_count} | [{filter.url.__str__().replace("https://", "")}]({filter.url}) |\n"
    return table


def main() -> None:
    with open(INPUT_FILE_PATH) as f:
        data: str = f.read()
    dgrd_response: AdguardResponseStatus = (
        ADGUARD_RESPONSE_STATUS_ADAPTER.validate_python(json_loads(data.strip()))
    )
    with open(OUTPUT_FILE_PATH, "w") as f:
        f.write("### Blocklists\n")
        f.write(generate_table_from_filters(dgrd_response.filters))
        f.write("\n### Allowlists\n")
        f.write(generate_table_from_filters(dgrd_response.whitelist_filters))


if __name__ == "__main__":
    main()
