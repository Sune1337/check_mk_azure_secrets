#!/usr/bin/env python3
# -*- encoding: utf-8; py-indent-offset: 4 -*-

# License: GNU General Public License v2

from cmk.agent_based.v2 import (
    AgentSection,
    CheckPlugin,
    CheckResult,
    DiscoveryResult,
    Metric,
    Result,
    Service,
    State,
    StringTable,
    check_levels
)
import json
from collections.abc import Mapping
from typing import Any, Dict
import datetime
from dateutil import tz

ClientSecretsData = Dict[str, Any]


def parse_azure_secrets_multiple(string_table: StringTable) -> ClientSecretsData:
    parsed = {}
    for line in string_table:
        entry = json.loads(line[0])
        item = entry.get("id")
        parsed.setdefault(item, entry)
    return parsed


agent_section_azure_secrets_client_secrets = AgentSection(
    name="azure_secrets_client_secrets",
    parse_function=parse_azure_secrets_multiple,
    parsed_section_name="azure_secrets_client_secrets",
)


def discovery_azure_secrets_client_secrets(section: ClientSecretsData) -> DiscoveryResult:
    for key in section.keys():
        item = section[key].get("id")
        if not item is None:
            yield Service(item=item)


def check_azure_secrets_client_secrets(item: str, params: Mapping[str, Any], section: ClientSecretsData) -> CheckResult:
    data = None
    for key in section.keys():
        if item == section[key].get("id"):
            data = section.get(key, None)
            break
    if data is None:
        return

    to_zone = tz.tzlocal()
    start_date_time = datetime.datetime.fromisoformat(data["startDateTime"]).astimezone(to_zone).date()
    end_date_time = datetime.datetime.fromisoformat(data["endDateTime"]).astimezone(to_zone).date()
    expires_in = end_date_time - datetime.date.today()

    yield Result(state=State(0), summary=f"{data["name"]}", details=f"Created: {start_date_time}, Expires {end_date_time}")
    yield Metric(name="expires_in", value=expires_in.days, levels=params["status_levels"])
    yield from check_levels(
        expires_in.days,
        label="Expires in",
        levels_lower = ("fixed", params["status_levels"]),
    )


check_plugin_azure_secrets_client_secrets = CheckPlugin(
    name="azure_secrets_client_secrets",
    service_name="Client secret %s",
    sections=["azure_secrets_client_secrets"],
    discovery_function=discovery_azure_secrets_client_secrets,
    check_function=check_azure_secrets_client_secrets,
    check_default_parameters={"status_levels": (14, 7)},
    check_ruleset_name="azure_secrets_client_secrets",
)
