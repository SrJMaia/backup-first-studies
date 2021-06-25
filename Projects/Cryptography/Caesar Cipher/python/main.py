import string as st
from unidecode import unidecode
import re

def shift_alphabet(shift):
    alphabet = st.ascii_lowercase
    alphabet_shifted = ""
    for i, _ in enumerate(alphabet):
        try:
            alphabet_shifted += alphabet[i+shift]
        except IndexError:
            for j in range(shift):
                alphabet_shifted += alphabet[j]
            break
    return alphabet, alphabet_shifted


class InvalidCharacter(Exception):
    def __init__(self):
             default_message = f"The string contains a special character besides {st.ascii_lowercase + '.,àèìòùáéíóúýâêîôûãñõäëïöüÿ '}."
             super().__init__(default_message)


class InvalidKey(Exception):
    def __init__(self):
             default_message = f"Invalid type for key. Must be an int type greatter than 0."
             super().__init__(default_message)


class InvalidRemove(Exception):
    def __init__(self):
             default_message = f"Invalid type for remove. Must be a bool type."
             super().__init__(default_message)


def checking_key(key):
    try:
        key = int(key)
    except ValueError:
        raise InvalidKey
    else:
        return key


def checking_remove(remove):
    if type(remove) == int:
        raise InvalidRemove
    elif remove == True or remove == False:
        return remove
    else:
        raise InvalidRemove


def checking_special_characters(message):
    special = st.ascii_lowercase + ".,àèìòùáéíóúýâêîôûãñõäëïöüÿ "
    matched_list = [characters in special for characters in message]
    return all(matched_list)


def cleaning_message(message, remove=True):
    if remove:
        message = re.sub(r'\s+', ' ', re.sub('[^A-Za-z\s]+', '', re.sub(r'\s+', ' ', message)).strip().lower())
    elif not remove:
        if not checking_special_characters(message):
            raise InvalidCharacter
        message = re.sub(r'\s+', ' ', unidecode(message)).strip().lower()
    return message


def encode(message, key, remove_characters=True):
    """
    Returns decoded message.

    Parameters:
        message (str): The message to be decoded
        key (int): The value to shift the alphabet
        remove_characters (bool): Whether to remove special characters or not

    Returns:
        coded_message (str): The message which gets coded
    """
    key = checking_key(key)
    remove_characters = checking_remove(remove_characters)
    message = cleaning_message(message, remove=remove_characters)
    coded_message = ""
    alphabet, alphabet_shifted = shift_alphabet(key)
    for _, v in enumerate(message):
        if v in st.punctuation + st.whitespace:
            coded_message += v
            continue
        coded_message += alphabet_shifted[alphabet.find(v)]
    return coded_message


def decode(message, key, remove_characters=True):
    """
    Returns decoded message.

    Parameters:
        message (str): The message to be decoded
        key (int): The value to shift the alphabet
        remove_characters (bool): Whether to remove special characters or not

    Returns:
        decoded_message (str): The message which gets decoded
    """
    key = checking_key(key)
    remove_characters = checking_remove(remove_characters)
    message = cleaning_message(message)
    decoded_message = ""
    alphabet, alphabet_shifted = shift_alphabet(key)
    for _, v in enumerate(message):
        if v in st.punctuation + st.whitespace:
            decoded_message += v
            continue
        decoded_message += alphabet[alphabet_shifted.find(v)]
    return decoded_message
