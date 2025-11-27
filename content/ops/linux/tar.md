---
title: "Tar"
date: 2025-11-27T11:02:37+08:00
draft: false
categories:
    - 运维
tags:
    - command
---

# tar 命令使用

### tar

```
基本选项：
-c：创建新的打包文件。
-x：从打包文件中提取文件。
-v：显示详细的操作过程。
-f：指定打包文件的名称。
压缩选项：
-z：使用gzip压缩算法对打包文件进行压缩/解压缩（通常使用.tar.gz扩展名）。
-j：使用bzip2压缩算法对打包文件进行压缩/解压缩（通常使用.tar.bz2扩展名）。
目录选项：
-C <目录>：在指定目录下执行打包或解压操作。
-P：保留绝对路径，完整地保存文件路径信息。
过滤选项：
--exclude <模式>：排除符合指定模式的文件或目录。
--include <模式>：仅包括符合指定模式的文件或目录。
其他选项：
-t：列出打包文件中的内容。
-r：将文件追加到已有的打包文件中。
-u：仅将比打包文件中相应文件更新的文件追加到已有的打包文件中。
--wildcards：支持使用通配符模式匹配文件。
```

### 打包

```
tar -cvf archive.tar file1 file2 ...          # 打包文件
tar -czvf archive.tar.gz file1 file2 ...      # 打包并压缩为gzip格式
tar -cjvf archive.tar.bz2 file1 file2 ...     # 打包并压缩为bzip2格式
#.tar 、tar.gz 、tar.bz2 区别：
#.tar 常见的打包格式，但是不进行压缩 .tar文件只是将文件和目录组织到一个归档中，保留了原始文件的权限、时间戳和目录结构。
#tar.gz 先打包成tar包，再进行.gz压缩。既保留了打包文件的目录结构，又对其进行了压缩。
#tar.bz2 与tar.gz不同的是用了.bz2 压缩
```

### 解压打包文件

```
tar -xvf archive.tar                         # 解压tar文件
tar -xzvf archive.tar.gz                      # 解压gzip压缩的tar文件
tar -xjvf archive.tar.bz2                     # 解压bzip2压缩的tar文件
```

### 查看打包文件内容

```
tar -tvf archive.tar                          # 列出tar文件中的内容
tar -tzvf archive.tar.gz                       # 列出gzip压缩的tar文件中的内容
tar -tjvf archive.tar.bz2                      # 列出bzip2压缩的tar文件中的内容
```

### 追加文件到已有打包文件

```
tar -rvf archive.tar file3 file4 ...          # 追加文件到tar文件
tar -rzvf archive.tar.gz file3 file4 ...      # 追加文件到gzip压缩的tar文件
tar -rjvf archive.tar.bz2 file3 file4 ...     # 追加文件到bzip2压缩的tar文件
```