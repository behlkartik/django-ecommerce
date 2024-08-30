CREATE DATABASE restaurant_app;
CREATE USER restaurant_app_user WITH PASSWORD 'postgres';
ALTER ROLE restaurant_app_user SET client_encoding TO 'utf8';
ALTER ROLE restaurant_app_user SET default_transaction_isolation TO 'read committed';
ALTER ROLE restaurant_app_user SET timezone TO 'UTC';
GRANT ALL PRIVILEGES ON DATABASE restaurant_app TO restaurant_app_user;