#!/usr/bin/env python3
# -*- encoding: utf-8; py-indent-offset: 4 -*-
"""server side component to create the special agent call"""

# License: GNU General Public License v2

from collections.abc import Iterator
from pydantic import BaseModel

from cmk.server_side_calls.v1 import (
    HostConfig,
    Secret,
    SpecialAgentCommand,
    SpecialAgentConfig,
)


class Params(BaseModel):
    authority: str
    clientId: str
    clientSecret: Secret


def _agent_azure_secrets_arguments(
        params: Params, host_config: HostConfig
) -> Iterator[SpecialAgentCommand]:
    command_arguments: list[str | Secret] = []

    if params.authority is not None:
        command_arguments += ["--authority", params.authority]
    if params.clientId is not None:
        command_arguments += ["--clientId", params.clientId]
    if params.clientSecret is not None:
        command_arguments += ["--clientSecret", params.clientSecret]

    yield SpecialAgentCommand(command_arguments=command_arguments)


special_agent_azure_secrets = SpecialAgentConfig(
    name="azure_secrets",
    parameter_parser=Params.model_validate,
    commands_function=_agent_azure_secrets_arguments,
)
