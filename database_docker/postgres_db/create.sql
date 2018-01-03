CREATE DATABASE metagenscope_prod;
CREATE DATABASE metagenscope_dev;
CREATE DATABASE metagenscope_test;

\c metagenscope_prod;
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";
\c metagenscope_dev;
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";
\c metagenscope_test;
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";
