#!/usr/bin/env bash
# 探 Addressables catalog 并枚举按需 .bundle(S3 LIST 多被拒,catalog 是全集来源)。
# 关键: Addressables 运行时文件在 streamingAssetsUrl 下的 **aa/** 子目录
#       (unityConfig 里 streamingAssetsUrl = <CDN>/addressables_assets,故 RuntimePath = .../addressables_assets/aa)。
#       Addressables 2.x = 二进制 catalog.bin(非 catalog.json);用 strings 枚举 bundle 名。
# 用: bash addressables-probe.sh <CDN_BASE> <code>
CDN="${1:?CDN_BASE}"; CODE="${2:?code}"; A="$CDN/addressables_assets"
echo "=== 探 aa/ 下的 Addressables 运行时文件(ss03 实测命中点) ==="
for p in aa/settings.json aa/catalog.bin aa/catalog.hash aa/catalog.json catalog.bin settings.json; do
  echo -n "$A/$p -> "; curl -s -m 8 -o /dev/null -w "%{http_code} %{size_download}B\n" "$A/$p"
done
echo ""
echo "=== 拉 catalog.bin + 枚举 bundle 名(strings) ==="
tmp=$(mktemp); curl -s -m 15 "$A/aa/catalog.bin" -o "$tmp"
if [ -s "$tmp" ]; then
  echo "bundle 名(<group>_assets_all_<hash>.bundle):"
  strings -n 8 "$tmp" | grep -aoE "[A-Za-z0-9_()/.-]+_(assets|scenes)_all_[0-9a-f]{32}\.bundle" | sort -u
  echo "—— locale/朝向/场景线索:"
  strings -n 4 "$tmp" | grep -aiE "horizontal|vertical|landscape|\.unity|scene|prefab" | sort -u | head
fi
rm -f "$tmp"
cat <<'NOTE'

注意:
- bundle 全名带 group 前缀(如 localization-assets-malaysian_assets_all_<hash>.bundle),不是裸 <hash>.bundle。
- bundle 的实际 URL 路径可能再带 BuildTarget/profile 前缀;若全名在 aa/ 与根都 403,从【线② 浏览器 Network】抓一个 .bundle 请求看真实 URL。
- ss03 实测:catalog 里 30 个 bundle 全是 localization(无美术/场景/横屏包)→ 游戏本体与双朝向布局都在 data.unity3d,Addressables 仅本地化。
NOTE
