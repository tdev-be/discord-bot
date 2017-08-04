1. Make sure to get Python 3.5 or higher

This is required to actually run the bot.

2. Set up venv

python3.6 -m venv venv

3. Install dependencies

python3 -m pip install -U -r requirements.txt

4. Create the database in PostgreSQL



5. Create config file

```python
client_id   = '' # your bot's client ID
token = '' # your bot's token
bots_key = '' # your key on bots.discord.pw
postgresql = 'postgresql://user:password@host/database' # your postgresql info from above

prefix= '+'
sql_debug=False
```