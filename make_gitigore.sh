#!/bin/bash
echo "Finding large files (100MB+) and sensitive files (.secret.*)..."
echo "Searching directories (this may take a while)..."

# 임시 파일들 생성
large_files_temp=$(mktemp)
secret_files_temp=$(mktemp)

echo "Searching for .secret.* files..."
# 1. 모든 .secret.* 파일들 찾기 (크기 상관없이)
find . -name ".secret.*" -type f 2>/dev/null | while read -r file; do
    normalized_file="${file#./}"
    echo "Found sensitive file: $normalized_file"
    echo "$normalized_file" >> "$secret_files_temp"
done

echo "Searching for large files (100MB+)..."
# 2. 100MB+ 파일들 찾기 (단, .secret.*는 제외)
find . -type f -size +100M ! -name ".secret.*" 2>/dev/null | while read -r file; do
    if [[ "$file" != ./.git/* ]] && [[ "$file" != ./env_wp/* ]]; then
        normalized_file="${file#./}"
        echo "Found large file: $normalized_file"
        echo "$normalized_file" >> "$large_files_temp"
    fi
done

# 임시 파일에서 결과 읽기
large_files=$(cat "$large_files_temp" 2>/dev/null)
secret_files=$(cat "$secret_files_temp" 2>/dev/null)
rm -f "$large_files_temp"
rm -f "$secret_files_temp"

echo ""
echo "Search completed!"

echo ""
if [ -n "$secret_files" ]; then
    echo "Summary of sensitive files found:"
    echo "$secret_files"
fi

if [ -n "$large_files" ]; then
    echo ""
    echo "Summary of large files found:"
    echo "$large_files"
fi

# 새로운 .gitignore 생성
echo "# Auto-generated gitignore" > .gitignore
echo "env_tra/" >> .gitignore

# 민감한 파일들 추가
if [ -n "$secret_files" ]; then
    echo "" >> .gitignore
    echo "# 민감한 파일들 (.secret.*)" >> .gitignore
    echo "$secret_files" >> .gitignore
fi

# 큰 파일들 추가
if [ -n "$large_files" ]; then
    echo "" >> .gitignore
    echo "# 100MB 이상 큰 파일들" >> .gitignore
    echo "$large_files" >> .gitignore
fi

# 중복 제거 및 정렬
sort .gitignore | uniq > .gitignore.tmp && mv .gitignore.tmp .gitignore

echo ""
echo "Added to .gitignore successfully!"