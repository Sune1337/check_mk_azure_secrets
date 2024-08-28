#!/usr/bin/env python3
# -*- encoding: utf-8; py-indent-offset: 4 -*-

# License: GNU General Public License v2

from cmk.gui.i18n import _
from cmk.gui.graphing._utils import check_metrics, metric_info
from cmk.gui.graphing import perfometer_info


check_metrics['check_mk-azure_secrets_client_secrets'] = {
    'validity_period_perc': {'auto_graph': False},
}

metric_info['validity_period_perc'] = {
    'title': _('Used up valid period'), 'unit': '%', "color": "15/a",
}

metric_info['expires_in'] = {
    'title': _('Expires in'), 'unit': 's', "color": "15/a",
}

perfometer_info.append(
    {
        "type": "linear",
        "segments": ["validity_period_perc"],
        "total": 100.0,
    }
)
