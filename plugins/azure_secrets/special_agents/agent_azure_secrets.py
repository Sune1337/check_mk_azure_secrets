#!/usr/bin/env python3
# -*- encoding: utf-8; py-indent-offset: 4 -*-
"""Special Agent to fetch client secrets data from Azure Graph API"""

# License: GNU General Public License v2

import sys
from collections.abc import Sequence

from pathlib import Path
from cmk.special_agents.v0_unstable.agent_common import (
    SectionWriter,
    special_agent_main,
)
from cmk.special_agents.v0_unstable.argument_parsing import (
    Args,
    create_default_argument_parser,
)
from cmk.utils import password_store

import msal
import requests


def parse_arguments(argv: Sequence[str] | None) -> Args:
    parser = create_default_argument_parser(description=__doc__)

    # required
    parser.add_argument("--authority", default=None, help="Used for authenticating to Graph API.", required=True)
    parser.add_argument("--clientId", default=None, help="Used for authenticating to Graph API.", required=True)
    parser.add_argument("--clientSecret", default=None, help="Used for authenticating to Graph API.", required=True)

    return parser.parse_args(argv)


def agent_azure_secrets_main(args: Args) -> int:
    """main function for the special agent"""

    # Get secret for authenticating.
    pw_id, pw_path = args.clientSecret.split(":")
    password = password_store.lookup(Path(pw_path), pw_id)

    # Get auth token.
    app = msal.ConfidentialClientApplication(args.clientId, authority=args.authority, client_credential=password)

    scope = ["https://graph.microsoft.com/.default"]
    result = app.acquire_token_silent(scope, account=None)

    if not result:
        # No suitable token exists in cache. Let's get a new one from AAD.
        result = app.acquire_token_for_client(scopes=scope)

    if not "access_token" in result:
        # Authentication failed.
        print(result, file=sys.stderr)
        return -1

    url = 'https://graph.microsoft.com/v1.0/applications?$select=appId,displayName,passwordCredentials'
    headers = {
        'Authorization': f"Bearer {result['access_token']}"
    }

    with SectionWriter(f"azure_secrets_client_secrets") as w:

        while True:
            # Make a GET request to the provided url, passing the access token in a header
            graph_result = requests.get(url=url, headers=headers)
            if not graph_result.ok:
                print(f"Error when calling Graph API. Status code: {graph_result.status_code} Reason: {graph_result.reason}", file=sys.stderr)
                return -1

            # Print the results in a JSON format
            query_result = graph_result.json()
            if "value" in query_result:
                for item in query_result["value"]:
                    if "passwordCredentials" in item:
                        for passwordCredential in item["passwordCredentials"]:
                            w.append_json({
                                "id": passwordCredential["keyId"],
                                "name": f"{item["displayName"]} / {passwordCredential["displayName"]}",
                                "startDateTime": passwordCredential["startDateTime"],
                                "endDateTime": passwordCredential["endDateTime"]
                            })

            if not "@odata.nextLink" in query_result:
                break

            url = query_result["@odata.nextLink"]

    return 0


def main() -> int:
    """Main entry point to be used"""
    return special_agent_main(parse_arguments, agent_azure_secrets_main)


if __name__ == "__main__":
    sys.exit(main())
