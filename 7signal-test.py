import requests
import csv

eye_url = 'https://api-v2.7signal.com/eyes'
org_url = 'https://api-v2.7signal.com/organizations'
organizationId = '8c5e9699-ba76-4926-aeb3-fxxxxxxxyyzz'
file_name = 'globalcorp_eyes.csv'

auth_data = {
    "client_id": "Se8JBZhBs43663bb4v3xuxknFxujjY3b",
    "client_secret": "H5qMCW-DZzlHWulLdXdl90mxZ53cHxao06zoynrgJEg7K1NuHW1LGEutNgBHf3fe",
    "grant_type": "client_credentials"
}

auth_headers = {
    "Accept": "application/json",
    "Content-Type": "application/x-www-form-urlencoded"
}

# Make the POST request to get token
token_exch_response = requests.post('https://api-v2.7signal.com/oauth2/token', data=auth_data, headers=auth_headers)

if token_exch_response.status_code == 200:
    token_exch_json_response = token_exch_response.json()
    token = token_exch_json_response.get("access_token")

    if token:
        # Headers for the eyes and org endpoints
        headers_eyes = {
            "Accept": "application/json",
            "Authorization": f"Bearer {token}"
        }

        # Make GET requests for both eye and org data
        eye_response = requests.get(f"{eye_url}?organizationId={organizationId}", headers=headers_eyes)
        org_response = requests.get(org_url, headers=headers_eyes)

        if eye_response.status_code == 200 and org_response.status_code == 200:
            eye_data = eye_response.json()
            org_data = org_response.json()


            # Flatten the eye data
            flattened_eye_data = {
                "agents_organizationName": eye_data.get("agents", {}).get("organizationName", "N/A"),
                "agents_deviceCount": eye_data.get("agents", {}).get("deviceCount", 0),
                "agents_licenseSummary_packageName": eye_data.get("agents", {}).get("licenseSummary", {}).get("packageName", "N/A"),
                "agents_licenseSummary_totalLicenses": eye_data.get("agents", {}).get("licenseSummary", {}).get("totalLicenses", 0),
                "agents_licenseSummary_usedLicenses": eye_data.get("agents", {}).get("licenseSummary", {}).get("usedLicenses", 0),
                "agents_licenseSummary_freeLicenses": eye_data.get("agents", {}).get("licenseSummary", {}).get("freeLicenses", 0),
                "sensors_deviceCount": eye_data.get("sensors", {}).get("deviceCount", 0),
                "sensors_deviceStatusSummary_offline": eye_data.get("sensors", {}).get("deviceStatusSummary", {}).get("offline", 0),
                "sensors_deviceStatusSummary_stopped": eye_data.get("sensors", {}).get("deviceStatusSummary", {}).get("stopped", 0),
                "sensors_deviceStatusSummary_idle": eye_data.get("sensors", {}).get("deviceStatusSummary", {}).get("idle", 0),
                "sensors_deviceStatusSummary_purchased": eye_data.get("sensors", {}).get("deviceStatusSummary", {}).get("purchased", 0),
                "sensors_deviceStatusSummary_active": eye_data.get("sensors", {}).get("deviceStatusSummary", {}).get("active", 0),
                "sensors_deviceStatusSummary_maintenance": eye_data.get("sensors", {}).get("deviceStatusSummary", {}).get("maintenance", 0),
                "sensors_modelSummary_eye6300": eye_data.get("sensors", {}).get("modelSummary", {}).get("eye 6300", 0),
                "sensors_modelSummary_eye6200": eye_data.get("sensors", {}).get("modelSummary", {}).get("eye 6200", 0),
                "sensors_modelSummary_eye2200": eye_data.get("sensors", {}).get("modelSummary", {}).get("eye 2200", 0),
                "sensors_modelSummary_eye250": eye_data.get("sensors", {}).get("modelSummary", {}).get("eye 250", 0),
            }

            # Flatten the org data and merge with eye data
            combined_data = []
            for result in org_data.get("results", []):
                merged_data = flattened_eye_data.copy()
                merged_data.update({
                    "pagination_perPage": org_data.get("pagination", {}).get("perPage", "N/A"),
                    "pagination_page": org_data.get("pagination", {}).get("page", "N/A"),
                    "pagination_total": org_data.get("pagination", {}).get("total", "N/A"),
                    "pagination_pages": org_data.get("pagination", {}).get("pages", "N/A"),
                    "result_connection_id": result.get("connection", {}).get("id", "N/A"),
                    "result_id": result.get("id", "N/A"),
                    "result_name": result.get("name", "N/A"),
                    "result_mobileEyeOrgCode": result.get("mobileEyeOrgCode", "N/A")
                })
                combined_data.append(merged_data)

            
            # Generate fieldnames dynamically
            fieldnames = set(flattened_eye_data.keys()).union(*[fd.keys() for fd in combined_data])

            # Write combined data to a CSV file
            csv_file_name = file_name
            with open(csv_file_name, mode='w', newline='') as file:
                writer = csv.DictWriter(file, fieldnames=sorted(fieldnames))
                writer.writeheader()
                writer.writerows(combined_data)

            print(f"Flattened data has been written to {csv_file_name}")
        else:
            print("Error fetching data from eyes or organizations endpoints.")
else:
    print("Error fetching authentication token.")


