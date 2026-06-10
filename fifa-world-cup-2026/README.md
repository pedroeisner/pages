# FIFA World Cup 2026 auto-updating Google Calendar feed

This repo generates a public `.ics` calendar feed for FIFA World Cup 2026.

It is designed to be subscribed to from Google Calendar using a stable raw GitHub URL:

```text
https://raw.githubusercontent.com/pedroeisner/pages/main/fifa-world-cup-2026/worldcup2026.ics
```

## What updates automatically

- Kickoff times are stored as UTC instants, so Google Calendar displays them in your local timezone.
- Event titles update as fixture data changes, including knockout opponents once known.
- Locations use the venue/stadium name returned by the fixture API.
- Descriptions include stage; group-stage matches include group name and the teams in that group.
- Events use stable UIDs based on fixture IDs, so Google Calendar updates existing events instead of creating duplicates.

## Setup

### Recommended data source: API-FOOTBALL / API-SPORTS

Create a repository secret named `API_FOOTBALL_KEY` with your API key. The workflow calls:

```text
https://v3.football.api-sports.io/fixtures?league=1&season=2026
https://v3.football.api-sports.io/standings?league=1&season=2026
```

### GitHub Action

The workflow runs every 3 hours, and can also be run manually from the Actions tab.
It commits `worldcup2026.ics` back to the repo only when the generated file changes.

## Google Calendar subscription

Google Calendar > Other calendars > + > From URL > paste:

```text
https://raw.githubusercontent.com/pedroeisner/pages/main/fifa-world-cup-2026/worldcup2026.ics
```

Google Calendar controls refresh timing; updates are not instant.
