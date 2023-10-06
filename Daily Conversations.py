import requests
import base64
import csv
from datetime import datetime

def get_agent_conversations_count(website_id, agent_id):
    page_number = 1  # Starting page number
    date_counts = {}  # Dictionary to store counts per date
    
    # Prepare the Basic Auth header
    auth_string = 'e824586c-92e2-4557-8724-765ca4b11eb6:09a75072340f7a15f6b2c82fe96002b0063be7a4691237ad4844e9e4917af94d'
    auth_encoded = base64.b64encode(auth_string.encode()).decode()
    auth_header = f'Basic {auth_encoded}'
    
    while True:
        # Construct the URL and headers for the request
        url = f"https://app.crisp.chat/api/v1/website/{website_id}/conversations/{page_number}"
        headers = {
            "Authorization": auth_header,
            "Content-Type": "application/json",
            "X-Crisp-Tier": "plugin"
        }
        
        # Define the query parameters for the request
        params = {
            "filter_assigned": agent_id
        }
        
        # Send the request to the Crisp API
        response = requests.get(url, headers=headers, params=params)
        
        # Check for a successful response
        if response.status_code == 200 or response.status_code == 206:
            # Parse the JSON response
            jsonData = response.json()
            
            # Process each conversation in the response
            for conversation in jsonData['data']:
                # Extract and format the creation timestamp as a date (assuming milliseconds since epoch)
                created_date = datetime.utcfromtimestamp(conversation['created_at'] / 1000).strftime('%Y-%m-%d')
                # Increment the count for this date
                date_counts[created_date] = date_counts.get(created_date, 0) + 1
            
            # If there are conversations in the current page, increment the page_number to fetch the next page
            if len(jsonData['data']) > 0:
                page_number += 1
            else:
                # Stop the loop when there are no more conversations
                break
        else:
            print(f'Failed to retrieve conversations: {response.status_code}')
            break  # Exit the loop if the request failed
    
    # Write the results to a CSV file
    with open('conversations_count.csv', 'w', newline='') as file:
        #prefix the above with the agent name, such as 'gino_conversations_count.csv'
        writer = csv.writer(file)
        writer.writerow(['Date', 'Count'])  # Write header row
        for date, count in sorted(date_counts.items()):
            writer.writerow([date, count])  # Write data rows

get_agent_conversations_count('854228c2-0dc4-4b4a-875e-4ead05d1a46b', 'PASTE AGENT ID HERE')
#Paste the agent ID above leaving the ' ' either side
