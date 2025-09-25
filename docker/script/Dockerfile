# 基於 Debian 輕量級映像檔
FROM python:3.12-bookworm


# 設定環境變數
ENV DEBIAN_FRONTEND=noninteractive
ENV PYTHONUNBUFFERED=1


# 設定使用者和群組
ARG USER=pc
ARG UID=1998
ARG GID=1998


# 安裝必要的套件並配置 MS ODBC 驅動程式
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    build-essential \
    unixodbc \
    unixodbc-dev \
    curl \
    gnupg \
    apt-transport-https \
    telnet \
    \
    # 加入 Microsoft apt 密鑰
    && curl -fsSL https://packages.microsoft.com/keys/microsoft.asc | gpg --dearmor -o /usr/share/keyrings/microsoft-prod.gpg \
    && echo "deb [arch=amd64 signed-by=/usr/share/keyrings/microsoft-prod.gpg] https://packages.microsoft.com/debian/12/prod bookworm main" > /etc/apt/sources.list.d/mssql-release.list \
    \
    && apt-get update \
    && ACCEPT_EULA=Y apt-get install -y msodbcsql18 \
    \
    # 創建使用者和群組
    && groupadd -g $GID $USER \
    && useradd -s /bin/bash -u $UID -g $GID -m $USER \
    && mkdir -p /builds/app \
    && chown -R $UID:$GID /builds \
    \
    # 清理 apt 快取以減少映像檔大小
    && apt-get autoremove -y \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*


COPY app /builds/app/
USER $USER
WORKDIR /builds/app


RUN pip install --no-cache-dir --upgrade -r /builds/app/requirements.txt \
    && rm -f /builds/app/requirements.txt


ENTRYPOINT ["python", "Entry.py"]