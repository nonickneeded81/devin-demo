# Bundesliga Odds Aggregator

Aggregates and averages betting odds for upcoming Bundesliga weekend matches from multiple European bookmakers.

Features:
- Fetches live odds from The Odds API (EU bookmakers: Pinnacle, Unibet, 1xBet, etc.)
- Averages Home / Draw / Away odds across all available bookmakers
- Displays team logos alongside match pairings
- Clean white UI with responsive design

## How to Run

1. Get a free API key from [The Odds API](https://the-odds-api.com/#get-access) (Starter tier, 500 requests/month).

2. Install dependencies:

```bash
pip install -r requirements.txt
```

3. Set your API key and start the app:

```bash
export ODDS_API_KEY=your_key_here
python app.py
```

4. Open http://127.0.0.1:5000 in your browser.
