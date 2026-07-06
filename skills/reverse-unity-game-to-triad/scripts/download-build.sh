#!/usr/bin/env bash
# 拉 + 解压 ss 系列 Unity WebGL 构建(公开 S3,免鉴权)。
# 用: bash download-build.sh <CDN_BASE> <code> [outdir]
#   CDN_BASE 形如 https://dev-assets-hybergaming.s3.us-west-2.amazonaws.com/ss03
set -e
CDN="${1:?CDN_BASE}"; CODE="${2:?code}"; OUT="${3:-build_$CODE}"
PKG="$CDN/unity_game_package/gz"
mkdir -p "$OUT"; cd "$OUT"
echo "=== version.json ==="; curl -s -m 10 "$PKG/version.json" | tee version.json; echo
for f in "$CODE.loader.js" "$CODE.framework.js.gz" "$CODE.wasm.gz" "$CODE.data.gz"; do
  echo -n "pull $f -> "; curl -s -m 240 "$PKG/$f" -o "$f" -w "%{http_code} %{size_download}B\n"
done
gunzip -kf "$CODE.data.gz" "$CODE.wasm.gz" "$CODE.framework.js.gz" 2>/dev/null || true
echo "=> $OUT/  下一步: python3 unpack-unitywebdata.py $OUT/$CODE.data"
echo "   (Addressables 按需内容另取: bash addressables-probe.sh \"$CDN\" $CODE)"
