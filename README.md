<a href='https://github.com/Junwu0615/Forex-Get-Quotes'><img alt='GitHub Views' src='https://views.whatilearened.today/views/github/Junwu0615/Forex-Get-Quotes.svg'> 
<a href='https://github.com/Junwu0615/Forex-Get-Quotes'><img alt='GitHub Clones' src='https://img.shields.io/badge/dynamic/json?color=success&label=Clone&query=count_total&url=https://gist.githubusercontent.com/Junwu0615/4bb80a5b6974941fbee54b711ec077bc/raw/Forex-Get-Quotes_clone.json&logo=github'> <br>
[![](https://img.shields.io/badge/Project-Automated_Scheduler-blue.svg?style=plastic)](https://github.com/Junwu0615/Forex-Get-Quotes) 
[![](https://img.shields.io/badge/Project-Docker-blue.svg?style=plastic)](https://github.com/Junwu0615/Forex-Get-Quotes) 
[![](https://img.shields.io/badge/Language-Python_3.12.0-blue.svg?style=plastic)](https://www.python.org/) 
[![](https://img.shields.io/badge/Operating_System-Windows_10-blue.svg?style=plastic)](https://www.microsoft.com/zh-tw/software-download/windows10) <br>
[![](https://img.shields.io/badge/Package-developer_0.1.0-green.svg?style=plastic)](https://github.com/Junwu0615/Database-Template)

<br>

## *A.　Update Plan*
| 事件 | 敘述 | 更新時間 |
|:--:|--|:--:|
| 專案上架 | Forex-Get-Quotes | 2024-09-12 |
| 加入排程邏輯 | 自動化抓取數據 | 2024-09-12 |
| 與 Database 串接 | 用 [Database-Template](https://github.com/Junwu0615/Database-Template) 完成該功能 | 2024-12-29 |
| Docker | 包裝成服務 | 2025-01-24 |
| 更新 README 說明 | Docker & Database 連線問題 | 2025-01-24 |
| 更新撰寫方式 | - | 2025-09-25 |
| 更新專案路徑編排 | - | 2025-09-25 |

<br>

## *B.　How To Use*

### *STEP.1　Clone*
```py
git clone https://github.com/Junwu0615/Forex-Get-Quotes.git
```

### *STEP.2　Requirements*
```py
pip install -r requirements.txt
```

### *STEP.3　Notice*
- #### *記得填寫 .env 或是在 IDE 設定參數 # 可參考下面的描述*
- #### *有引用 [Database-Template](https://github.com/Junwu0615/Database-Template) 功能完成餵入 Database 的動作*

### *STEP.4　Run*
```py
python Entry.py
```
![00.gif](/sample/00.gif)

![00.jpg](/sample/00.jpg)

![01.jpg](/sample/01.jpg)

<br>

## *C.　Dockerization*

### *Directory Structure Diagram*
```commandline
Forex-Get-Quotes/docker
  ├── app
  │   ├── package
  │   │   ├── __init__.py
  │   │   ├── base.py
  │   │   ├── source.py
  │   │   ├── token.py
  │   │   └── token.txt
  │   ├── Entry.py
  │   └── requirements.txt
  └── script
      ├── .env
      ├── docker-compose.yaml
      └── Dockerfile
```

### *STEP.1　進入腳本路徑*
```bash
cd docker
```

### *STEP.2　新增檔案 : `./script/.env`*
```commandline
SQL_SERVER_DRIVER=17
SQL_SERVER_BROKER_HOST=<Your SQL Server IP>,<YOUR SQL Server Port>
SQL_SERVER_LOGIN_USER=<Your User Name>
SQL_SERVER_LOGIN_PASSWORD=<Your User Password>
SCHEDULE_SETTINGS=MTWTFss=22:00:00,MTWTFss=10:00:00 # Linux 時間計算為+0
SAVE_PATH=/builds/rep/datasets
FMP_TOKEN=<Your FMP_TOKEN>
TELEGRAM_BOT_TOKEN=<Your TELEGRAM_BOT_TOKEN>
TELEGRAM_CHAT_ID=<Your TELEGRAM_CHAT_ID>
```

### *STEP.3　安裝 Dockerfile*
```bash
docker build -t forex-get-quotes:latest -f script/Dockerfile . --no-cache
```

### *STEP.4　安裝 docker-compose*
```bash
docker stack deploy -c script/docker-compose.yaml forex-get-quotes
```

### *STEP.5　檢視 docker service 清單*
```bash
docker service ls
```

### *STEP.6　查看專案 log 打印*
```bash
docker service logs -f forex-get-quotes_task
```

![02.jpg](/sample/02.jpg)

<br>


## *D.　Other*
### *新增 SQL 用戶來登入 Database*
- #### *確認使用者是否存在*
  ```sql
  SELECT name FROM sys.server_principals WHERE name='new_user';
  ```
  - #### *若不存在，則新增使用者*
    ```sql
    CREATE LOGIN new_user WITH PASSWORD='YourPassword';
    ```
  - #### *若忘記密碼，可重設使用者密碼*
    ```sql
    ALTER LOGIN new_user WITH PASSWORD='NewPassword';
    ```
- #### *檢查目標資料庫中是否已建立使用者*
  ```sql
  USE [YourDatabase];
  SELECT name FROM sys.database_principals WHERE name = 'new_user';
  ```
  - #### *若不存在，則建立資料庫使用者並關聯登入*
    ```sql
    CREATE USER new_user FOR LOGIN new_user;
    -- 賦予管理權限
    ALTER ROLE db_owner ADD MEMBER new_user; 
    ```
- #### *SQL Server 身份驗證模式設定與調整，變更驗證模式*
  - #### *變更登入驗證模式*
    ```commandline
    regedit
    ```
    - 瀏覽至該路徑: `HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Microsoft SQL Server\MSSQL{InstanceID}.MSSQLSERVER\LoginMode`
    - 改變 LoginMode 數值
      - 1 = 僅允許 Windows 身份驗證
      - 2 = 啟用混合模式 (SQL Server 和 Windows 身份驗證)
    - 儲存更改，然後重新啟動 SQL Server 服務
  - #### *SQL 查詢指令確認有無生效*
    ```sql
    -- 0：混合模式
    -- 1: 僅 Windows 身份驗證
    SELECT SERVERPROPERTY('IsIntegratedSecurityOnly') AS AuthenticationMode;
    ```

<br>

### *刪除欲移除的 SQL 用戶*
- #### *確認使用者的 ~~`principal_id`~~ & 類型*
  ```sql
  SELECT name, principal_id, type_desc FROM sys.database_principals
  SELECT name, principal_id, type_desc FROM sys.server_principals
  ```
- #### ~~*確認使用者的 綁定的角色 ID*~~
  ```sql
  SELECT * FROM sys.database_role_members WHERE member_principal_id=<principal_id> 
  ```
- #### *刪除使用者 (依使用者類型決定以什麼方式刪除)*
  ```sql
  DROP USER <user_name>
  DROP LOGIN <user_name>
  ```
  
<br>

### *測試是否有以 IP 形式連接上 Database*
- #### *進入 container 輸入指令*
  ```bash
  docker exec -it <container id> bash
  ```
- #### *開啟 SQL Server TCP/IP 協議*
  ```commandline
  Win + R : compmgmt.msc
  ```
- #### *確認是否有連接上 Database*
  - #### *telnet 測試*
    ```bash
    telnet <SQL Server IP> <port>
    ```
  - #### *Docker container 進去 bash 測試*
    ```bash
    # 確認是否能連接該位置
    telnet <SQL Server IP> <port>
    ```
    ```bash
    # 確認是否能以該使用者登入資料庫，成功後可下指令測試
    sqlcmd -S <SQL Server IP>,<port> -U <user> -P <password> -d <database>
    ```

<br>

### *其他指令*
- #### *確認實體連線設定等狀態*
  ```sql
  EXEC sp_helpserver
  ```
- #### *SQL 版本確認*
  ```sql
  SELECT @@VERSION;
  ```
- #### *查閱資料庫允許通過的連線設定*
  ```sql
  EXEC xp_readerrorlog 0, 1, N'server is listening';
  ```

<br>

### *Notice:　About SPN*
- #### *btw，這玩意兒讓我瘋狂鬼打牆，卡了近 4 天*
- #### *法 1.　直接設定 NTLM，繞過 SPN*
  ```commandline
  regedit
  ```
  - 瀏覽至該路徑: `HKEY_LOCAL_MACHINE\SYSTEM\CurrentControlSet\Control\Lsa`
  - 新增 DWORD 32 位元 `DisableLoopbackCheck`，數值設置 1
- #### *法 2.　設定 SPN ( 我沒成功，未來有機會再搞 )*
  ```commandline
  setspn -L <服務帳戶>
  # 預期出現
  MSSQLSvc/<服務帳戶>:<port>
  MSSQLSvc/<服務帳戶>.domain.local:<port>
  ```
  - #### 若無則手動新增
  ```commandline
  setspn -A MSSQLSvc/<SQL Server IP>:<port> <服務帳戶>$
  setspn -A MSSQLSvc/<服務帳戶>.domain.local:<port> <服務帳戶>$
  ```
- #### *重啟 SQL server 服務，確認 IP 形式是否能正常連上 Database*

<br>

## *E.　Data & Reference Sources*
- #### [Financial Modeling Prep](https://financialmodelingprep.com/developer/docs/)
- #### [找不到 SQL Server 配置管理器](https://blog.csdn.net/czjnoe/article/details/136991382)
- #### [SQL Server TCP/IP 设置](https://blog.csdn.net/kfepiza/article/details/131266987)
- #### [輸入防火牆設置](https://blog.csdn.net/zgscwxd/article/details/131553890)
- #### [SQL 服務無法正常啟用，可以試著輸入: netsh winsock reset](https://blog.csdn.net/qq_23082219/article/details/125576935)