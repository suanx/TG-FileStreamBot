<hr>

<h1 align="center">Telegram File Stream Bot</h1>
<p align="center">
  <a href="https://github.com/EverythingSuckz/TG-FileStreamBot">
    <img src="https://socialify.git.ci/suanx/TG-FileStreamBot/image?font=Source%20Code%20Pro&logo=https://telegra.ph/file/01385a9f4cf0419682b87.png&pattern=Circuit%20Board&theme=Dark" alt="Cover Image" width="650">
  </a>
  <p align="center">
    一个生成Telegram内<b>文件直链</b>的机器人。
  </p>
</p>

<hr>

此仓库源于 [EverythingSuckz/TG-FileStreamBot](https://github.com/EverythingSuckz/TG-FileStreamBot) 的 [python](https://github.com/EverythingSuckz/TG-FileStreamBot/tree/python) 分支，遵循 [GNU Affero General Public License](https://www.gnu.org/licenses/agpl-3.0.zh-cn.html)。

## 修复内容

### 安全修复
- **docker-compose.yml**: 移除硬编码敏感信息，改为从 `.env` 文件读取
- **依赖更新**: 更新 aiohttp 到 >=3.9.0 (修复 CVE-2023-25527, CVE-2023-3164)
- **速率限制**: 添加每 IP 60 秒内最多 30 次请求的限流保护

### 稳定性修复
- **BIN_CHANNEL 验证**: 启动时检查 BIN_CHANNEL 是否为空，为空则报错退出
- **异常处理**: 保留完整堆栈信息便于调试
- **后台任务管理**: 添加任务取消机制，防止资源泄漏
- **客户端初始化**: 失败时抛出异常而非静默忽略

### 代码质量
- **拼写修正**: FIleNotFound → FileNotFound
- **Python 版本**: 升级至 3.12-alpine，使用多阶段构建减小镜像体积
- **类型安全**: 添加 from_user 判空检查，parse_file_id 显式返回 None

## 这是啥

这是一个 Telegram 机器人，它将为您提供 Telegram 文件的流链接，无需等待下载完成。

## 部署

### Docker Compose 部署

1. 克隆仓库：
   ```bash
   git clone https://github.com/suanx/TG-FileStreamBot.git
   cd TG-FileStreamBot
   ```

2. 创建 `.env` 文件，填入 Telegram 配置：
   ```
   API_ID=your_api_id
   API_HASH=your_api_hash
   BOT_TOKEN=your_bot_token
   BIN_CHANNEL=your_channel_id
   PORT=9191
   NO_PORT=true
   FQDN=example.com
   HAS_SSL=true
   ```

3. 编辑 `docker-compose.yml`，将镜像地址修改为您的 GitHub 用户名和仓库名：
   ```yaml
   image: ghcr.io/suanx/tg-filestreambot:latest
   ```

4. 启动：
   ```bash
   docker-compose up -d
   ```

### 环境变量

#### 必选变量

- `API_ID`：Telegram 帐户的 API ID，从 [my.telegram.org](https://my.telegram.org) 获取。
- `API_HASH`：Telegram 帐户的 API 哈希，从 [my.telegram.org](https://my.telegram.org) 获取。
- `BOT_TOKEN`：机器人令牌，从 [@BotFather](https://telegram.dog/BotFather) 获取。
- `BIN_CHANNEL`：日志频道 ID。创建频道后，发布一条消息，回复该消息给 [@missrose_bot](https://telegram.dog/MissRose_bot) 使用 `/id` 命令获取。

#### 可选变量

| 变量 | 默认值 | 说明 |
|------|--------|------|
| `HASH_LENGTH` | 6 | 生成 URL 的哈希长度（6~63） |
| `SLEEP_THRESHOLD` | 60 | 洪水等待异常睡眠阈值（秒） |
| `WORKERS` | 6 | 并发工作者数量 |
| `PORT` | 8080 | Web 服务监听端口 |
| `WEB_SERVER_BIND_ADDRESS` | 0.0.0.0 | 服务器绑定地址 |
| `NO_PORT` | False | URL 中是否省略端口号 |
| `FQDN` | `WEB_SERVER_BIND_ADDRESS` | 完全限定域名 |
| `HAS_SSL` | False | 是否使用 HTTPS |
| `KEEP_ALIVE` | False | 是否启用自保活 ping（PaaS 免费层有用） |
| `PING_INTERVAL` | 1200 | 自保活 ping 间隔（秒） |
| `USE_SESSION_FILE` | False | 使用会话文件而非内存数据库 |
| `ALLOWED_USERS` | 空 | 用户白名单（逗号分隔的用户 ID 或用户名） |

#### 多客户端支持

```
MULTI_TOKEN1=your_bot_token_1
MULTI_TOKEN2=your_bot_token_2
```

> **警告**：所有机器人必须加入 `BIN_CHANNEL` 才能正常工作。

## GitHub Actions 自动构建

推送代码到 `release` 分支时，GitHub Actions 会自动构建 Docker 镜像并推送到 **GitHub Container Registry (ghcr.io)**。

- 镜像地址：`ghcr.io/suanx/tg-filestreambot:latest`

## 使用

直接发送/转发文件，稍等片刻，机器人将会返回直链。

![](https://go.xiaobai.mom/https://telegra.ph/file/4ed1d0d46dfaf3f7ff39c.png)
