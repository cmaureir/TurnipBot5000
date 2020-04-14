# TurnipBot5000

Ad-hoc Telegram bot that provide functionality around the *Animal Crossing: New Horizon Game*.
You need a `config.ini` file with a [Google OAuth 2.0](https://developers.google.com/drive/api/v3/about-auth)
(`credentials.json`) file, and a [Token for your Telegram bot](https://core.telegram.org/bots).

## What does this do?

* Given a shared Google Sheet containing the Turnip prices, it gets the latest prices while using
  the command: `/prices` or the previous one using `/prices prev` (Since people live in different
  hemispheres)

* Two CSV files containing the Critters prices (Fish and Bugs) can be
  located in the `data/` directory. One can interact with them via:
  * `/fish info sea bass`:
    ```
    Name: Sea Bass
    Price: 400
    Location: Sea
    Time: All
    Month: All
    Size: XL
    ```
  * `/fish price eye`:
    ```
    :fish: for 'eye'
    Pop-eyed Goldfish: 1300
    Barreleye: 15000
    ```
  * `/bug info flea`:
    ```
    Name: Flea
    Price: 70
    Months: All except January, February, March, December
    Times: All
    Location: Bouncing on certain villager's heads
    ```
  * `/bug price moth`:
    ```
    :bug: for 'moth'
    Moth: 130
    Atlas Moth: 3000
    Madagascan Sunset Moth: 2500
    ```

## Contributing

Suggestions, ideas, etc, just open an Issue or submit a Pull request.
