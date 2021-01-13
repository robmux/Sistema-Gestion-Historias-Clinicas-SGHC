-- CREATE DATABASE sghc OWNER postgres TABLESPACE sghcspace;

SELECT 'CREATE DATABASE sghc'
WHERE NOT EXISTS (SELECT FROM pg_database WHERE datname = 'sghc')\gexec