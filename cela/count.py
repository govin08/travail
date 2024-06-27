character_count = 0 # 전체 등장인물
main_char_count = 0 # 주요 등장인물 : 소설 서사에 직접 등장 & 이름 호명
with open('colmena_characters.txt', 'r', encoding='utf-8') as file:
    for line in file:
        # 빈 행은 제외
        line = line.strip()
        if not line:
            continue
        # 숫자로 시작하는 행은 장(章) 구분을 위한 것이니 제외
        if line[0].isdigit():
            continue
        # 에필로그 장도 제외
        if line.startswith('에필로그'):
            continue
        # 행 수를 합산하여 총 등장인물수 계산
        character_count += 1
        # 소괄호로 시작하는 행의 등장인물은 주요 등장인물이 아님
        if line.startswith('('):
            continue
        main_char_count += 1
print(character_count)
print(main_char_count)
