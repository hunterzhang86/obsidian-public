import os
import shutil
from pypinyin import lazy_pinyin
import argparse
import re
import subprocess


# 获取指定目录下的文件列表
def get_files(path):
    files = []
    for file in os.listdir(path):
        if os.path.isfile(os.path.join(path, file)):
            files.append(file)
    return files


# 获取指定目录下的文件列表
def get_files_recursively(path):
    files = []
    for file in os.listdir(path):
        full_path = os.path.join(path, file)
        if os.path.isfile(full_path):
            files.append(full_path)
        elif os.path.isdir(full_path):
            files += get_files(full_path)
    return files


# 根据文件名字匹配获取文件
def get_file_by_name(name, files):
    matched_files = []
    for file in files:
        if name in file:
            matched_files.append(file)
    return matched_files


# 拷贝文件到指定目录
def copy_file(src_path, dst_path):
    shutil.copy(src_path, dst_path)


# 获取指定目录下的文件列表，并让用户选择文件
def choose_file(path, keyword):
    files = get_files(path)
    matching_files = []
    for file in files:
        if keyword in file:
            matching_files.append(file)
    if len(matching_files) == 0:
        print(f"No files found in the directory matching the keyword '{keyword}'.")
        return None
    elif len(matching_files) == 1:
        return matching_files[0]
    else:
        print(
            f"Multiple files found in the directory matching the keyword '{keyword}':"
        )
        for i, file in enumerate(matching_files):
            print(f"{i+1}. {file}")
        choice = int(input("Please choose a file: "))
        return matching_files[choice - 1]


def find_and_copy_files(
    md_file_path, link_relative_path, search_directory, target_directory
):
    # 读取 Markdown 文件
    with open(md_file_path, "r") as file:
        content = file.read()

    # 查找所有匹配的文件名
    filenames = re.findall(r"!\[\[(.*?)\]\]", content)

    # 在目标目录中创建与 Markdown 文件同名的目录
    md_filename = os.path.basename(md_file_path)
    md_name_without_ext = os.path.splitext(md_filename)[0]
    target_subdirectory = os.path.join(target_directory, md_name_without_ext)

    if not os.path.exists(target_subdirectory):
        os.makedirs(target_subdirectory)

    # 递归搜索文件并拷贝
    for root, dirs, files in os.walk(search_directory):
        for filename in filenames:
            if filename in files:
                source_path = os.path.join(root, filename)
                new_file_name = format_filename(filename, maxlen=50)
                target_path = os.path.join(target_subdirectory, new_file_name)
                shutil.copy2(source_path, target_path)
                print(f"Copied: {source_path} to {target_path}")

                # 替换 Markdown 文件中的链接
                relative_path = os.path.join(
                    link_relative_path, md_name_without_ext, new_file_name
                )
                content = content.replace(f"![[{filename}]]", f"![]({relative_path})")

    # 更新 Markdown 文件
    with open(md_file_path, "w") as file:
        file.write(content)


def format_filename(filename, ext=None, maxlen=20):
    # 将文件名（不包括扩展名）转换为拼音，并在每个拼音之间加上短横线
    name_without_ext = os.path.splitext(filename)[0]
    if ext is None:
        ext = os.path.splitext(filename)[1]

    pinyin_name = "-".join(lazy_pinyin(name_without_ext))

    # 删除所有非字母、数字和短横线的字符
    pinyin_name = re.sub(r"[^a-zA-Z0-9-]", "", pinyin_name)

    # 替换多个连续的短横线为单个短横线
    pinyin_name = re.sub(r"-+", "-", pinyin_name)

    # 限制长度至多为20个字符
    if len(pinyin_name) > maxlen:
        pinyin_name = pinyin_name[:maxlen].rstrip("-")  # 去除尾部可能出现的短横线

    # 转换为小写并添加原始扩展名
    new_filename = pinyin_name.lower() + ext

    return new_filename


def commit_and_push_changes(repo_path, commit_message):
    # 切换到仓库目录
    os.chdir(repo_path)

    # 添加所有新文件
    subprocess.run(["git", "add", "-A"])

    # 提交更改
    subprocess.run(["git", "commit", "-m", commit_message])

    # 推送更改到远程仓库
    subprocess.run(["git", "push"])


# 主函数
def main():
    # 获取基础目录和相对目录
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-src_base_path",
        type=str,
        help="path to source base directory",
        default="/Users/zhanghuan/Library/Mobile Documents/iCloud~md~obsidian/Documents/个人笔记/",
    )
    parser.add_argument(
        "-src_rel_path",
        type=str,
        help="relative path to source directory",
        default="通用能力/知识分享/Backend",
    )
    parser.add_argument(
        "-dst_base_path",
        type=str,
        help="path to destination base directory",
        default="/Users/zhanghuan/VscodeProjects/ifb-blog/",
    )
    parser.add_argument(
        "-dst_md_rel_path",
        type=str,
        help="md relative path to destination directory",
        default="data/blog/ai",
    )
    parser.add_argument(
        "-dst_img_rel_path",
        type=str,
        help="img relative path to destination directory",
        default="public/static/images",
    )
    parser.add_argument(
        "-link_relative_path",
        type=str,
        help="link relative path in md",
        default="/static/images/",
    )
    parser.add_argument(
        "-auto_commit",
        type=str,
        help="whether auto commit",
        default=False,
    )

    parser.add_argument("-search_file", type=str, help="search filename", default="")
    args = parser.parse_args()

    src_base_path = args.src_base_path
    src_rel_path = args.src_rel_path
    dst_base_path = args.dst_base_path
    dst_md_rel_path = args.dst_md_rel_path
    dst_img_rel_path = args.dst_img_rel_path
    link_relative_path = args.link_relative_path
    auto_commit = args.auto_commit
    search_file = args.search_file

    src_path = os.path.join(src_base_path, src_rel_path)

    # 获取文件名字并拷贝文件到指定目录
    filename = choose_file(src_path, search_file)
    if filename is not None:
        # 将文件名字转换为小写字母拼接，如果是中文则使用拼音代替
        new_filename = format_filename(filename, ext=".mdx")
        copy_file(
            os.path.join(src_path, filename),
            os.path.join(dst_base_path, dst_md_rel_path, new_filename),
        )
        find_and_copy_files(
            os.path.join(dst_base_path, dst_md_rel_path, new_filename),
            link_relative_path,
            src_base_path,
            os.path.join(dst_base_path, dst_img_rel_path),
        )
    if auto_commit:
        commit_and_push_changes(dst_base_path, "".join(filename))

if __name__ == "__main__":
    main()
