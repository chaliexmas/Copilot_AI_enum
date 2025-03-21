Power Platform OpenID and Agent Enumerator

This Python script is designed to:

Query Microsoft Online's OpenID configuration for a given domain.

Extract the Tenant ID from OpenID response URLs.

Generate an Environment ID from the extracted Tenant ID.

Bruteforce schema variations and agent names against Power Platform's botsbyschema API endpoint.

Features

Automatically extract OpenID configuration data.

Derive and format the Environment ID.

Supports both single agent name input or a wordlist of agent names.

Brute force schema names from cr000 to crfff.

Handles API response statuses:

200 OK with bot discovery.

401 Unauthorized indicating authentication required.

404 Not Found for non-existent agents.

Outputs positive findings directly to the terminal.

Logs all exceptions and prints the full URL that caused each error.

Requirements

Python 3.x

requests library

Install dependencies:

pip install requests

Usage

python script.py

You will be prompted to enter the domain (e.g., contoso.com).

The script will automatically query the OpenID config and extract necessary information.

Then you will be prompted to input either a single agent name or the path to a .txt wordlist file.

The script will then start enumerating all cr000 to crfff schemas with each provided agent name.

Example Output

[+] Tenant id: 72f988bf-86f1-41af-91ab-2d7cd011db47
[+] Environment id: 72f988bf86f141af91ab2d7cd011db.47
[+] Enumerating schemas and agent names, please wait...
.
.
[+] Success! Agent agent1 found at schema cr650
[+] Url: https://72f988bf86f141af91ab2d7cd011db.47.environment.api.powerplatform.com/powervirtualagents/botsbyschema/cr650_agent1/canvassettings?api-version=2022-03-01-preview

Notes

The script will handle network/DNS resolution errors gracefully and continue the enumeration.

Ensure your network can reach Microsoft's Power Platform API endpoints.

Intended for educational and authorized use only.

Disclaimer

This tool is provided as-is for research and educational purposes. Ensure you have permission to perform enumerations against the target domain or environment.

