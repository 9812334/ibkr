from rcp import get_polls, get_poll_data, to_csv

# Search for Biden polls
polls = get_polls(candidate="Biden")

# Get data for a specific poll (replace with desired URL)
data = get_poll_data(polls['url'], csv_output=True)

# Save to CSV
to_csv('biden_polling_data.csv', data)