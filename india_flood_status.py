"""
India flood status from the Google Flood Forecasting API.

Pulls every river gauge in India (or another country) with its latest
Flood Hub severity and trend, then writes:
  - flood_status.csv  (one row per gauge, opens in Excel or Google Sheets)
  - flood_map.html    (a map you can open in any browser)

Requirements: Python 3.8+, no extra packages. Runs in Google Colab too.

Get access first (free, non-commercial use):
  1. Join the waitlist: https://developers.google.com/flood-forecasting
  2. When approved, enable the Flood Forecasting API in a Google Cloud
     project and create an API key.

Usage:
  python india_flood_status.py --key YOUR_API_KEY
  python india_flood_status.py --key YOUR_API_KEY --region BD
  python india_flood_status.py --sample        # test the pipeline offline

Data: Google Flood Forecasting API, licensed CC BY 4.0. Flood Hub is a
support tool. Official warnings in India come from IMD, CWC and the SDMA.
"""
import argparse, csv, json, os, sys, urllib.request, urllib.error
from collections import Counter

BASE = "https://floodforecasting.googleapis.com/v1"
SEV_ORDER = ["EXTREME", "SEVERE", "ABOVE_NORMAL", "NO_FLOODING", "UNKNOWN"]
SEV_COLOR = {"EXTREME": "#6a1b9a", "SEVERE": "#c62828", "ABOVE_NORMAL": "#e0a826",
             "NO_FLOODING": "#0b7a3e", "UNKNOWN": "#888888"}


def post(path, body, key):
    req = urllib.request.Request(
        f"{BASE}/{path}?key={key}",
        data=json.dumps(body).encode(),
        headers={"Content-Type": "application/json"},
        method="POST",
    )
    try:
        with urllib.request.urlopen(req, timeout=60) as r:
            return json.load(r)
    except urllib.error.HTTPError as e:
        sys.exit(f"API error {e.code}: {e.read().decode()[:500]}\n"
                 "Check that your key is valid and your project has API access.")


def fetch_all(path, body, key, list_field):
    out, token = [], None
    while True:
        b = dict(body)
        if token:
            b["pageToken"] = token
        page = post(path, b, key)
        out.extend(page.get(list_field, []))
        token = page.get("nextPageToken")
        if not token:
            return out


def sample_data():
    """Synthetic records to test the pipeline. Not real forecasts."""
    pts = [("SAMPLE-1", "Sample gauge A", "Sample river 1", 26.2, 91.7, "SEVERE", "RISE"),
           ("SAMPLE-2", "Sample gauge B", "Sample river 2", 25.6, 85.1, "ABOVE_NORMAL", "RISE"),
           ("SAMPLE-3", "Sample gauge C", "Sample river 3", 31.1, 75.3, "NO_FLOODING", "FALL"),
           ("SAMPLE-4", "Sample gauge D", "Sample river 4", 20.3, 85.8, "EXTREME", "NO_CHANGE"),
           ("SAMPLE-5", "Sample gauge E", "Sample river 5", 16.5, 80.6, "NO_FLOODING", "NO_CHANGE")]
    gauges = [{"gaugeId": g, "siteName": s, "river": r, "source": "SAMPLE",
               "location": {"latitude": la, "longitude": lo}, "qualityVerified": True}
              for g, s, r, la, lo, _, _ in pts]
    statuses = [{"gaugeId": g, "severity": sv, "forecastTrend": tr, "issuedTime": "SAMPLE",
                 "qualityVerified": True} for g, _, _, _, _, sv, tr in pts]
    return gauges, statuses


def write_csv(rows, path):
    cols = ["gaugeId", "siteName", "river", "latitude", "longitude", "severity",
            "forecastTrend", "issuedTime", "source", "qualityVerified"]
    with open(path, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=cols, extrasaction="ignore")
        w.writeheader()
        w.writerows(rows)


