#!/bin/bash
# 最终版：仅检查URL是否包含任意域名字符串，无需全词匹配

# 检查参数
if [ $# -ne 3 ]; then
    echo "用法: $0 <域名列表文件> <URL列表文件> <输出目录>" >&2
    exit 1
fi

DOMAIN_FILE=$1
URL_FILE=$2
OUTPUT_DIR=$3

# 创建输出目录
mkdir -p "$OUTPUT_DIR"
MATCHED="$OUTPUT_DIR/matched_urls.txt"
UNMATCHED="$OUTPUT_DIR/unmatched_urls.txt"
FIRST_LEVEL="$OUTPUT_DIR/unmatched_first_level.txt"
SECOND_LEVEL="$OUTPUT_DIR/unmatched_second_level.txt"

# 清空文件
> "$MATCHED" > "$UNMATCHED" > "$FIRST_LEVEL" > "$SECOND_LEVEL"

# 预处理域名：转义所有特殊字符（除.外）、去重、小写
DOMAINS=$(cat "$DOMAIN_FILE" | 
          tr '[:upper:]' '[:lower:]' |        # 转小写
          sed -e 's/[()[?*+^$|]/\\&/g' -e '/^$/d' |  # 转义特殊字符（保留.）
          sort -u |                            # 去重
          paste -sd '|' -)                     # 拼接为正则表达式

# 处理URL文件：移除隐藏字符（如零宽度空格）
CLEAN_URL_FILE=$(mktemp)
sed -e 's/^\xef\xbb\xbf//' "$URL_FILE" > "$CLEAN_URL_FILE"  # 移除UTF-8 BOM头

# 并行处理URL（使用awk检查是否包含任意域名）
awk -v dom_re="$DOMAINS" -v first="$FIRST_LEVEL" -v second="$SECOND_LEVEL" -v matched="$MATCHED" -v unmatched="$UNMATCHED" '
    {
        url = $0;
        url_tolower = tolower(url);
        # 检查是否包含任意域名（不区分大小写，无需全词匹配）
        if (url_tolower ~ dom_re) {
            print url > matched;
            next;
        }
        # 处理不匹配的URL
        print url > unmatched;
        
        # 提取路径（支持带端口和参数的URL）
        match(url, /:\/\/[^\/:]+(:[0-9]+)?/, host_part);
        path = substr(url, RSTART + RLENGTH);
        path = gensub(/\/$/, "", "g", path);        # 移除末尾/
        path = gensub(/\?.*$/, "", "g", path);       # 移除参数
        
        # 判断是否为一级链接（路径为空）
        if (path == "") {
            print url > first;
        } else {
            print url > second;
        }
    }' "$CLEAN_URL_FILE"

# 清理临时文件
rm -f "$CLEAN_URL_FILE"

echo "处理完成，结果保存至：$OUTPUT_DIR"
