#!/usr/bin/env python3title=Title
# -*- encoding: utf-8; py-indent-offset: 4 -*-
"""rule for assigning the special agent to host objects"""

# License: GNU General Public License v2

from cmk.rulesets.v1 import Title, Help
from cmk.rulesets.v1.form_specs import (
    DictElement,
    Dictionary,
    Password,
    String,
)
from cmk.rulesets.v1.rule_specs import Topic, SpecialAgent


def _valuespec_special_agents_azure_secrets() -> Dictionary:
    return Dictionary(
        title=Title("Azure secrets agent"),
        elements={
            "authority": DictElement(
                parameter_form=String(
                    title=Title("Authority"),
                    help_text=Help(
                        "Used for authenticating to Graph API."
                    ),
                ),
                required=True,
            ),
            "clientId": DictElement(
                parameter_form=String(
                    title=Title("Client ID"),
                    help_text=Help(
                        "Used for authenticating to Graph API."
                    ),
                ),
                required=True,
            ),
            "clientSecret": DictElement(
                parameter_form=Password(
                    title=Title("Client secret"),
                    help_text=Help(
                        "Used for authenticating to Graph API."
                    ),
                ),
                required=True,
            ),
        },
    )


rule_spec_azure_secrets_datasource_programs = SpecialAgent(
    name="azure_secrets",
    title=Title("Azure secrets agent"),
    topic=Topic.CLOUD,
    parameter_form=_valuespec_special_agents_azure_secrets,
    help_text=Help(
        "This rule selects the Azure secrets agent instead of the normal Check_MK Agent "
        "which collects the data through the Azure Graph API"
    ),
)
