import requests
import os
from datetime import datetime, timedelta

# List of plugin slugs
plugins = ['feedzy-rss-feeds', 'visualizer', 'wpcf7-redirect', 'woocommerce-product-addon', 'otter-blocks', 'themeisle-companion', 'multiple-pages-generator-by-porthas', 'menu-icons', 'wp-maintenance-mode', 'templates-patterns-collection', 'blocks-export-import', 'blocks-css', 'blocks-animation', 'optimole-wp', 'media-library-organizer', 'wp-cloudflare-page-cache', 'tweet-old-post']  # Add more plugin slugs as needed

# Function to get yesterday's download count for a plugin
def get_yesterday_downloads(plugin_slug):
    api_url = f'https://api.wordpress.org/stats/plugin/1.0/downloads.php?slug={plugin_slug}&limit=2'
    try:
        response = requests.get(api_url)
        data = response.json()

        # Get yesterday's date
        yesterday_date = (datetime.now() - timedelta(1)).strftime('%Y-%m-%d')

        # Check if yesterday's data is available
        if yesterday_date in data:
            downloads_yesterday = int(data[yesterday_date])
            return yesterday_date, downloads_yesterday
        else:
            print(f"No download data available for yesterday ({yesterday_date}) for plugin '{plugin_slug}'.")
            return yesterday_date, 0

    except Exception as e:
        print(f"An error occurred for plugin '{plugin_slug}': {e}")
        return None, None

# Process each plugin
for plugin_slug in plugins:
    # Get yesterday's downloads
    yesterday_date, downloads_yesterday = get_yesterday_downloads(plugin_slug)

    if downloads_yesterday is not None:
        # File to store the download data for the plugin
        data_file = f'{plugin_slug}_downloads_data.txt'

        # Header for the data file
        header = "Date,Downloads\n"

        # Check if the file exists and whether it has headers
        file_exists = os.path.exists(data_file)
        add_header = not file_exists or (file_exists and not open(data_file).readline().startswith("Date"))

        # Print the results
        print(f"Yesterday's downloads for plugin '{plugin_slug}': {downloads_yesterday}")

        # Append the header if needed and the new data to the file
        with open(data_file, 'a') as file:
            if add_header:
                file.write(header)
            file.write(f"{yesterday_date},{downloads_yesterday}\n")

        # Ensure the new file is tracked by Git
        os.system(f'git add {data_file}')


# Configure Git user identity
os.system('git config --global user.email "b.vytis@gmail.com"')
os.system('git config --global user.name "vytisbulkevicius"')

# Commit and push the updated files
os.system(f'git commit -m "Update plugin downloads data for {yesterday_date}"')
os.system('git push origin main')
