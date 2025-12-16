---
title: 教具相关软件安装使用
layout: default
parent: 软件使用
nav_order: 10
---

# 教具相关软件安装使用
{: .no_toc }

相关实验箱、开发板的相关软件安装和使用说明。

<details open markdown="block">
  <summary>
    目录
  </summary>
  {: .text-delta }
1. TOC
{:toc}

<hr>

## 安装 VSCode

点击界面左下角的 `九宫格(Show Applications)`，然后搜索 `VSCode`。如能找到则打开直接使用。如没有找到，参考如下步骤安装 VSCode 到开发板。

- 打开开发板上的浏览器，访问 VSCode 官网 Download 页面：[https://code.visualstudio.com/Download](https://code.visualstudio.com/Download)
- 选择下载 `.deb` `Arm64`。通常下载到用户的 HOME 目录的 `Downloads` 子目录中，比如 `/home/jetson/Downloads`。
- 依次执行以下命令，安装 VSCode：

```bash
cd /home/jetson/Downloads # 假定 .deb 安装包下载到 /home/jetson/Downloads 目录中
sudo dpkg -i 下载的.deb安装包文件
```

- 点击界面左下角的 `九宫格(Show Applications)`，然后搜索 `VSCode`，就可以找到该应用。打开应用后，在界面左侧导航栏中找到该应用，鼠标右键选 `Add to Favorites`，以方便下次使用。

<hr>

## 开发板截图

在英伟达开发板上，如需要截图，除了手机拍照，还可使用内置应用 `Screenshot`。点击界面左下角的 `九宫格(Show Applications)`，然后搜索 `Screenshot`，就可以找到该应用。

截图可以通过 `微信文件传输网页版`，或 `scp` 命令等，传到微信或电脑中。此处从略。

在界面左侧导航栏中找到该应用，鼠标右键选 `Add to Favorites`，以方便下次使用。