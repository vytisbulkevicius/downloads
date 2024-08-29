import requests
import os
from datetime import datetime

# Define the API URL for theme information
api_url = 'https://api.wordpress.org/themes/info/1.1/'

# List of theme slugs
themes = ['neve', 'hestia', 'neve-fse', 'raft', 'jaxon', 'fork', 'riverbank']

# Function to get the total downloads
def get_total_downloads(theme_slug):
    payload = {
        'action': 'theme_information',
        'request[slug]': theme_slug
    }
    response = requests.get(api_url, params=payload)
    theme_data = response.json()
    return theme_data.get('downloaded')

# Process each theme
for theme_slug in themes:
    # File to store the download data for each theme
    data_file = f'{theme_slug}_downloads_data.txt'
    
    # Header for the data file
    header = "Total Downloads,Date,Today's Downloads\n"
    
    # Check if the file exists and whether it has headers
    file_exists = os.path.exists(data_file)
    add_header = not file_exists or (file_exists and not open(data_file).readline().startswith("Total Downloads"))

    # Get today's total downloads
    total_downloads = get_total_downloads(theme_slug)

    # Initialize yesterday's downloads to the current total if the file doesn't exist yet
    yesterday_total_downloads = total_downloads

    # If the file exists, read the last recorded total downloads
    if file_exists:
        with open(data_file, 'r') as file:
            lines = file.readlines()
            if lines:
                last_line = lines[-1].strip()
                yesterday_total_downloads, _, _ = last_line.split(',')
                yesterday_total_downloads = int(yesterday_total_downloads)

    # Calculate today's downloads as the difference between today and yesterday's total
    today_downloads = total_downloads - yesterday_total_downloads

    # Get today's date
    today_date = datetime.now().strftime('%Y-%m-%d')

    # Print the results
    print(f"Total downloads for theme '{theme_slug}': {total_downloads}")
    print(f"Today's date: {today_date}")
    print(f"Today's downloads: {today_downloads}")

    # Append the header if needed and the new data to the file
    with open(data_file, 'a') as file:
        if add_header:
            file.write(header)
        file.write(f"{total_downloads},{today_date},{today_downloads}\n")

# Configure Git user identity
os.system('git config --global user.email "b.vytis@gmail.com"')
os.system('git config --global user.name "vytisbulkevicius"')

# Save the updated file to the repository by committing and pushing it
os.system('git add downloads_data.txt')
os.system(f'git commit -m "Update downloads data for {today_date}"')
os.system('git push origin main')
