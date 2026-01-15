
-- Create Table for Licenses
CREATE TABLE IF NOT EXISTS licenses (
    key VARCHAR(255) PRIMARY KEY,
    email VARCHAR(255),
    hwid VARCHAR(255),
    status VARCHAR(50) DEFAULT 'active', -- 'active', 'banned'
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    last_check TIMESTAMP WITH TIME ZONE
);

-- Example Insert (Run this in Supabase SQL Editor)
-- INSERT INTO licenses (key, email, status) VALUES ('SKLUM-TEST-KEY-123', 'admin@example.com', 'active');
