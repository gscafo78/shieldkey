import config
import string
import secrets
from utils.password_utils import (
    calculate_entropy,
    check_password_pwned,
    generate_passphrase,
    get_random_separator,
    filter_homoglyphs,
    fetch_custom_wordlist
)

# Helper function to parse boolean values from the request form
def get_bool(request_form, field_name, default):
    return request_form.get(field_name, str(default)).lower() == 'true'

# Main async handler for password/passphrase generation requests
async def handle_generate_password_request(request_form):
    # Read all options from the request, falling back to config defaults
    language = request_form.get('language', config.PP_LANGUAGE)
    languageCustom = request_form.get('languageCustom', config.PP_LANGUAGE_CUSTOM)
    length = int(request_form.get('length', config.PW_LENGTH))
    include_uppercase = get_bool(request_form, 'include_uppercase', config.PW_INCLUDE_UPPERCASE)
    include_digits = get_bool(request_form, 'include_digits', config.PW_INCLUDE_DIGITS)
    include_special = get_bool(request_form, 'include_special', config.PW_INCLUDE_SPECIAL)
    exclude_homoglyphs = get_bool(request_form, 'exclude_homoglyphs', config.PW_EXCLUDE_HOMOGLYPHS)
    generate_type = request_form.get('type', 'password')
    capitalize = get_bool(request_form, 'capitalize', config.PP_CAPITALIZE)
    separator_type = request_form.get('separator_type', config.PP_SEPARATOR_TYPE)
    max_word_length = int(request_form.get('max_word_length', config.PP_MAX_WORD_LENGTH))
    user_defined_separator = request_form.get('user_defined_separator', config.PP_USER_DEFINED_SEPARATOR)
    word_count = int(request_form.get('word_count', config.PP_WORD_COUNT))
    include_numbers = get_bool(request_form, 'include_numbers', config.PP_INCLUDE_NUMBERS)
    include_special_chars = get_bool(request_form, 'include_special_chars', config.PP_INCLUDE_SPECIAL_CHARS)

    # If a custom language is selected, fetch the custom word list
    custom_word_list = None
    if language not in ['en', 'fi', 'fr', 'it']:
        try:
            custom_word_list = await fetch_custom_wordlist(languageCustom)
        except Exception as e:
            # Return error if fetching the custom word list fails
            return {"password": f"Error: Failed to fetch custom word list due to {e}", "entropy": 0}
        language = 'custom'

    # Build the character set for password generation
    characters = string.ascii_lowercase
    if exclude_homoglyphs:
        characters = filter_homoglyphs(characters, True)
    if include_uppercase:
        characters += string.ascii_uppercase if not exclude_homoglyphs else filter_homoglyphs(string.ascii_uppercase, True)
    if include_digits:
        characters += string.digits if not exclude_homoglyphs else filter_homoglyphs(string.digits, True)
    if include_special:
        characters += config.special_characters if not exclude_homoglyphs else filter_homoglyphs(config.special_characters, True)

    # Generate passphrase or password based on the requested type
    if generate_type == 'passphrase':
        attempt = 0
        password = await generate_passphrase(
            word_count, capitalize, separator_type, max_word_length,
            user_defined_separator, include_numbers, include_special_chars,
            language, custom_word_list
        )
        # Check if the generated passphrase has been pwned; retry up to 10 times if so
        while True:
            passphrase_is_pwned = await check_password_pwned(password)
            if not passphrase_is_pwned or attempt >= 10:
                break
            password = await generate_passphrase(
                word_count, capitalize, separator_type, max_word_length,
                user_defined_separator, include_numbers, include_special_chars,
                language, custom_word_list
            )
            attempt += 1
    else:
        attempt = 0
        # Generate a random password using the selected character set
        password = ''.join(secrets.choice(characters) for _ in range(length))
        # Check if the generated password has been pwned; retry up to 10 times if so
        while True:
            password_is_pwned = await check_password_pwned(password)
            if not password_is_pwned or attempt >= 10:
                break
            password = ''.join(secrets.choice(characters) for _ in range(length))
            attempt += 1

    # Calculate entropy of the final password/passphrase
    entropy = calculate_entropy(password)
    # Return the result as a dictionary
    return {"password": password, "entropy": entropy}
