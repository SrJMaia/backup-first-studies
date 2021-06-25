from main import decode, encode

message = "The Zen of Python, by Tim Peters |"

encode_message = encode(message, 10, remove_characters=True)

decoded_message = decode(encode_message, 3)
