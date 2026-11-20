# mugsun-site

[![Site CI](https://github.com/mugsun/mugsun-site/actions/workflows/site-ci.yml/badge.svg?branch=main)](https://github.com/mugsun/mugsun-site/actions/workflows/site-ci.yml)

mugsun.com 的入口页。官网还没有做，这里只有两个页面，把访问转到文档站 [docs.mugsun.com](https://docs.mugsun.com/)。

> [!NOTE]
> `mugsun.com` 的域名解析现在没有指向 GitHub Pages，所以跳转还没有生效。文档站请直接打开 docs.mugsun.com。

## 里面有什么

| 文件 | 作用 |
| --- | --- |
| `index.html` | 首页，打开后立即跳到文档站 |
| `404.html` | 处理其余所有路径，跳到文档站的同一路径，查询参数和锚点会保留 |
| `CNAME` | GitHub Pages 的自定义域名，内容是 `mugsun.com` |
| `.nojekyll` | 让 GitHub Pages 跳过 Jekyll，原样发布文件 |
| `scripts/check-workflows.py` | CI 用的检查脚本 |

例如打开 `mugsun.com/guide/getting-started`，会跳到文档站的 `/guide/getting-started`。

## 发布

站点由 GitHub Pages 发布，没有构建步骤。推到 `main` 的提交会直接上线。

## 检查

每次推送会运行两个工作流：

| 工作流 | 检查什么 |
| --- | --- |
| Site CI | 工作流文件的权限是否只读，action 是否固定到完整的提交 SHA |
| Security scan | 用 gitleaks 扫描全部提交历史里的密钥 |

第一项可以先在本地运行：

```bash
python3 scripts/check-workflows.py
```

## 参与贡献

提交前请读[贡献指南](https://github.com/mugsun/.github/blob/main/CONTRIBUTING.md)。安全问题请按 [SECURITY.md](https://github.com/mugsun/.github/blob/main/SECURITY.md) 私下报告，不要开公开 Issue。
