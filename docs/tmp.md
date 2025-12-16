---
layout: default
title: 临时未分类
nav_exclude: true
# permalink: /404
---

# 临时未分类
{: .no_toc }

<details open markdown="block">
  <summary>
    Table of contents
  </summary>
  {: .text-delta }
1. TOC
{:toc}
</details>

macOS:

nohup sh -c 'ping --apple-time -i 5 www.baidu.com >> ping_baidu.log 2>&1' > /dev/null 2>&1 &

Ubuntu:

nohup sh -c 'ping -D -i 60 172.18.144.18 >> ping18.log 2>&1' > /dev/null 2>&1 &

tail -f ping18.log