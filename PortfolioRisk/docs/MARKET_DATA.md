# Market-data provider contract

Provider timestamps are Unix epoch milliseconds. Prices may be used for risk for
at most `MAX_PRICE_AGE_MS` milliseconds. At exactly the configured age they are
valid; anything older is stale.

Notional is `signed quantity × price × contract multiplier`. Equities normally
have multiplier 1; listed equity options normally have multiplier 100. Currency
conversion is intentionally outside this exercise.
