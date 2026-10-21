#!/usr/bin/env python3
"""校验 .github/workflows 的权限、触发方式和 Actions 钉 SHA。

规则（ci-checklist 3.2、3.8）：
- 每个 workflow 顶层必须是 permissions: contents: read（只读）；
  需要更多权限的 job 在 job 级单独声明。
- 禁止 pull_request_target 触发。
- uses: 必须钉 40 位 commit SHA（本地 ./ 和 docker:// 除外）。

不依赖 PyYAML，按行解析，只认本仓 workflow 的常规写法。
用法: check-workflows.py [workflows 目录]
"""
import pathlib
import re
import sys

root = pathlib.Path(sys.argv[1] if len(sys.argv) > 1 else ".github/workflows")
files = sorted(list(root.glob("*.yml")) + list(root.glob("*.yaml")))
if not files:
    print(f"{root}: 没有 workflow 文件")
    sys.exit(1)

USES = re.compile(r"^\s*(?:-\s+)?uses:\s*['\"]?([^'\"\s#]+)")
SHA = re.compile(r"^[^@]+@[0-9a-f]{40}$")
bad = []


def strip(line):
    return re.sub(r"\s+#.*$", "", line).rstrip()


for f in files:
    lines = f.read_text(encoding="utf-8").splitlines()
    top = None  # 顶层 permissions 解析结果
    for i, raw in enumerate(lines, 1):
        line = strip(raw)
        if re.search(r"\bpull_request_target\b", line) and not raw.lstrip().startswith("#"):
            bad.append(f"{f}:{i} 禁止使用 pull_request_target")
        m = USES.match(line)
        if m:
            ref = m.group(1)
            if not (ref.startswith("./") or ref.startswith("docker://") or SHA.match(ref)):
                bad.append(f"{f}:{i} uses 未钉 40 位 SHA: {ref}")
        if line.startswith("permissions:"):
            val = line.split(":", 1)[1].strip()
            if val:
                top = {"_inline": val}
            else:
                top = {}
                for sub in lines[i:]:
                    s = strip(sub)
                    if not s:
                        continue
                    if not sub.startswith((" ", "\t")):
                        break
                    k, _, v = s.strip().partition(":")
                    top[k.strip()] = v.strip()
    if top is None:
        bad.append(f"{f}: 缺少顶层 permissions: contents: read")
    elif top != {"contents": "read"}:
        bad.append(f"{f}: 顶层 permissions 只能是 contents: read，现为 {top}；"
                   "其他权限请写在 job 级")

if bad:
    print("\n".join(bad))
    sys.exit(1)
print(f"check-workflows: {len(files)} 个 workflow 通过")
