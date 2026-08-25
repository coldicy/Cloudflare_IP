# 🔧 GitHub Actions 无法推送的排查指南

## ❌ 问题现象
Action 执行成功，但仓库没有更新（没有新的 commit）

## ✅ 已修复的关键点

### 1. **权限配置** (已更新)
```yaml
permissions:
  contents: write  # 写入代码
  actions: write   # 写入 Actions
```

### 2. **Checkout 时指定 Token** (已更新)
```yaml
uses: actions/checkout@v4
with:
  fetch-depth: 0
  token: ${{ secrets.GITHUB_TOKEN }}  # ← 关键！
```

### 3. **正确的 Push 命令** (已更新)
```bash
# 明确指定推送到当前分支
git push origin HEAD:$CURRENT_BRANCH
```

### 4. **Git 用户邮箱格式** (已更新)
```bash
# 使用标准格式
git config --global user.email '41898282+github-actions[bot]@users.noreply.github.com'
```

---

## 🚨 还需要你手动完成的步骤

### 步骤 1: 替换上游仓库 URL
编辑 `.github/workflows/sync-clean.yml`，找到这一行：
```yaml
UPSTREAM_URL="https://github.com/ORIGINAL_OWNER/ORIGINAL_REPO.git"
```
替换为你要同步的**真实上游仓库地址**。

### 步骤 2: 检查仓库设置
1. 进入你的 GitHub 仓库页面
2. 点击 **Settings** → **Actions** → **General**
3. 确保 **Workflow permissions** 设置为：
   - ✅ **Read and write permissions** (不是 Read only)
4. 勾选 ✅ **Allow GitHub Actions to create and approve pull requests**

### 步骤 3: 检查分支保护规则
如果启用了分支保护：
1. 进入 **Settings** → **Branches** → **Branch protection rules**
2. 确保没有阻止 Actions 推送的规则
3. 或者添加例外：✅ **Allow GitHub Actions to bypass**

### 步骤 4: 手动触发测试
1. 进入仓库的 **Actions** 标签页
2. 点击左侧的 **Sync and Clean Data** 工作流
3. 点击 **Run workflow** 按钮
4. 等待运行完成
5. 查看日志，确认有 `🎉 Successfully pushed updates!` 输出
6. 检查仓库是否有新的 commit

---

## 📋 常见错误排查

### 错误 1: "Permission denied" 或 "403 Forbidden"
**原因**: Workflow 权限不足  
**解决**: Settings → Actions → General → 开启 Read and write permissions

### 错误 2: "nothing to commit, working tree clean"
**原因**: 数据没有变化，这是正常的  
**解决**: 无需处理，说明数据和上次一样

### 错误 3: "remote upstream not found"
**原因**: 上游仓库 URL 未正确配置  
**解决**: 检查 yml 文件中的 `UPSTREAM_URL` 是否正确

### 错误 4: Action 运行了但没有 commit
**原因**: 
- 可能没有检测到变更（正常）
- 或者 push 命令失败  
**解决**: 查看 Action 日志的最后几行，找错误信息

---

## 🔍 验证清单

- [ ] 已替换 `UPSTREAM_URL` 为真实地址
- [ ] Workflow permissions 已设为 Read and write
- [ ] 没有分支保护规则阻止推送
- [ ] 手动触发过测试并查看日志
- [ ] 日志显示 `Successfully pushed updates!`

---

## 💡 提示

如果还是不行，请提供：
1. Action 的运行日志截图
2. 你的仓库是否为私有仓库
3. 是否使用了自定义 GITHUB_TOKEN

这样可以更精确地定位问题。
