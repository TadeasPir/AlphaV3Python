-- Vytvoření databáze pro P2P bankovní systém
CREATE DATABASE IF NOT EXISTS p2p_bank;
USE p2p_bank;

-- Tabulka pro bankovní účty
CREATE TABLE IF NOT EXISTS accounts (
  account_number INT NOT NULL AUTO_INCREMENT,   -- will auto-generate value
  bank_code      VARCHAR(15) NOT NULL,
  balance        BIGINT UNSIGNED NOT NULL DEFAULT 0,
  created_at     TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  updated_at     TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (account_number)
) AUTO_INCREMENT = 10000;




