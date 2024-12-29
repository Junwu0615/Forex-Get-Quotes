<a href='https://github.com/Junwu0615/Forex-Get-Quotes'><img alt='GitHub Views' src='https://views.whatilearened.today/views/github/Junwu0615/Forex-Get-Quotes.svg'> 
<a href='https://github.com/Junwu0615/Forex-Get-Quotes'><img alt='GitHub Clones' src='https://img.shields.io/badge/dynamic/json?color=success&label=Clone&query=count_total&url=https://gist.githubusercontent.com/Junwu0615/6c605b43f1b9dcb93f9c7b6c1a5103ab/raw/Forex-Get-Quotes_clone.json&logo=github'> </br>
[![](https://img.shields.io/badge/Project-Automated_Scheduler-blue.svg?style=plastic)](https://github.com/Junwu0615/Forex-Get-Quotes) 
[![](https://img.shields.io/badge/Language-Python_3.12.0-blue.svg?style=plastic)](https://www.python.org/) </br>
[![](https://img.shields.io/badge/Package-requests_2.27.1-green.svg?style=plastic)](https://pypi.org/project/requests/) 
[![](https://img.shields.io/badge/Package-schedule_1.2.2-green.svg?style=plastic)](https://pypi.org/project/schedule/) 

### STEP.1　CLONE
```py
git clone https://github.com/Junwu0615/Forex-Get-Quotes.git
```

### STEP.2　INSTALL PACKAGES
```py
pip install -r requirements.txt
```

### STEP.3　NOTICE
- #### 將 package `token_.txt` -> `token.txt` 修改內容
    ```
    LINE,[Fill In Your LINE Token]
    FMP,[Fill In Your FMP Token]
    TELEGRAM,[Fill In Your Bot Token],[Fill In Your Chat Token]
    ```
- #### 有引用 [Database-Template](https://github.com/Junwu0615/Database-Template) 功能完成餵入資料庫的動作
- #### 未來預計將此專案打包成 Docker 服務

### STEP.4　RUN 
```py
python Entry.py
```
![00.gif](/sample/00.gif)

![00.jpg](/sample/00.jpg)

![01.jpg](/sample/01.jpg)

### 數據來源
- #### [Financial Modeling Prep](https://financialmodelingprep.com/developer/docs/)