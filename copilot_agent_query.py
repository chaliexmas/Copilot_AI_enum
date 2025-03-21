import requests
import json
import re
import sys
import time

def fetch_openid_configuration():
    domain = input("Enter the DOMAIN: ")
    url = f"https://login.microsoftonline.com/{domain}/.well-known/openid-configuration"
    
    try:
        response = requests.get(url)
        response.raise_for_status()  # Raise an error for bad responses (4xx and 5xx)
        
        # Parse JSON response
        parsed_response = json.loads(response.text)
        
        # Extract tenant ID using regex
        urls = [
            parsed_response.get("userinfo_endpoint", ""),
            parsed_response.get("token_endpoint", ""),
            parsed_response.get("kerberos_endpoint", ""),
            parsed_response.get("issuer", ""),
            parsed_response.get("device_authorization_endpoint", ""),
            parsed_response.get("end_session_endpoint", "")
        ]
        
        tenant_ids = set(re.findall(r"https://(?:login\.microsoftonline\.com|sts\.windows\.net)/([\w-]+)/", " ".join(urls)))
        
        for tenant_id in tenant_ids:
            print(f"[+] Tenant id: {tenant_id}")
            
            # Modify tenant ID to EnvironmentID format
            environment_id = tenant_id.replace("-", "").rsplit(".", 1)[0] + "." + tenant_id[-2:]
            print(f"[+] Environment id: {environment_id}")
            
            base_url = f"https://{environment_id}.environment.api.powerplatform.com/powervirtualagents/botsbyschema/"
            
            # Prompt user for AGENT_NAME input method
            agent_input = input("Enter the AGENT_NAME or provide a path to a wordlist file: ")
            
            agent_names = []
            if agent_input.endswith(".txt"):
                try:
                    with open(agent_input, "r") as file:
                        agent_names = [line.strip() for line in file if line.strip()]
                except FileNotFoundError:
                    print("[!] Wordlist file not found. Continuing.")
            else:
                agent_names.append(agent_input)
            
            print("[+] Enumerating schemas and agent names, please wait...")
            
            for agent_name in agent_names:
                for i in range(0x000, 0xfff + 1):
                    schema_name = f"cr{format(i, '03x')}"
                    url = f"{base_url}{schema_name}_{agent_name}/canvassettings?api-version=2022-03-01-preview"
                    
                    if i % 100 == 0:
                        sys.stdout.write(".")
                        sys.stdout.flush()
                    
                    try:
                        response = requests.get(url)
                        print(f"[+] Url Response: {url} {response.status_code}")
                        
                        data = response.json() if response.status_code in [200, 401, 404] else {}
                        
                        if response.status_code == 200 and "botCanvasSettings" in data and "botId" in data["botCanvasSettings"]:
                            print(f"\n[+] Success! Agent {agent_name} found at schema {schema_name}")
                            print(f"[+] Url: {url}")
                            break
                        elif response.status_code == 401 or data.get("demoWebsiteErrorCode") == "401":
                            print(f"\n[+] Success! Agent {agent_name} found at schema {schema_name} but requires authentication (401)")
                            print(f"[+] Url: {url}")
                            break
                        elif response.status_code == 404 or data.get("demoWebsiteErrorCode") == "404":
                            continue
                    except requests.exceptions.RequestException as e:
                        print(f"[!] Exception occurred while accessing {url}: {e}")
                        continue
            
            print("\n[+] Enumeration complete.")
        
        if not tenant_ids:
            print("\nNo Tenant ID found.")
    except requests.exceptions.RequestException as e:
        print(f"\nError: {e}")

if __name__ == "__main__":
    fetch_openid_configuration()
