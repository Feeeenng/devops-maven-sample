# Windows 容器化

Windows 框架分为 `.net core ` 跟 `.net Framework`, core 可以运行在 Liunx 环境下, 而 Framework 只能运行在 windows 环境


# .net Core容器化

core 容器化是可以通过 Liunx 环境进行构建并且运行在 Liunx 环境上的应用

## 构建环境镜像


构建环境镜像通常都是包含 .net core sdk相关镜像, 譬如 

-  mcr.microsoft.com/dotnet/sdk:5.0
-  mcr.microsoft.com/dotnet/sdk:6.0

官方地址：https://mcr.microsoft.com/product/dotnet/sdk/about
