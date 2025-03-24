# 学习计划管理系统

一个简单的学习计划管理系统，使用Django (后端) 和Vue.js (前端) 构建。用户可以查看学习计划阶段，并添加个人笔记。

## 功能

- 分阶段的学习计划查看
- 个人笔记添加与管理
- 笔记的本地存储和云端同步
- 暗黑模式支持

## 技术栈

- 后端：Django, Django Rest Framework
- 前端：Vue.js 
- 数据库：SQLite (开发环境)

## 开发环境设置

### 后端 (Django)

```bash
# 创建虚拟环境
python -m venv venv
source venv/bin/activate  # 在Windows上使用: venv\Scripts\activate

# 安装依赖
pip install -r requirements.txt

# 运行迁移
python manage.py migrate

# 加载测试数据
python manage.py loaddata planner/fixtures/initial_data.json

# 启动开发服务器
python manage.py runserver
```

### 前端 (Vue)

```bash
# 进入前端目录
cd frontend

# 安装依赖
npm install

# 启动开发服务器
npm run serve
```

## 生产环境部署

详见文档 [deployment.md](deployment.md)

## 贡献指南

1. Fork 该仓库
2. 创建特性分支 (`git checkout -b feature/amazing-feature`)
3. 提交更改 (`git commit -m 'Add some amazing feature'`)
4. 推送到分支 (`git push origin feature/amazing-feature`)
5. 创建Pull Request

## 许可证

MIT License 