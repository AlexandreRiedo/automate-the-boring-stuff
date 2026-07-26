import re


def get_hashtags(sentence: str) -> list[str]:
    return re.findall(r"#\w+", sentence)


usr_in = input("Enter a sentence:\n")
for hashtag in get_hashtags(usr_in):
    print(hashtag)
