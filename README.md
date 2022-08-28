# of_cmake_config
[中文](README.md) | [英文](README.en.md)

#### 介绍
本项目用于生成OpenFOAM项目的CMakeLists.txt

#### 安装教程
0. 激活OpenFOAM环境: 
    - 使用别名 `of2012clang` or `of2012clangdebug`
    - 直接source: `source $HOME/OpenFOAM/OpenFOAM-v2012/etc/bashrc WM_COMPILER=Clang ...`
1. 获取该项目源码：`git clone https://gitee.com/xfygogo/of_cmake_config.git of_cmake_config`
2. 安装：`cd of_cmake_config && ./install`

#### 使用说明

0. 激活OpenFOAM环境
1. 在项目根目录下, 
    - 运行 `ofCmakeConfig`，生成`CMakeLists.txt`
    - 或运行`occ`，其包装了`ofCmakeConfig`，除了生成`CMakeLists.txt`，还会调用cmake，生成`compile_commands.json`。


#### 测试环境
- `vscode` + `clangd`
- `vim` + `coc-clangd`

[视频演示](demo/occ_demo.mp4)
