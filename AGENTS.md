# AGENTS.md

本文件是 mugsun 自己的提交规则，不约束外部贡献者。

## 提交身份

新提交的作者和提交者为 `mugsun <bydongxin@gmail.com>`，不再要求使用 noreply 邮箱。

提交时用下面的命令，或在自己的 worktree 里设仓库级 config，不要改全局配置。

```bash
git -c user.name=mugsun -c user.email=bydongxin@gmail.com commit
```

已经推送的历史一律不改写。

## 合入流程

本仓不走 PR。流程是本地提交，经过审查，推到分支，检查全绿后快进 main。

还没审过的提交，不要放在跟踪 main 的分支上，也就是 upstream 为 origin/main 的分支。

推送一律写全 refspec，不用裸 `git push`，也不依赖 upstream：

```bash
git push origin <sha>:refs/heads/<分支>
```

不推 `HEAD`，例如不用 `git push origin HEAD:main`。

Mac mini 上的 zsh 会把 `$S:refs/...` 里的 `:r` 当成变量修饰符，把 refspec 改坏。

所以要么直接写 SHA 字面量，要么写成 `"${S}:refs/heads/<分支>"`。

推 main 前要核对完整 SHA 已经审过，审查结论里写的就是这个 SHA。

再用 `gh run list --commit <完整 SHA>` 核对检查结果。短 SHA 可能查不到结果，不算核对。

Site CI 和 Security scan 都成功后才能推。

把 main 合进分支产生的 merge commit 是新 SHA，同样要先在分支上跑绿。

改动 `.github/` 下任何文件的提交，必须先有安全官签字，才能进 main。

一个 worktree 只给一条工作线用，另开的工作线一律新建自己的 worktree。

推送前用 `git rev-parse HEAD` 对照审过的 SHA，一致才推。

push 被打断时，先用 `git ls-remote` 和 `ps` 确认它没有在后台跑完，再做下一步。

不 force-push，不加 `--no-verify`，不 rebase 已推送的分支。

合入后当即看 main 上这个 SHA 的 CI，作者自己删除远端分支。

新增或修改 workflow 时，触发用 `push: branches: ['**']` 加 `workflow_dispatch`。

deploy、release、publish 这类发布 workflow 的触发条件不动。

concurrency 按 3.17 写：

```yaml
concurrency:
  group: ${{ github.workflow }}-${{ github.ref }}${{ github.ref == 'refs/heads/main' && format('-{0}', github.sha) || '' }}
  cancel-in-progress: ${{ github.ref != 'refs/heads/main' }}
```

依赖基线的检查在 push 和 dispatch 下也要有基线。

分支用 `git merge-base origin/main HEAD`，main 用非全零的 `github.event.before`。

拿不到基线时报 `::error` 并失败，不得静默跳过。
