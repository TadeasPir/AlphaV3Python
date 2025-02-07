
# P2P Banking System

## Overview

This project implements a simple P2P banking system using Python. It includes a TCP server that listens for client connections and processes banking-related commands. The system supports account creation, deposit, withdrawal, balance inquiry, and account removal. It also provides basic bank information and logging capabilities.

## File Structure

```
.
├── config
│   ├── config.py
│   └── config.yaml
├── src
│   ├── commands
│   │   └── accountManager.py
│   ├── database
│   │   └── database.py
│   └── server.py
└── main.py
├── utils
│   
└── README.md
```

*   `config/config.py`: Defines the `Config` class for loading configuration settings from the `config.yaml` file.
*   `config/config.yaml`: YAML file containing configuration parameters for the application, such as database credentials, server IP, port, and logging settings.
*   `src/commands/accountManager.py`: Implements the `AccountManager` class, which handles database interactions for managing bank accounts.
*   `src/database/database.py`: Defines the `Database` class for managing the MySQL database connection.
*   `src/server.py`: Contains the `TCPServer` class, which handles client connections, receives commands, and processes them using the `AccountManager`.
*   `src/main.py`: The main entry point of the application, responsible for initializing the server and starting the main event loop.
*   `utils/logging_config.py`: Provides the `setup_logging` function for configuring the application's logging.
*   `README.md`: Provides an overview of the project.

## Configuration

The application uses a `config.yaml` file to store configuration settings. Here's an example of the configuration file:

```yaml
bank:
  ip: "10.147.18.126"
  port: "65525"
  timeout: "5"

db:
  host: "localhost"
  user: "root"
  password: ""
  database: "p2p_bank"

logging:
  level: "INFO"
  file: "app.log"
```

*   `bank`: Contains settings related to the TCP server, such as the IP address, port, and client timeout.
*   `db`: Contains database connection settings, such as the host, user, password, and database name.
*   `logging`: Configures the logging level and file path.

## Dependencies

The project uses the following Python libraries:

*   `logging`: For logging application events.
*   `re`: For regular expressions, used in input validation.
*   `socket`: For network communication.
*   `datetime`: For handling date and time.
*   `multiprocessing`: For handling multiple client connections concurrently.
*   `typing`: For type hinting.
*   `mysql.connector`: For connecting to the MySQL database.
*   `yaml`: For parsing the YAML configuration file.

You can install the dependencies using pip:

```bash
pip install mysql-connector-python pyyaml
```

## Setup

1.  **Clone the repository:**

    ```bash
    git clone [repository_url]
    cd [repository_directory]
    ```

2.  **Install dependencies:**

    ```bash
    pip install mysql-connector-python pyyaml
    ```

3.  **Configure the database:**

    *   Create a MySQL database named `p2p_bank`.
    *   Update the database credentials in `config/config.yaml`.
    *   Run the SQL script to create the `accounts` table:

        ```sql
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
        ```

4.  **Configure the server:**

    *   Update the server IP and port in `config/config.yaml`.

## Running the Server

To start the server, execute the `src/main.py` script:

```bash
python src/main.py
```

The server will listen for incoming connections on the configured IP address and port.

## Usage

Once the server is running, clients can connect to it and send commands to perform banking operations. The following commands are supported:

*   `DATE`: Returns the current date and time.
*   `HELP`: Returns a list of available commands.
*   `BC`: Returns the bank code (server IP).
*   `AC`: Creates a new account and returns the account number and bank code.
*   `AD account_number/ip_address amount`: Deposits the specified amount into the account.
*   `AW account_number/ip_address amount`: Withdraws the specified amount from the account.
*   `AB account_number/ip_address`: Returns the account balance.
*   `AR account_number/ip_address`: Removes the account.
*   `BA`: Returns the total amount of money in the bank.
*   `BN`: Returns the number of accounts in the bank.

## Logging

The application uses the `logging` module to log events to a file. The logging level and file path can be configured in the `config.yaml` file.

## Error Handling

The application includes error handling to catch exceptions and log error messages. This helps in debugging and maintaining the system.

## Future Enhancements

*   Implement more robust error handling and input validation.
*   Add support for user authentication and authorization.
*   Implement transaction logging and auditing.
*   Add a graphical user interface (GUI) for clients.
*   Implement unit tests to ensure code quality.

## Author

Tadeas Pirich
