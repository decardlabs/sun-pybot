# /home/ubuntu/wecom-service/app.py
from http.server import BaseHTTPRequestHandler, HTTPServer
import json

# 定义请求处理器
class WecomCallbackHandler(BaseHTTPRequestHandler):
    # 处理 GET 请求（企业微信回调验证）
    def do_GET(self):
        if self.path == '/wecom/callback':
            # 企业微信回调验证逻辑（示例：返回 echostr，实际需替换为你的验证逻辑）
            self.send_response(200)
            self.send_header('Content-type', 'text/plain')
            self.end_headers()
            self.wfile.write(b'Hello Wecom Callback!')
        elif self.path == '/health':
            # 健康检查接口
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps({"status": "ok"}).encode('utf-8'))
        else:
            self.send_response(404)
            self.end_headers()
            self.wfile.write(b'404 Not Found')

    # 处理 POST 请求（企业微信消息接收）
    def do_POST(self):
        if self.path == '/wecom/callback':
            # 读取请求体
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            
            # 处理消息（示例：打印消息，实际需替换为你的业务逻辑）
            print(f"Received Wecom message: {post_data.decode('utf-8')}")
            
            # 返回成功响应
            self.send_response(200)
            self.send_header('Content-type', 'text/plain')
            self.end_headers()
            self.wfile.write(b'success')
        else:
            self.send_response(404)
            self.end_headers()

# 启动服务（监听容器内的 3000 端口，0.0.0.0 允许容器外部访问）
def run_server():
    server_address = ('0.0.0.0', 3000)  # 必须用 0.0.0.0，不能用 127.0.0.1（容器内 127.0.0.1 仅容器自身可访问）
    httpd = HTTPServer(server_address, WecomCallbackHandler)
    print('Starting Wecom callback server on port 3000...')
    httpd.serve_forever()

if __name__ == '__main__':
    run_server()