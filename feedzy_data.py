import requests

# Set the plugin slug
plugin_slug = 'feedzy-rss-feeds'

# WordPress API URL with the limit set to retrieve the desired number of days
api_url = f'https://api.wordpress.org/stats/plugin/1.0/downloads.php?slug={plugin_slug}&limit=7'

# Function to get and print the daily download counts
def get_daily_downloads():
    try:
        response = requests.get(api_url)
        data = response.json()

        # Sort the data by date to ensure correct order
        sorted_dates = sorted(data.keys())

        if len(sorted_dates) == 0:
            print("No data available.")
            return None

        # Print the downloads for each retrieved day
        print("Daily downloads:")
        for date in sorted_dates:
            downloads = int(data[date])
            if date == sorted_dates[-1]:  # Highlight the most recent date
                print(f"**{date}: {downloads} downloads (Most Recent)**")
            else:
                print(f"{date}: {downloads} downloads")

        return data

    except Exception as e:
        print(f"An error occurred: {e}")
        return None

# Call the function to get the daily downloads
get_daily_downloads()
