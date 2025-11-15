# MySQL8系のイメージを指定
FROM mysql:8.0

# MySQLのローカルの設定ファイルをコンテナにコピー
COPY Docker/MySQL/custom.cnf /etc/mysql/conf.d/custom.cnf
RUN chmod 644 /etc/mysql/conf.d/custom.cnf

# init.sqlをコンテナの/docker-entrypoint-init.db.dと共有
COPY Docker/MySQL/init.sql /docker-entrypoint-initdb.d