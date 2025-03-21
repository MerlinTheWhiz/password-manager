import random
import string

def main():
    while True:
        print("What's your desired password length?")
        length = input("Min of 8 characters: ").strip()
        if length.isdigit():
            length = int(length)
            if length >= 8:
                print("Generated Password:", password_generator(length))
                break
            else:
                print("Minimum should be 8 based on security best practices")
        else:
            print("Input is not a number")
        

def password_generator(length):
    uppercase = string.ascii_uppercase
    lowercase = string.ascii_lowercase
    digits = string.digits
    special_chars = string.punctuation

    password = [
        random.choice(uppercase),
        random.choice(lowercase),
        random.choice(digits),
        random.choice(special_chars),
    ]

    all_chars = uppercase + lowercase + digits + special_chars
    password += random.choices(all_chars, k=length - 4)

    random.shuffle(password)

    return "".join(password)

if __name__ =="__main__":
    main()