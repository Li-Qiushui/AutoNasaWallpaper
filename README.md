# NASA自动壁纸更换程序

一个专门使用NASA天文图片数据库自动更换Windows桌面壁纸的Python程序。

## 功能特点

- 🌌 **NASA每日图片**: 获取NASA天文图片数据库的每日精选图片
- 🎲 **随机历史图片**: 获取NASA历史图片库中的随机图片
- 🧹 **自动清理**: 自动清理旧图片，节省磁盘空间
- 📝 **详细日志**: 记录所有操作，便于调试和监控
- ⚡ **一键运行**: 简单易用，支持命令行参数
- 🕘 **定时任务**: 支持设置Windows任务计划程序，自动定时更新

## 安装依赖

```bash
pip install -r requirements.txt
```

## 使用方法

### 基本使用
```bash
python run.py
```
程序会获取今日的NASA每日图片并设置为壁纸。

### 指定模式
```bash
# 获取今日NASA图片（默认）
python run.py today

# 获取随机历史NASA图片
python run.py random
```

### 批处理文件
双击运行 `update_wallpaper.bat` 来执行程序，包含依赖检查和错误处理。

## 自动定时更新设置

### 手动设置
1. 按 `Win + R`，输入 `taskschd.msc`，回车
2. 点击右侧 "创建基本任务"
3. 任务名称：`NASA壁纸自动更新`
4. 触发器：每天
5. 开始时间：`09:00`
6. 操作：启动程序
7. 程序：选择 `update_wallpaper.bat` 文件
8. 完成设置

### 管理定时任务
- 打开任务计划程序 (`taskschd.msc`)
- 在左侧找到 "任务计划程序库"
- 找到任务 "NASA壁纸自动更新" 进行管理
- 可以修改、删除或手动运行任务

## 图片源说明

**NASA天文图片数据库 (APOD)**
- 来源：NASA官方天文图片数据库
- 特点：高质量的天文、太空、科学图片
- 内容：包括星系、行星、星云、航天器等
- 需要：NASA API key（默认使用DEMO_KEY）

## 文件结构

```
AutoWallpaper/
├── run.py                    # 主程序
├── update_wallpaper.bat      # 批处理文件
├── setup_scheduler.bat       # 自动设置批处理文件（推荐）
├── setup_scheduler.ps1       # 自动设置PowerShell脚本
├── requirements.txt          # 依赖文件
├── README.md                # 说明文档
├── 自动设置说明.txt          # 设置说明
├── wallpapers/              # 下载的图片目录（自动创建）
└── wallpaper.log            # 日志文件（自动创建）
```

## 高级配置

### 获取NASA API Key（推荐）
1. 访问 [NASA API](https://api.nasa.gov/)
2. 注册并获取API key
3. 在代码中替换 `self.nasa_api_key = "DEMO_KEY"`

**注意**: 使用DEMO_KEY有请求频率限制，建议申请自己的API key以获得更好的体验。

### 自定义设置
- 修改 `keep_count` 参数来调整保留的图片数量
- 修改随机图片的日期范围（默认从2020年开始）
- 调整图片下载超时时间
- 修改定时任务的执行时间（在setup_scheduler.bat中修改）

## 注意事项

- 程序需要网络连接来下载图片
- 确保有足够的磁盘空间存储图片
- 程序会自动创建 `wallpapers` 目录
- 日志文件会记录所有操作，便于排查问题
- NASA API有请求频率限制，建议不要过于频繁地运行程序
- 定时任务需要确保电脑在指定时间处于开机状态

## 故障排除

如果遇到问题，请检查：
1. 网络连接是否正常
2. 是否有足够的磁盘空间
3. 查看 `wallpaper.log` 文件中的错误信息
4. 确保Python版本 >= 3.6
5. 如果使用DEMO_KEY，检查是否超过请求限制
6. 定时任务是否正常创建和运行
7. 如果PowerShell脚本闪退，尝试使用批处理文件方法

## 许可证

MIT License

Copyright (c) 2024 LiQiushui

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE. 