import requests

# Define the API URL for theme information
api_url = 'https://api.wordpress.org/themes/info/1.1/'

# Set the theme slug
theme_slug = 'neve'

# Prepare the payload with the necessary parameters
payload = {
    'action': 'theme_information',
    'request[slug]': theme_slug
}

# Make the request to the API
response = requests.get(api_url, params=payload)
theme_data = response.json()

# Display the response to see available data
print(theme_data)
