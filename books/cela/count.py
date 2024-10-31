import os
path_txt = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'colmena_characters.txt')
print(path_txt)
with open(path_txt, 'r', encoding='utf-8') as file:
    lines = []
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
        lines.append(line)

print(f"전체 등장인물 : {len(lines)}")
char_index_plot = set()
char_index_name = set()

for line in lines:
    if not line.startswith('('): # 서사x or 이름x
        char_index_plot.add(lines.index(line))
    if line.endswith('*')    : # 이름o
        char_index_name.add(lines.index(line))
print(f"이름이 호명되는 등장인물 : {len(char_index_name)}")
print(f"서사에 등장하면서 이름이 호명되는 등장인물 : {len(char_index_plot)}")
for index in char_index_plot - char_index_name:
    print(index, lines[index])