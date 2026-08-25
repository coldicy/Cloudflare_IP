# 自动同步并清洗数据

本方案提供两种自动同步上游仓库并清洗数据的方式：

## 🚀 方案一：GitHub Actions（推荐）

适用于托管在 GitHub 上的仓库，可全自动定时执行。

### 配置步骤：

1. **编辑工作流文件** `.github/workflows/sync-clean.yml`：
   - 将 `https://github.com/ORIGINAL_OWNER/ORIGINAL_REPO.git` 替换为实际的上游仓库 URL
   - 调整 `cron` 时间（默认每 5 分钟执行一次）

2. **启用 GitHub Actions**：
   - 进入仓库 Settings → Actions → General
   - 确保 Actions 已启用

3. **触发方式**：
   - ⏰ 定时触发：按 cron 表达式自动执行
   - 🖱️ 手动触发：Actions 页面 → "Sync and Clean Data" → "Run workflow"
   - 📤 Push 触发：当主分支有推送时自动执行

### Cron 时间示例：
```yaml
# 每 5 分钟
- cron: '*/5 * * * *'

# 每小时
- cron: '0 * * * *'

# 每天凌晨 2 点
- cron: '0 2 * * *'
```

---

## 💻 方案二：本地/服务器脚本

适用于本地开发或自有服务器环境。

### 使用方法：

```bash
# 基本用法（使用默认配置）
./sync_and_clean.sh

# 指定上游仓库和分支
./sync_and_clean.sh https://github.com/owner/repo.git main

# 或分步执行
git remote add upstream https://github.com/owner/repo.git
git fetch upstream
git merge upstream/main
python3 clean_data.py
```

### 自动化建议：

#### Linux/Mac 定时任务（crontab）：
```bash
# 编辑 crontab
crontab -e

# 添加以下行（每 5 分钟执行）
*/5 * * * * cd /path/to/your/repo && ./sync_and_clean.sh >> sync.log 2>&1
```

#### Windows 任务计划程序：
1. 打开"任务计划程序"
2. 创建基本任务
3. 设置触发器（如每 5 分钟）
4. 操作：启动程序 `bash.exe`
5. 参数：`-c "cd /path/to/repo && ./sync_and_clean.sh"`

---

## 📁 输出说明

清洗后的文件保存在 `cleaned/` 目录：
- `{地区代码}.txt` - 按地区分类的文件（如 HK.txt, US.txt）
- `all.txt` - 所有数据的汇总文件

格式：`IP:端口#地区`
示例：`43.126.2.1:8443#HK`

---

## ⚙️ 自定义配置

### 修改 CSV 列名
如果源文件的列名不同，编辑 `clean_data.py`：
```python
ip = row.get('你的 IP 列名', '').strip()
port = row.get('你的端口列名', '').strip()
country = row.get('你的地区列名', '').strip()
```

### 修改输出格式
在 `clean_data.py` 中第 42 行修改：
```python
entry = f"{ip}:{port}#{country}"  # 自定义格式
```

---

## 🔍 验证运行

```bash
# 测试运行
python3 clean_data.py

# 查看生成的文件
ls -la cleaned/

# 查看某个地区文件内容
head cleaned/HK.txt
```
