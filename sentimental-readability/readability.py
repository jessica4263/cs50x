from cs50 import get_string
import string


def main():

    text = get_string("Text: ")
    L = (letter(text) / word(text)) * 100.0
    S = (sentence(text) / word(text)) * 100.0
    index = 0.0588 * L - 0.296 * S - 15.8
    grade = round(index)

    if grade > 1 and grade < 16:
        print(f"Grade {grade}")
    elif grade < 1:
        print("Before Grade 1")
    elif grade > 16:
        print("Grade 16+")


def letter(t):
    count = 0
    for i in t:
        if i.isalpha():
            count += 1
    return count


def word(t):
    count = 0
    for i in t:
        if i.isspace():
            count += 1
    return count + 1


def sentence(t):
    count = 0
    for char in t:
        if char in string.punctuation:
            if ord(char) in [39, 34, 58, 59, 45, 44]:
                continue
            else:
                count += 1
    return count


main()
