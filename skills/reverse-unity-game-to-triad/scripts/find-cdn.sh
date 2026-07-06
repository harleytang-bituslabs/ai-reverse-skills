#!/usr/bin/env bash
# 找 ss 系列(Unity WebGL)游戏的 CDN base + Unity 包路径。
# 真相: cdnUrl/unityVersion 在源码里是「运行时从网关取」(私有 @hg 中间件,端点猜不到),
#       但【线上部署的构建把它硬编码进 JS chunk 了】—— 抓部署页的 chunk grep 出来即可。
# 用: bash find-cdn.sh <游戏宿主URL，如 https://game.dev.hybergaming.com/ss03>
set -e
HOST="${1:?用法: find-cdn.sh https://game.<env>.hybergaming.com/<code>}"
base="$(echo "$HOST" | grep -oE 'https?://[^/]+')"
work="$(mktemp -d)"
curl -s -m 12 -L "$HOST/" -o "$work/index.html"
# 收集页面引用的 JS chunk 并下载
grep -oE '(src|href)="[^"]+\.js"' "$work/index.html" | sed 's/.*="//;s/"//' | while read -r p; do
  case "$p" in http*) u="$p";; *) u="$base$p";; esac
  curl -s -m 15 "$u" -o "$work/$(echo "$p" | tr '/?:' '___')" 2>/dev/null || true
done
echo "=== CDN host(S3/CloudFront/OSS;注意 minified JS 里 host 常与 https:// 分开拼接,故不锚定 scheme) ==="
# host 字面量(scheme 可有可无): *.s3.<region>.amazonaws.com / *.cloudfront.net / *.oss-*.aliyuncs.com / *cdn*
grep -rhoE "(https?://)?[A-Za-z0-9._-]+\.(s3[.-][A-Za-z0-9.-]*amazonaws\.com|cloudfront\.net|oss-[A-Za-z0-9.-]+\.aliyuncs\.com)(/[A-Za-z0-9._/-]*)?|(https?://)?[A-Za-z0-9._-]*cdn[A-Za-z0-9._-]+\.[A-Za-z]{2,}(/[A-Za-z0-9._/-]*)?" "$work" 2>/dev/null | sort -u
echo ""
echo "=== Unity 包 / 接口路径线索 ==="
grep -rhoE "unity_game_package|addressables_assets|asset_v[0-9]+|/game/[a-z0-9-]+-(api|socket)[a-z0-9/_.-]*|version\.json" "$work" 2>/dev/null | sort -u
echo ""
echo "下一步: 取 <S3_BASE>(形如 https://<bucket>.s3.<region>.amazonaws.com/<code>) 交给 download-build.sh。"
echo "(ss03 实测 = https://dev-assets-hybergaming.s3.us-west-2.amazonaws.com/ss03)"
