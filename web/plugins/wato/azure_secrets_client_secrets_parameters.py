# License: GNU General Public License v2

from cmk.gui.i18n import _

from cmk.gui.valuespec import (
    Dictionary,
    Integer,
    Tuple,
)

from cmk.gui.plugins.wato.utils import (
    CheckParameterRulespecWithItem,
    rulespec_registry,
    RulespecGroupCheckParametersApplications,
)


def _item_valuespec_azure_secrets_client_secrets():
    return Dictionary(
        elements=[
            (
                "status_levels",
                Tuple(
                    title=_("Number of days to expiration."),
                    elements=[
                        Integer(title=_("Warning"), default_value=14),
                        Integer(title=_("Critical"), default_value=7),
                    ],
                )
            ),
        ],
    )


rulespec_registry.register(
    CheckParameterRulespecWithItem(
        check_group_name="azure_secrets_client_secrets",
        group=RulespecGroupCheckParametersApplications,
        match_type="dict",
        item_spec=_item_valuespec_azure_secrets_client_secrets,
        parameter_valuespec=_item_valuespec_azure_secrets_client_secrets,
        title=lambda: _("Azure client secrets expiration"),
    )
)
