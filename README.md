# 酒店管理系统

## 项目概述
酒店管理系统是一个基于Flask框架开发的酒店会议室预订和管理系统，支持用户管理、会议室预订、会议管理、成本跟踪等功能。

## 技术架构

### 后端技术
- **Flask**: Python Web框架
- **Flask-SQLAlchemy**: ORM数据库工具
- **Flask-Migrate**: 数据库迁移工具
- **Flask-Login**: 用户认证管理
- **Flask-WTF**: 表单处理和验证
- **SQLite**: 轻量级数据库系统

### 前端技术
- **Jinja2**: 模板引擎
- **HTML5/CSS3**: 页面结构和样式
- **Bootstrap**: 响应式UI框架

## 项目结构

```
Hotel-Management-System-Flask-App/
├── app/
│   ├── templates/
│   │   ├── base.html
│   │   ├── index.html
│   │   ├── login.html
│   │   ├── register.html
│   │   ├── book.html
│   │   ├── roomavailable.html
│   │   ├── roomavailablelist.html
│   │   ├── roomoccupation.html
│   │   ├── roomoccupationlist.html
│   │   ├── costs.html
│   │   ├── costcheck.html
│   │   ├── allrecords.html
│   │   └── ...
│   ├── __init__.py
│   ├── models.py
│   ├── forms.py
│   └── routes.py
├── migrations/
├── config.py
├── lab2.py
├── lab2.db
└── README.md
```

## 核心功能

### 1. 用户管理
- 用户注册和登录
- 用户信息管理
- 团队管理

### 2. 会议室管理
- 会议室信息管理
- 会议室可用性查询
- 会议室占用情况查看

### 3. 会议管理
- 会议预订
- 会议参与者管理
- 会议状态管理
- 会议取消

### 4. 成本管理
- 会议成本跟踪
- 成本明细记录
- 成本统计

### 5. 业务伙伴管理
- 业务伙伴信息管理
- 会议邀请业务伙伴

## 数据库设计

### 主要数据表
- **user**: 用户信息
- **team**: 团队信息
- **room**: 会议室信息
- **meeting**: 会议信息
- **cost_log**: 成本记录
- **businesspartner**: 业务伙伴信息
- **participants_user**: 用户-会议关联
- **participants_partner**: 业务伙伴-会议关联

## 快速开始

### 环境要求
- Python 3.6+
- pip

### 安装步骤
1. 克隆仓库
   ```bash
   git clone https://github.com/sangjiexun/Hotel-Management-System-Flask-App.git
   cd Hotel-Management-System-Flask-App
   ```

2. 安装依赖
   ```bash
   pip install -r requirements.txt
   ```

3. 初始化数据库
   ```bash
   flask db init
   flask db migrate
   flask db upgrade
   ```

4. 运行应用
   ```bash
   python lab2.py
   ```

## 部署说明

### 生产环境部署
- 使用Gunicorn作为WSGI服务器
- 使用Nginx作为反向代理
- 配置HTTPS
- 启用生产模式

### 环境变量配置
- `SECRET_KEY`: 应用密钥
- `DATABASE_URL`: 数据库连接URL
- `DEBUG`: 调试模式

## 许可证

MIT License

---

# Hotel Management System

## Project Overview
Hotel Management System is a Flask-based hotel meeting room booking and management system, supporting user management, meeting room booking, meeting management, cost tracking, and other functions.

## Technical Architecture

### Backend Technologies
- **Flask**: Python Web framework
- **Flask-SQLAlchemy**: ORM database tool
- **Flask-Migrate**: Database migration tool
- **Flask-Login**: User authentication management
- **Flask-WTF**: Form handling and validation
- **SQLite**: Lightweight database system

### Frontend Technologies
- **Jinja2**: Template engine
- **HTML5/CSS3**: Page structure and styling
- **Bootstrap**: Responsive UI framework

## Project Structure

```
Hotel-Management-System-Flask-App/
├── app/
│   ├── templates/
│   │   ├── base.html
│   │   ├── index.html
│   │   ├── login.html
│   │   ├── register.html
│   │   ├── book.html
│   │   ├── roomavailable.html
│   │   ├── roomavailablelist.html
│   │   ├── roomoccupation.html
│   │   ├── roomoccupationlist.html
│   │   ├── costs.html
│   │   ├── costcheck.html
│   │   ├── allrecords.html
│   │   └── ...
│   ├── __init__.py
│   ├── models.py
│   ├── forms.py
│   └── routes.py
├── migrations/
├── config.py
├── lab2.py
├── lab2.db
└── README.md
```

## Core Features

### 1. User Management
- User registration and login
- User information management
- Team management

### 2. Meeting Room Management
- Meeting room information management
- Meeting room availability query
- Meeting room occupation status viewing

### 3. Meeting Management
- Meeting booking
- Meeting participant management
- Meeting status management
- Meeting cancellation

### 4. Cost Management
- Meeting cost tracking
- Cost detail recording
- Cost statistics

### 5. Business Partner Management
- Business partner information management
- Meeting invitation for business partners

## Database Design

### Main Data Tables
- **user**: User information
- **team**: Team information
- **room**: Meeting room information
- **meeting**: Meeting information
- **cost_log**: Cost records
- **businesspartner**: Business partner information
- **participants_user**: User-meeting association
- **participants_partner**: Business partner-meeting association

## Quick Start

### Environment Requirements
- Python 3.6+
- pip

### Installation Steps
1. Clone the repository
   ```bash
   git clone https://github.com/sangjiexun/Hotel-Management-System-Flask-App.git
   cd Hotel-Management-System-Flask-App
   ```

2. Install dependencies
   ```bash
   pip install -r requirements.txt
   ```

3. Initialize database
   ```bash
   flask db init
   flask db migrate
   flask db upgrade
   ```

4. Run the application
   ```bash
   python lab2.py
   ```

## Deployment Instructions

### Production Environment Deployment
- Use Gunicorn as WSGI server
- Use Nginx as reverse proxy
- Configure HTTPS
- Enable production mode

### Environment Variables Configuration
- `SECRET_KEY`: Application secret key
- `DATABASE_URL`: Database connection URL
- `DEBUG`: Debug mode

## License

MIT License