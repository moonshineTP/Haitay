#!/usr/bin/env bash
# Biên dịch báo cáo LaTeX bằng latexmk, đưa PDF ra thư mục gốc và dọn file thừa.
#
# Cách dùng:
#   bash scripts/compile.sh [target.tex]   # biên dịch (mặc định main.tex)
#   bash scripts/compile.sh --clean        # chỉ dọn file thừa trong mã nguồn
#
# File trung gian nằm trong build/ để latexmk biên dịch tăng dần, không dựng lại từ đầu.
# File thừa trong thư mục nguồn được chuyển vào .trash/<thời gian>/ thay vì xóa hẳn.

set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT"

BUILD_DIR="build"
TRASH_DIR=".trash/$(date +%Y%m%d-%H%M%S)"
SOURCE_DIRS=(. chapters figures)

JUNK_EXTENSIONS=(aux log out toc lof lot fls fdb_latexmk synctex.gz bbl blg nav snm vrb idx ilg ind lol)

# Chuyển file thừa trong một thư mục vào .trash, giữ nguyên tên thư mục con.
sweep_junk() {
    local dir="$1" ext file
    for ext in "${JUNK_EXTENSIONS[@]}"; do
        for file in "$dir"/*."$ext"; do
            [[ -e "$file" ]] || continue
            mkdir -p "$TRASH_DIR/$dir"
            mv -- "$file" "$TRASH_DIR/$dir/"
            echo "Đã chuyển vào trash: $file"
        done
    done
}

sweep_sources() {
    local dir
    for dir in "${SOURCE_DIRS[@]}"; do
        sweep_junk "$dir"
    done
}

if [[ "${1:-}" == "--clean" ]]; then
    sweep_sources
    exit 0
fi

TARGET="${1:-main.tex}"
PDF_NAME="${TARGET%.tex}.pdf"
# \include ghi file .aux của từng chương vào đúng thư mục con của build/.
for dir in "${SOURCE_DIRS[@]}"; do
    mkdir -p "$BUILD_DIR/$dir"
done

# halt-on-error khiến latexmk báo lỗi khi thiếu file, thay vì xuất PDF thiếu nội dung.
if ! latexmk -pdf -outdir="$BUILD_DIR" \
        -pdflatex="pdflatex -interaction=nonstopmode -halt-on-error -file-line-error %O %S" \
        "$TARGET"; then
    echo "Biên dịch thất bại. Xem log trong $BUILD_DIR/ để tìm lỗi." >&2
    exit 1
fi

cp -- "$BUILD_DIR/$PDF_NAME" "$ROOT/$PDF_NAME"
sweep_sources
echo "Hoàn tất: $ROOT/$PDF_NAME"
