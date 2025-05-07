## 使用 Claw Cloud 免费部署 Gemini 反向代理教程 由[@IDeposit](https://github.com/IDeposit)编写

本教程将指导您如何利用 Claw Cloud 的免费额度部署一个 Gemini API 的反向代理服务。

**✨ 优势:**

1.  **完全免费:** 利用平台的免费额度，无需支付费用。
2.  **操作简单:** 部署过程直观，易于上手。
3.  **国内友好:** 部分节点（如日本）对中国大陆访问速度较好。
4.  **流量充足:** 每月提供 10GB 免费流量，对于个人使用 Gemini API 来说通常绰绰有余。

**🔑 前置条件 (满足其一即可):**

*   拥有一个注册时间超过 180 天的 GitHub 账号 (每月可获得 $5 赠金，理论永久)。
*   使用 Gmail 账号登录 (只能获得一个月 $5 赠金)，多个谷歌账号即可无限续杯。

**🚀 部署步骤:**
---
1.  **登录 Claw Cloud 控制台**
    访问 [https://console.run.claw.cloud/signin](https://console.run.claw.cloud/signin) 并使用您的 GitHub 或 Gmail 账号登录。
    ![登录界面](./img/claw/1.png)
---
2.  **选择区域 (首次登录)**
    首次登录时会提示选择服务器区域。此选择后续可以更改，这里以选择 `日本 (Japan)` 为例（目前日本和新加坡服务器处于高负载状态，请使用其他区域）,如果项目持续卡在create或waiting，请删除项目并在此切换地区重试（请一定要删除原项目，否则5美元赠金无法支持一个月的消耗）。
    ![选择区域](./img/claw/2.png)
---
3.  **进入 APP Launchpad**
    在控制台主界面，找到并点击 **APP Launchpad**。
    ![进入 APP Launchpad](./img/claw/3.png)
---
4.  **创建新应用**
    点击 **Create APP** 按钮开始创建。
    ![创建APP](./img/claw/4.png)
---
5.  **配置应用信息**
    *   **Application Name:** 填写一个应用名称（必须是**英文**，且以**小写字母**开头）。
    *   **Image Name:** 输入镜像地址 `ghcr.io/wyeeeee/hajimi:latest`
    * 配置端口为7860并打开
    ![填写应用信息](./img/claw/11.png)
> 在日本区域，创建容器后绑定自定义域名有概率失败，只能 http 访问。请删除容器后重新创建并绑定，或者使用新加坡的容器。参见 https://question.run.claw.cloud/questions/10010000000000298
---
6.  **找到环境变量设置**
    向下滚动页面，找到 **Environment Variables** 部分。
    ![环境变量部分](./img/claw/6.png)
---
7.  **填写环境变量**
    从https://github.com/wyeeeee/hajimi/releases/tag/settings 下载settings.txt
    按照注释配置相应内容，您可以保留这个txt作为本地备份<br>
    注意：大部分设置都拥有默认值，如果您不理解设置内容，只需要填写拥有的gemini key到对应位置即可
    ![配置文件](./img/claw/settings.png)
    
    点击claw的 **Add environment variable**将txt文件内容复制并粘贴进去

    ![填写环境变量](./img/claw/env.png)
---
8.  **部署应用**
    返回页面顶部，点击 **Deploy application** 按钮。
    ![部署应用](./img/claw/8.png)
---

9.  **等待部署完成**
    等待应用状态 (`Status`) 变为 **Running**，这表示部署已成功。
    ![部署成功状态](./img/claw/9.png)
---
10. **获取反代地址并使用**
    *   切换到 **Network** 标签页。
    *   在右侧会看到一个 URL 地址，这就是你的反向代理地址。点击 **Copy** 复制它。

    ![获取反代地址](./img/claw/10.png)
11. **访问前端界面**
    * 把你刚刚复制的链接地址在浏览器中打开，就能看到如图所示的前端界面。
    * 如果无法显示，请耐心等待，若仍无法打开，请将链接开头的https改为http
    ![前端界面](./img/claw/hajimi.png)
12. **在酒馆中使用**
    * 进入到酒馆界面，打开API连接配置（即插头），api选择 聊天补全，聊天补全来源选择 自定义（兼容 OpenAI）
    * 把您刚刚复制的链接地址粘贴到自定义端点（基础 URL）
    * 在链接后方加上/v1（若您在上一步中使用的是http，在这里也要把链接开头的https改成http）
    * 自定义api秘钥填写您配置的password（不能为空，默认为123）
    此时酒馆应如图所示
     ![sillytavern](./img/claw/sillytavern.png)
    * 如果您在填写完以上信息后，下方没有模型供您选择，请您点击连接按钮，此时您应该可以看到模型，选择模型即可使用
13. **更新**
![sillytavern](./img/claw/update.png)

---

🎉 恭喜！你现在拥有了一个免费的 Gemini 反向代理服务。

---

# 如果你想使用Vertex 请看这里

1.如图所示在环境变量设置中添加 ENABLE_VERTEX=true
![环境变量](./img/claw/vertex1.png)

---
2.根据图片添加文件映射/app/credentials/google-key.json 并填入你的Vertex JSON

![映射1](./img/claw/vertex2.png)

![映射2](./img/claw/vertex3.png)

---
3.部署应用(和上面教程第八步开始一样)

![部署成功状态](./img/claw/8.png)
