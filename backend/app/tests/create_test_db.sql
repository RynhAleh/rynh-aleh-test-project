-- Create test database for automated tests
CREATE DATABASE test_db;

-- You can also add test-specific setup here if needed
-- For example, test roles or extensions:
CREATE ROLE test_user WITH LOGIN PASSWORD 'test_password';
GRANT ALL PRIVILEGES ON DATABASE test_db TO test_user;
