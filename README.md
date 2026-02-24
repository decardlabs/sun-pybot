# Wecom Callback Server

一个简单的企业微信回调服务器，使用 Python 内置 HTTP 服务器实现。

## 功能说明

### 代码结构

```
app.py
├── WecomCallbackHandler  # HTTP 请求处理器类
│   ├── do_GET()         # 处理 GET 请求
│   │   ├── /wecom/callback  - 企业微信回调验证接口
│   │   └── /health          - 健康检查接口
│   └── do_POST()        # 处理 POST 请求
│       └── /wecom/callback  - 接收企业微信消息推送
└── run_server()         # 启动服务器（监听 0.0.0.0:3000）
```

### API 接口

| 方法 | 路径 | 说明 |
|------|------|------|
| GET | `/wecom/callback` | 企业微信回调验证，用于配置回调 URL 时的验证 |
| GET | `/health` | 健康检查接口，返回服务状态 |
| POST | `/wecom/callback` | 接收企业微信推送的消息 |

### 响应示例

**健康检查 (`GET /health`)**
```json
{
  "status": "ok"
}
```

## 部署指南

### 环境要求

- Ubuntu 20.04+ / Ubuntu 22.04+
- Python 3.6+

### 安装步骤

#### 1. 安装 Python3（如未安装）

```bash
sudo apt update
sudo apt install -y python3 python3-pip
```

验证安装：
```bash
python3 --version
```

#### 2. 下载代码

```bash
# 创建应用目录
mkdir -p /opt/wecom-service
cd /opt/wecom-service

# 将 app.py 上传到该目录
# 或使用 git clone（如果是从仓库拉取）
```

#### 3. 手动运行

```bash
cd /opt/wecom-service
python3 app.py
```

服务将在端口 3000 启动，输出：
```
Starting Wecom callback server on port 3000...
```

#### 4. 使用 Systemd 服务部署（推荐）

创建 systemd 服务文件：

```bash
sudo tee /etc/systemd/system/wecom-service.service << 'EOF'
[Unit]
Description=Wecom Callback Server
After=network.target

[Service]
Type=simple
User=www-data
WorkingDirectory=/opt/wecom-service
ExecStart=/usr/bin/python3 /opt/wecom-service/app.py
Restart=always
RestartSec=5

[Install]
WantedBy=multi-user.target
EOF
```

设置权限并启动服务：

```bash
# 设置目录权限
sudo chown -R www-data:www-data /opt/wecom-service

# 重载 systemd
sudo systemctl daemon-reload

# 启动服务
sudo systemctl start wecom-service

# 设置开机自启
sudo systemctl enable wecom-service
```

查看服务状态：
```bash
sudo systemctl status wecom-service
```

查看日志：
```bash
sudo journalctl -u wecom-service -f
```

### 端口映射配置

#### 防火墙配置（UFW）

如果启用了 UFW 防火墙，开放 3000 端口：

```bash
sudo ufw allow 3000/tcp
sudo ufw reload
```

#### 使用 Nginx 反向代理（可选，推荐用于生产环境）

安装 Nginx：
```bash
sudo apt install -y nginx
```

创建 Nginx 配置文件：
```bash
sudo tee /etc/nginx/sites-available/wecom-service << 'EOF'
server {
    listen 80;
    server_name your-domain.com;  # 替换为你的域名

    location / {
        proxy_pass http://127.0.0.1:3000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
EOF
```

启用配置：
```bash
sudo ln -s /etc/nginx/sites-available/wecom-service /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl restart nginx
```

### 测试服务

```bash
# 测试健康检查接口
curl http://localhost:3000/health

# 测试回调接口
curl http://localhost:3000/wecom/callback

# 测试 POST 消息接收
curl -X POST http://localhost:3000/wecom/callback \
  -H "Content-Type: application/json" \
  -d '{"msg":"test"}'
```

## 配置说明

当前代码中使用的端口为 3000，如需修改：

编辑 `app.py` 第 47 行：
```python
server_address = ('0.0.0.0', 3000)  # 修改为你需要的端口
```

**注意**：必须使用 `0.0.0.0` 而不是 `127.0.0.1`，否则外部无法访问服务。

## 开发说明

### 企业微信回调验证

当前代码中的回调验证逻辑为示例代码，仅返回固定字符串。实际使用时需要根据企业微信的验证规则实现：

1. 解密收到的 `echostr` 参数
2. 使用企业微信提供的 Token、EncodingAESKey 进行验证
3. 返回解密后的明文

### 消息处理

POST 请求处理目前仅打印接收到的消息。实际使用时需要：
1. 解析 XML/JSON 格式的消息
2. 验证消息签名
3. 实现业务逻辑并返回响应

## 许可证

MIT
# sun-pybot
# sun-pybot
# sun-pybot
