character_count = 0
main_char_count = 0
with open('colmena_characters.txt', 'r', encoding='utf-8') as file:
    for line in file:
        line = line.strip()
        if not line:
            continue
        if line[0].isdigit():
            continue
        if line.startswith('에필로그'):
            continue
        character_count += 1
        if line.startswith('('):
            continue
        main_char_count += 1
print(character_count)
print(main_char_count)