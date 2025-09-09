# ShieldKey - Secure Password Generator (Fork)

## Description

**ShieldKey** is a fork of the [Secure Password Generator](https://pwgen.joonatanh.com) (`main` branch). This simple Docker web application is designed to generate secure passwords or passphrases with customizable options. In addition to all the original features, ShieldKey adds support for an Italian wordlist for passphrase generation.

## What's New in ShieldKey

- **Italian Wordlist**: You can now generate passphrases using Italian words, in addition to the previously supported English, Finnish, and French.

## Features

- **User Interface**: Displays the generated password or passphrase in a user-friendly interface with the option to copy it to the clipboard.
- **Security Check**: Checks all generated passwords and passphrases against the haveibeenpwned database using their API to ensure users are not shown a compromised password.
- **Offline Mode**: Option to disable checking passwords against the haveibeenpwned API, suitable for instances running in isolated networks or where external API access is unnecessary.
- **Environment Variable Configuration**: Allows users to define default settings for password and passphrase generation using environment variables.
- **Local Settings Storage**: Ability to save all generation settings in a browser cookie for persistence between visits. This can be toggled on or off by the user.
- **Multiple Generation**: Generates up to 5 passwords or passphrases simultaneously, configurable via an environment variable (`MULTI_GEN=true`).
- **Language Dropdown Control**: Allows disabling the language dropdown menu through an environment variable (`PP_HIDE_LANG=true`), simplifying the UI based on user preference.
- **Progressive Web Application (PWA)**: Ensures a seamless, app-like experience on various devices.
- **Comprehensive Password Generation Options**: Includes uppercase letters, digits, and special characters, with an option to exclude homoglyphs.
- **Flexible Passphrase Generation**: Offers capitalization of words, choice of separators (space, number, special character, or user-defined character), and inclusion of numbers or special characters.
- **Language Support**: Now supports Italian, in addition to English, Finnish, and French wordlists for passphrase generation.
- **Custom Word Lists**: Supports fetching custom word lists from specified URLs and local files, facilitating personalized passphrase generation.

## How to Use

1. **Install Docker** if you haven't already.
2. **Run ShieldKey**: Build or pull the image and run it using the following commands:

```bash
docker pull 4ss078/shieldkey:latest
docker run -d -p 5000:5000 4ss078/shieldkey:latest
```

To enable **Offline Mode**, append `-e NO_API_CHECK=true` to the `docker run` command:

```bash
docker run -d -p 5000:5000 -e NO_API_CHECK=true 4ss078/shieldkey:latest
```

Example with environment variables:

```bash
docker run -d -p 5000:5000 \
  -e NO_API_CHECK=false \
  -e PW_LENGTH=12 \
  -e PW_INCLUDE_UPPERCASE=false \
  -e PW_INCLUDE_DIGITS=false \
  -e PW_INCLUDE_SPECIAL=false \
  -e PW_EXCLUDE_HOMOGLYPHS=true \
  -e PP_WORD_COUNT=4 \
  -e PP_CAPITALIZE=false \
  -e PP_SEPARATOR_TYPE=dash \
  -e PP_USER_DEFINED_SEPARATOR='' \
  -e PP_MAX_WORD_LENGTH=12 \
  -e PP_INCLUDE_NUMBERS=false \
  -e PP_INCLUDE_SPECIAL_CHARS=false \
  -e PP_LANGUAGE=it \
  -e PP_HIDE_LANG=false \
  -e PP_LANGUAGE_CUSTOM='' \
  -e MULTI_GEN=true \
  -e GENERATE_PP=true \
  -e SHOW_SAVE_SETTINGS=true \
  -e ROBOTS_ALLOW=false \
  -e GOOGLE_SITE_VERIFICATION='' \
  -e DISABLE_URL_CHECK=false \
  -e BASE_PATH='' \
  -e PP_LOCAL_WORDLIST=/app/custom_wordlist.txt \
  -v "A:\german.txt:/app/custom_wordlist.txt" \
  4ss078/shieldkey:latest
```

## Requirements

- Docker
- Any modern web browser

## License

This project is open-source and available under the AGPL-3.0
