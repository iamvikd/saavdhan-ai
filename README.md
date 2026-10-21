# Flood Hub data starter

`india_flood_status.py` lists every river gauge in India with its latest Google Flood Hub severity (Extreme, Severe, Above normal, No flooding) and trend, then saves a spreadsheet and a map.

## Steps
1. Join the free API waitlist at https://developers.google.com/flood-forecasting (non-commercial use, data under CC BY 4.0).
2. After approval, enable the Flood Forecasting API in a Google Cloud project and create an API key.
3. Run it, on your laptop or in Google Colab:
   ```
   python india_flood_status.py --key YOUR_API_KEY
   ```
4. Open `flood_map.html` in a browser and `flood_status.csv` in Excel or Google Sheets.

No key yet? `python india_flood_status.py --sample` runs the whole pipeline on clearly marked sample data.

Useful options: `--region BD` for another country, `--all-gauges` to include gauges that are not quality verified.

## Project ideas on top of this
- Filter the CSV to gauges within 50 km of your college and send a daily summary to a WhatsApp or Telegram group.
- Translate each Severe or Extreme status into local-language action steps (see the Alert to Action tab).
- Compare today's gauges with past floods using Google's open datasets: Runoff Reanalysis and Reforecast (1980 to 2023), Inundation History (1999 to 2020), Groundsource flash flood events.

Flood Hub is a support tool. Official warnings in India come from IMD, CWC and your State Disaster Management Authority.
