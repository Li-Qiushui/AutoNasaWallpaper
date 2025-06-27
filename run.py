import os
import sys
import json
import time
import random
import logging
import requests
from datetime import datetime
from pathlib import Path
import ctypes
from ctypes import wintypes
import urllib.parse

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('wallpaper.log', encoding='utf-8'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

class WallpaperChanger:
    def __init__(self):
        self.download_dir = Path("wallpapers")
        self.download_dir.mkdir(exist_ok=True)
        
        # Windows API常量
        self.SPI_SETDESKWALLPAPER = 0x0014
        self.SPIF_UPDATEINIFILE = 0x01
        self.SPIF_SENDCHANGE = 0x02
        
        # NASA API配置
        self.nasa_api_key = "DEMO_KEY"  # 可以替换为你的NASA API key
        
    def download_image(self, url, filename):
        """下载图片到本地"""
        try:
            logger.info(f"正在下载图片: {url}")
            response = requests.get(url, timeout=30)
            response.raise_for_status()
            
            file_path = self.download_dir / filename
            with open(file_path, 'wb') as f:
                f.write(response.content)
            
            logger.info(f"图片已保存到: {file_path}")
            return str(file_path)
        except Exception as e:
            logger.error(f"下载图片失败: {e}")
            return None
    
    def get_nasa_image(self):
        """从NASA API获取每日图片"""
        try:
            # NASA APOD API - 获取今日图片
            url = f"https://api.nasa.gov/planetary/apod?api_key={self.nasa_api_key}"
            response = requests.get(url, timeout=10)
            response.raise_for_status()
            
            data = response.json()
            if data:
                image_url = data.get('hdurl') or data.get('url')
                title = data.get('title', 'nasa_image')
                date = data.get('date', '')
                
                if image_url:
                    # 清理文件名
                    safe_title = "".join(c for c in title if c.isalnum() or c in (' ', '-', '_')).rstrip()
                    filename = f"nasa_{safe_title}_{date}_{datetime.now().strftime('%H%M%S')}.jpg"
                    return self.download_image(image_url, filename)
            
            logger.warning("无法获取NASA图片")
            return None
        except Exception as e:
            logger.error(f"获取NASA图片失败: {e}")
            return None
    
    def get_random_nasa_image(self):
        """从NASA API获取随机历史图片"""
        try:
            # 获取随机日期的NASA图片
            # 从2020年开始到现在的随机日期
            start_date = datetime(2020, 1, 1)
            end_date = datetime.now()
            random_date = start_date + (end_date - start_date) * random.random()
            date_str = random_date.strftime('%Y-%m-%d')
            
            url = f"https://api.nasa.gov/planetary/apod?api_key={self.nasa_api_key}&date={date_str}"
            response = requests.get(url, timeout=10)
            response.raise_for_status()
            
            data = response.json()
            if data and data.get('media_type') == 'image':
                image_url = data.get('hdurl') or data.get('url')
                title = data.get('title', 'nasa_image')
                
                if image_url:
                    # 清理文件名
                    safe_title = "".join(c for c in title if c.isalnum() or c in (' ', '-', '_')).rstrip()
                    filename = f"nasa_random_{safe_title}_{date_str}_{datetime.now().strftime('%H%M%S')}.jpg"
                    return self.download_image(image_url, filename)
            
            logger.warning("无法获取随机NASA图片")
            return None
        except Exception as e:
            logger.error(f"获取随机NASA图片失败: {e}")
            return None
    
    def set_wallpaper(self, image_path):
        """设置Windows壁纸"""
        try:
            # 确保路径是绝对路径
            abs_path = os.path.abspath(image_path)
            
            # 使用Windows API设置壁纸
            result = ctypes.windll.user32.SystemParametersInfoW(
                self.SPI_SETDESKWALLPAPER,
                0,
                abs_path,
                self.SPIF_UPDATEINIFILE | self.SPIF_SENDCHANGE
            )
            
            if result:
                logger.info(f"壁纸设置成功: {abs_path}")
                return True
            else:
                logger.error("设置壁纸失败")
                return False
        except Exception as e:
            logger.error(f"设置壁纸时出错: {e}")
            return False
    
    def cleanup_old_images(self, keep_count=5):
        """清理旧图片，只保留最新的几张"""
        try:
            image_files = list(self.download_dir.glob("*.jpg")) + list(self.download_dir.glob("*.png"))
            if len(image_files) > keep_count:
                # 按修改时间排序
                image_files.sort(key=lambda x: x.stat().st_mtime, reverse=True)
                
                # 删除旧文件
                for old_file in image_files[keep_count:]:
                    try:
                        old_file.unlink()
                        logger.info(f"已删除旧文件: {old_file}")
                    except Exception as e:
                        logger.warning(f"删除文件失败 {old_file}: {e}")
        except Exception as e:
            logger.error(f"清理旧文件时出错: {e}")
    
    def change_wallpaper(self, mode="today"):
        """更换壁纸的主函数"""
        logger.info("开始更换NASA壁纸...")
        
        image_path = None
        
        if mode == "random":
            logger.info("获取随机NASA图片...")
            image_path = self.get_random_nasa_image()
        else:
            logger.info("获取今日NASA图片...")
            image_path = self.get_nasa_image()
        
        if image_path:
            # 设置壁纸
            if self.set_wallpaper(image_path):
                logger.info("NASA壁纸更换成功！")
                # 清理旧文件
                self.cleanup_old_images()
                return True
            else:
                logger.error("壁纸设置失败")
                return False
        else:
            logger.error("无法获取NASA图片")
            return False

def main():
    """主函数"""
    print("=== NASA自动壁纸更换程序 ===")
    print("使用NASA天文图片数据库的每日精选图片")
    print()
    
    changer = WallpaperChanger()
    
    # 检查命令行参数
    if len(sys.argv) > 1:
        mode = sys.argv[1].lower()
        if mode not in ["today", "random"]:
            print("用法: python run.py [today|random]")
            print("  today: 获取今日NASA图片（默认）")
            print("  random: 获取随机历史NASA图片")
            return
    else:
        mode = "today"
    
    print(f"模式: {mode}")
    print("正在获取NASA图片...")
    
    success = changer.change_wallpaper(mode)
    
    if success:
        print("✅ NASA壁纸更换成功！")
    else:
        print("❌ 壁纸更换失败，请查看日志文件获取详细信息")
        sys.exit(1)

if __name__ == "__main__":
    main()
