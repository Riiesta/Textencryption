from flask import Flask, render_template, request

app = Flask(__name__)

def caesar_cipher(text, shift):
    result = ""
    for char in text:
        if char.isalpha():
            shifted = ord(char) + shift
            if char.islower():
                if shifted > ord('z'):
                    shifted -= 26
                elif shifted < ord('a'):
                    shifted += 26
            elif char.isupper():
                if shifted > ord('Z'):
                    shifted -= 26
                elif shifted < ord('A'):
                    shifted += 26
            result += chr(shifted)
        else:
            result += char
    return result


def vigenere_cipher(text, keyword):
    ENG_ALPHABET = 'abcdefghijklmnopqrstuvwxyz'
    RUS_ALPHABET = 'абвгдеёжзийклмнопрстуфхцчшщъыьэюя'

    def shift_char(char, key_char, alphabet):
        char_idx = alphabet.index(char)
        key_idx = alphabet.index(key_char)
        return alphabet[(char_idx + key_idx) % len(alphabet)]

    keyword_repeated = ''
    keyword_index = 0

    for char in text:
        if char.isalpha():
            keyword_repeated += keyword[keyword_index % len(keyword)]
            keyword_index += 1
        else:
            keyword_repeated += char

    encrypted_text = ''
    for original, key in zip(text, keyword_repeated):
        if original.isalpha():
            if original.islower():
                if original in ENG_ALPHABET:
                    alphabet = ENG_ALPHABET
                else:
                    alphabet = RUS_ALPHABET.lower()
            else:
                if original.lower() in ENG_ALPHABET:
                    alphabet = ENG_ALPHABET.upper()
                else:
                    alphabet = RUS_ALPHABET.upper()

            key = key.lower() if key.lower() in alphabet else key.upper()
            encrypted_text += shift_char(original, key, alphabet)
        else:
            encrypted_text += original

    return encrypted_text

@app.route("/", methods=["GET", "POST"])
def index():
    encrypted_text = ""
    if request.method == "POST":
        text = request.form["text"]
        method = request.form["encryption_method"]
        if method == "caesar":
            shift = int(request.form["shift"])
            encrypted_text = caesar_cipher(text, shift)
        elif method == "vigenere":
            keyword = request.form["keyword"]
            encrypted_text = vigenere_cipher(text, keyword)
    return render_template("index.html", encrypted_text=encrypted_text)

if __name__ == "__main__":
    app.run(debug=True)
