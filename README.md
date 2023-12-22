## 介绍
该脚本用于将 Obsidian 的笔记发布到基于 Hugo 或者 [Tailwind Nextjs Starter Blog](https://github.com/timlrx/tailwind-nextjs-starter-blog) 的博客，博客需要通过类似 Vercel 之类的平台部署，在我们将 Markdown 文件和图片资源同步到 GitHub 以后，平台会自动构建部署。所以这个脚本实现的功能是将 Obsidian 的笔记同步到 GitHub。

我自己的个人博客 [Innovation for Bytes](https://www.ifb.me/) 也是基于 Tailwind Nextjs Starter Blog 二次开发的博客，部署在 Vercel 平台，域名使用的是 CloudFlare，通过这个脚本实现了一键将我的本地 Obsidian 笔记发布到博客，大大提高了我的码字效率。

## 特点
- 将文件从 Obsidian 源目录复制到博客本地 Git 目录
- 将文件名统一转换为小写形式，并用拼音表示中文字符
- 将 Obsidian 原来图片的引用方式修改为标准 Markdown 的图片引用，并拷贝相关图片到博客图片资源目录

## 要求
- Python 3.x
- pypinyin库

## 使用方法
1. 打开一个终端或命令提示符。
2. cd 到包含 app.py 脚本的目录。
3. 执行以下命令来运行脚本：
```python
python app.py [参数]
```

4. 参数：
   - `-src_base_path`：源基目录的路径。默认值为'/Users/zhanghuan/Library/Mobile Documents/iCloud~md~obsidian/Documents/个人笔记/'。
   - `-src_rel_path`：源目录的相对路径。默认值为'通用能力/知识分享/Backend'。
   - `-dst_base_path`：目标基目录的路径。默认值为/Users/zhanghuan/VscodeProjects/ifb-blog/'。
   - `-dst_md_rel_path`：目标Markdown目录的相对路径。默认值为'data/blog/ai'。
   - `-dst_img_rel_path`：目标图像目录的相对路径。默认值为'public/static/images'。
   - `-link_relative_path`：Markdown中链接图像的相对路径。默认值为'/static/images/'。
   - `-auto_commit`：是否自动提交更改。默认值为False。
   - `-search_file`：要复制的文件的文件名。
## 示例
- 将特定文件复制到目标目录并自动提交更改：
```python
python app.py -dst_md_rel_path='data/blog/ai' -search_file='Obsidian + ChatGPT + Excalidraw：打造高效学习与知识沉淀系统' -auto_commit=True
```
