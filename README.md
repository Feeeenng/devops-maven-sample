# Windows 容器化

Windows 框架分为 `.net core ` 跟 `.net Framework`, core 可以运行在 Liunx 环境下, 而 Framework 只能运行在 windows 环境



# 构建环境镜像

.net Core 构建环境镜像通常都是包含相关镜像, 譬如 

-  mcr.microsoft.com/dotnet/sdk:5.0
-  mcr.microsoft.com/dotnet/sdk:6.0

官方地址：https://mcr.microsoft.com/product/dotnet/sdk/about

.net Framework 



# 运行环境镜像

运行环境通常都是以 Dockerfile 形式, 代码最终的运行环境

.net Core

- mcr.microsoft.com/dotnet/aspnet:5.0
- mcr.microsoft.com/dotnet/aspnet:6.0

官方地址：https://mcr.microsoft.com/product/dotnet/aspnet/about

.net Framework

- mcr.microsoft.com/windows/servercore:ltsc2022
- mcr.microsoft.com/windows/servercore:ltsc2019

官方地址：https://mcr.microsoft.com/en-us/product/windows/servercore/about