def write_map(rows, path, region, sample):
    pts = [r for r in rows if r["latitude"] is not None]
    banner = ("<div style='background:#c62828;color:#fff;padding:8px 12px;font:600 14px sans-serif'>"
              "SAMPLE DATA FOR TESTING. NOT A REAL FORECAST.</div>") if sample else ""
    legend = "".join(f"<span style='margin-right:12px'><b style='color:{SEV_COLOR[s]}'>&#9679;</b> "
                     f"{s.replace('_', ' ').title()}</span>" for s in SEV_ORDER)
    html = f"""<!doctype html><html><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Flood status {region}</title>
<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/leaflet/1.9.4/leaflet.min.css">
<script src="https://cdnjs.cloudflare.com/ajax/libs/leaflet/1.9.4/leaflet.min.js"></script>
<style>html,body{{margin:0;height:100%}}#map{{height:calc(100% - 70px)}}
.bar{{padding:8px 12px;font:14px system-ui,sans-serif}}</style></head><body>
{banner}<div class="bar"><b>Flood status, {region}</b> ({len(pts)} gauges). {legend}
<br><small>Data: Google Flood Forecasting API, CC BY 4.0. Confirm with IMD, CWC or your SDMA.</small></div>
<div id="map"></div>
<script>
var pts = {json.dumps(pts)};
var col = {json.dumps(SEV_COLOR)};
var map = L.map('map').setView([22.5, 80], 5);
L.tileLayer('https://{{s}}.tile.openstreetmap.org/{{z}}/{{x}}/{{y}}.png',
  {{maxZoom: 18, attribution: '&copy; OpenStreetMap contributors'}}).addTo(map);
pts.forEach(function(p) {{
  L.circleMarker([p.latitude, p.longitude], {{radius: 6, color: col[p.severity] || '#888',
    fillOpacity: 0.85, weight: 1}})
   .bindPopup('<b>' + (p.siteName || p.gaugeId) + '</b><br>' + (p.river || '') +
     '<br>Severity: ' + p.severity + '<br>Trend: ' + (p.forecastTrend || '') +
     '<br>Issued: ' + (p.issuedTime || '') + '<br>Source: ' + (p.source || ''))
   .addTo(map);
}});
</script></body></html>"""
    with open(path, "w", encoding="utf-8") as f:
        f.write(html)


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--key", default=os.environ.get("FLOODHUB_API_KEY"), help="API key (or set FLOODHUB_API_KEY)")
    ap.add_argument("--region", default="IN", help="CLDR region code, default IN (India)")
    ap.add_argument("--all-gauges", action="store_true", help="include gauges that are not quality verified")
    ap.add_argument("--sample", action="store_true", help="use synthetic sample data, no API call")
    ap.add_argument("--out", default=".", help="output folder")
    a = ap.parse_args()

    if a.sample:
        gauges, statuses = sample_data()
    else:
        if not a.key:
            sys.exit("Add --key YOUR_API_KEY, or run with --sample to test.")
        body = {"regionCode": a.region, "pageSize": 1000, "includeNonQualityVerified": a.all_gauges}
        print(f"Fetching gauges for {a.region} ...")
        gauges = fetch_all("gauges:searchGaugesByArea", body, a.key, "gauges")
        print(f"Fetching latest flood status for {a.region} ...")
        statuses = fetch_all("floodStatus:searchLatestFloodStatusByArea", body, a.key, "floodStatuses")

    meta = {g["gaugeId"]: g for g in gauges}
    rows = []
    for s in statuses:
        g = meta.get(s.get("gaugeId"), {})
        loc = s.get("gaugeLocation") or g.get("location") or {}
        rows.append({
            "gaugeId": s.get("gaugeId"), "siteName": g.get("siteName", ""), "river": g.get("river", ""),
            "latitude": loc.get("latitude"), "longitude": loc.get("longitude"),
            "severity": s.get("severity", "UNKNOWN"), "forecastTrend": s.get("forecastTrend", ""),
            "issuedTime": s.get("issuedTime", ""), "source": s.get("source") or g.get("source", ""),
            "qualityVerified": s.get("qualityVerified", g.get("qualityVerified", "")),
        })
    rank = {s: i for i, s in enumerate(SEV_ORDER)}
    rows.sort(key=lambda r: rank.get(r["severity"], 99))

    os.makedirs(a.out, exist_ok=True)
    csv_path, map_path = os.path.join(a.out, "flood_status.csv"), os.path.join(a.out, "flood_map.html")
    write_csv(rows, csv_path)
    write_map(rows, map_path, a.region, a.sample)

    counts = Counter(r["severity"] for r in rows)
    print(f"\n{len(rows)} gauges with a flood status ({'SAMPLE DATA' if a.sample else a.region}):")
    for s in SEV_ORDER:
        print(f"  {s.replace('_', ' ').title():<14} {counts.get(s, 0)}")
    for r in rows[:10]:
        if r["severity"] in ("EXTREME", "SEVERE"):
            print(f"  ! {r['severity']:<8} {r['siteName'] or r['gaugeId']} {r['river']}")
    print(f"\nWrote {csv_path} and {map_path}")


if __name__ == "__main__":
    main()
