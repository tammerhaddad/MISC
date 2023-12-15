a = "abcdefgabcdefgabcdefg"

c = ""
notes = {"a": "1016", "b": "1174", "c": "1318", "d": "1346", "e": "1567", "f": "1760", "g": "1975"}
for b in a:
    c = c + "word " + notes[b] + ", "

print(c)