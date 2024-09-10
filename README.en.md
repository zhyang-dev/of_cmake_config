# of_cmake_config
[中文](README.md) | [English](README.en.md)

#### Description
This project is used to generate CMakeLists.txt for OpenFOAM project.

#### Installation
0. Activate OpenFOAM environment: 
    - Using alias `of2012clang` or `of2012clangdebug`
    - source directly: `source $HOME/OpenFOAM/OpenFOAM-v2012/etc/bashrc WM_COMPILER=Clang ...`
1. Get this project: `git clone https://gitee.com/xfygogo/of_cmake_config.git of_cmake_config`
2. Install: `cd of_cmake_config && ./install`

#### Instructions

1.  Activate OpenFOAM environment
2.  In project root path, 
    - run `ofCmakeConfig` to generate `CMakeLists.txt`
    - or run `occ`, which is a wrapper of `ofCmakeConfig` script, to generate `CMakeLists.txt` and `compile_commands.json`.

[video demo](demo/occ_demo.gif)