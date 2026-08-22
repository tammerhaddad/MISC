a = "abcdefgabcdefgabcdefg"

c = ""
# A6-G6, rounded to whole Hz. These were previously assigned in ascending
# order down the alphabet, which put every letter on the wrong pitch.
notes = {"a": "1760", "b": "1975", "c": "1046", "d": "1174", "e": "1318", "f": "1397", "g": "1568"}
for b in a:
    c = c + "word " + notes[b] + ", "

print(c)