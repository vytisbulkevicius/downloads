import requests
import os
from datetime import datetime

# Define the API URL for theme information
api_url = 'https://api.wordpress.org/themes/info/1.1/'

# Set the theme slug
theme_slug = 'neve'

# Prepare the payload with the necessary parameters
payload = {
    'action': 'theme_information',
    'request[slug]': theme_slug
}

# Function to get the total downloads
def get_total_downloads():
    # Make the request to the API
    response = requests.get(api_url, params=payload)
    theme_data = response.json()
    # Extract total downloads
    return theme_data.get('downloaded')

# File to store the download data
data_file = 'downloads_data.txt'

# Get today's total downloads
total_downloads = get_total_downloads()

# Initialize yesterday's downloads to 0 if the file doesn't exist yet
yesterday_downloads = 0

# If the file exists, read the last recorded downloads
if os.path.exists(data_file):
    with open(data_file, 'r') as file:
        lines = file.readlines()
        if lines:
            last_line = lines[-1].strip()
            _, _, yesterday_downloads = last_line.split(',')
            yesterday_downloads = int(yesterday_downloads)

# Calculate today's downloads
today_downloads = total_downloads - yesterday_downloads

# Get today's date
today_date = datetime.now().strftime('%Y-%m-%d')

# Print the results
print(f"Total downloads for theme '{theme_slug}': {total_downloads}")
print(f"Today's date: {today_date}")
print(f"Today's downloads: {today_downloads}")

# Append the new data to the file
with open(data_file, 'a') as file:
    file.write(f"{total_downloads},{today_date},{today_downloads}\n")

# Configure Git user identity
os.system('git config --global user.email "b.vytis@gmail.com"')
os.system('git config --global user.name "vytisbulkevicius"')

# Save the updated file to the repository by committing and pushing it
os.system('git add downloads_data.txt')
os.system(f'git commit -m "Update downloads data for {today_date}"')
os.system('git push origin main')
