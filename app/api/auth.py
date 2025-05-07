from fastapi import HTTPException, Request
import app.config.settings as settings
# 密码验证依赖
async def verify_password(request: Request, PASSWORD: str = None):
    """验证请求中的Bearer令牌是否与配置的密码匹配"""
    if PASSWORD:
        auth_header = request.headers.get("Authorization")
        if not auth_header or not auth_header.startswith("Bearer "):
            raise HTTPException(
                status_code=401, detail="Unauthorized: Missing or invalid token")
        token = auth_header.split(" ")[1]
        if token != PASSWORD:
            raise HTTPException(
                status_code=401, detail="Unauthorized: Invalid token")


