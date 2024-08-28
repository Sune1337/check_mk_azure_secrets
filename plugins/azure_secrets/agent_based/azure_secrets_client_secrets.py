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
from datetime import datetime, timezone
from dateutil import tz
from cmk.agent_based.v2 import render

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

    start_date = datetime.fromisoformat(data["startDateTime"])
    end_date = datetime.fromisoformat(data["endDateTime"])
    expires_in = (end_date - datetime.now(timezone.utc)).total_seconds()
    validity_period = (end_date - start_date).total_seconds()
    validity_period_perc = min(100.0, (validity_period - expires_in) / validity_period * 100)

    to_zone = tz.tzlocal()
    status_levels = (params["status_levels"][0] * 86400, params["status_levels"][1] * 86400)
    yield Result(state=State(0), summary=f"{data["name"]}", details=f"Created: {start_date.astimezone(to_zone).date()}, Expires {end_date.astimezone(to_zone).date()}")
    yield Metric(name="expires_in", value=expires_in, levels=status_levels)
    yield Metric(name="validity_period_perc", value=validity_period_perc, )
    yield from check_levels(
        max(0.0, expires_in),
        label="Expires in",
        levels_lower = ("fixed", status_levels),
        render_func = lambda v: render.timespan(v),
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
