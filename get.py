import os
import requests

# 请求的URL
url = "https://alist.worldhim.eu.org/api/fs/list"

# 获取文件夹内容的函数
def home(path):
    payload = {
        "path": path,  # 动态设置每个人的目录路径
        "password": "",
        "page": 1,
        "per_page": 0,
        "refresh": False
    }

    # 发送POST请求
    try:
        response = requests.post(url, json=payload)
        response.raise_for_status()  # 检查响应是否成功
        return response.json()  # 返回响应的JSON数据
    except requests.exceptions.RequestException as e:
        print(f"获取路径 {path} 的数据失败: {e}")
        return None

# 创建对应的文件夹
def create_folders(base_directory, dir_names):
    # 确保目标目录存在，如果不存在则创建
    if not os.path.exists(base_directory):
        os.makedirs(base_directory)

    # 遍历列表并为每个人创建文件夹
    for name in dir_names:
        folder_path = os.path.join(base_directory, name)
        try:
            # 创建文件夹
            os.makedirs(folder_path, exist_ok=True)
            print(f"文件夹 '{name}' 创建成功: {folder_path}")
        except OSError as e:
            print(f"创建文件夹 '{name}' 失败: {e}")

# 下载并保存文件的函数
def download_file(file_url, save_path):
    try:
        # 下载文件
        response = requests.get(file_url)
        response.raise_for_status()  # 检查请求是否成功
        with open(save_path, 'wb') as f:
            f.write(response.content)
        print(f"文件下载成功: {save_path}")
    except Exception as e:
        print(f"下载文件失败: {file_url}, 错误: {e}")

# 获取每个人的链接并下载内容
def get_files(base_directory, dir_names):
    base_url = "https://alist.worldhim.eu.org/d/randpic/"

    for name in dir_names:
        folder_path = os.path.join(base_directory, name)
        link = f"{base_url}{name}"

        # 调用 home() 获取每个目录的内容
        result = home(name)
        if result and "data" in result and "content" in result["data"]:
            # 遍历该目录中的文件并下载
            for item in result["data"]["content"]:
                if not item["is_dir"]:  # 忽略目录，仅处理文件
                    file_url = f"{link}/{item['name']}"  # 构建文件URL
                    save_path = os.path.join(folder_path, item["name"])  # 保存路径
                    download_file(file_url, save_path)
        else:
            print(f"未能获取 {name} 的有效数据，跳过此文件夹。")

# 主程序逻辑
def main():
    # 初始获取根目录的文件夹
    home_response = home("/")
    if home_response:
        dir_names = [item["name"] for item in home_response["data"]["content"] if item["is_dir"]]
        print("将创建文件夹:", dir_names)

        # 创建文件夹
        base_directory = "randpic"
        create_folders(base_directory, dir_names)

        # 获取文件并下载到对应文件夹
        get_files(base_directory, dir_names)

if __name__ == "__main__":
    main()
