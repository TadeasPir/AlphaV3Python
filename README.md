# P2P Banking System

A peer-to-peer banking system enabling basic banking operations via a TCP server. Supports account management, deposits, withdrawals, balance checks, and bank-wide queries.

## Features

- **Account Management**:
  - `AC`: Create a new account.
  - `AR`: Remove an account (if balance is zero).
- **Transactions**:
  - `AD [account]/[ip] [amount]`: Deposit funds.
  - `AW [account]/[ip] [amount]`: Withdraw funds.
- **Queries**:
  - `AB [account]/[ip]`: Check account balance.
  - `BA`: Total balance across all accounts in the bank.
  - `BN`: Total number of accounts in the bank.
- **Utilities**:
  - `DATE`: Get server date and time.
  - `HELP`: List available commands.
  - `BC`: Retrieve the bank code (server IP).

## Installation

1. **Prerequisites**:
   - MySQL Server.
   - Python 3.8+.
   - Required packages:  
     ```bash
     pip install mysql-connector-python PyYAML
     ```

2. **Database Setup**:
   - Run the SQL script to create the database and table:  
     ```bash
     mysql -u [user] -p < Alpha3.sql
     ```

3. **Configuration**:
   - Create `config/config.yaml` with the following structure:  
     ```yaml
     ip: "127.0.0.1"  # Server IP
     port: 12345       # Server port
     client_timeout: 30
     logging_level: "INFO"
     logging_file: "logs/app.log"
     # Database settings
     host: "localhost"
     user: "your_db_user"
     password: "your_db_password"
     database: "p2p_bank"
     ```

## Usage

1. **Start the Server**:
   ```bash
   python main.py
Connect via TCP Client (e.g., telnet):

bash
Copy
telnet 127.0.0.1 12345
Example Commands:

Create account:
AC → Returns AC 10001/127.0.0.1

Deposit 500 units:
AD 10001/127.0.0.1 500 → Returns AD

Check balance:
AB 10001/127.0.0.1 → Returns AB 500

Withdraw 200 units:
AW 10001/127.0.0.1 200 → Returns AW

Database Schema
Table accounts:

Column	Type	Description
account_number	INT	Auto-incremented (starts at 10000)
bank_code	VARCHAR(15)	Bank identifier (server IP)
balance	BIGINT	Stored in cents (e.g., 100 = $1)
created_at	TIMESTAMP	Account creation time
updated_at	TIMESTAMP	Last update time
Logging
Logs are stored in logs/app.log (rotates after 5 MB, keeps 3 backups).

Logging level can be adjusted in config.yaml (DEBUG, INFO, WARNING, ERROR).

Notes
Account Format: [account_number]/[bank_ip] (e.g., 10001/127.0.0.1).

Validation:

Account numbers range: 10000–99999.

Withdrawals fail if amount exceeds balance.

Account deletion requires zero balance.

Assumptions:

Balances are stored as integers (avoid floating-point inaccuracies).

Bank code is the server’s IP address for simplicity.

License
MIT License. See LICENSE for details.
