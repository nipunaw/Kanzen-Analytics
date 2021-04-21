# Kanzen Analytics
Kanzen Analytics is a web scraping and data visualization application for anime search analytics. By using this tool, users can add, edit, remove, and export line plots capturing search data for a particular anime show.

Utilized Libraries:
- Django - Renders web content with Python OOP
- Dash - Dynamic visualizations
- Plotly - Static visualizations

APIs:
- MyAnimeList (JikanPy Wrapper) - Scrape anime names
- Google Trends (PyTrends Wrapper) - Scrape search analytics

Data Storage:
- PostgresSQL (Heroku, or local) - Store anime names
- config.ini (local) - Store minor user configurations
