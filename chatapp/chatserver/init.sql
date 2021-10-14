CREATE USER django WITH PASSWORD 'mypsqlpass';
CREATE DATABASE chatapp_dev;
GRANT ALL PRIVILEGES ON DATABASE chatapp_dev TO django;
