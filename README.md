# MindsDB

MindsDB is an open-source machine learning platform that enables developers to build, train, and deploy machine learning models directly within their database environments. This repository contains the MindsDB Knowledge Base Application, which provides various functionalities such as chatting, summarizing, searching, and browsing content with the assistance of AI.

## Setup

### Environment Configuration

To use the MindsDB KB App with OpenAI's API, you need to configure your environment with an API key. Follow these steps:

1. **Locate the Environment File**: An environment file named `.env` has been created in the `mindsdb-kb-app` directory.
2. **Add Your OpenAI API Key**: Open the `.env` file and replace `your_openai_api_key_here` with your actual OpenAI API key. The file should look like this:
   ```
   OPENAI_API_KEY=your_actual_api_key
   ```
3. **Protect Your API Key**: Ensure that the `.env` file is not committed to version control. Add it to your `.gitignore` file if necessary to prevent accidental exposure of your API key.

### Running the Application

**Prerequisite**: Ensure that MindsDB is installed and running on your system. MindsDB must be accessible on `localhost:47334` (default port) for the application to connect successfully. If MindsDB is not running, follow the steps below to start it before proceeding with the application launch. If you encounter connection errors, verify that MindsDB is active and listening on the correct port.

**Starting MindsDB**:
1. **Install MindsDB**: If MindsDB is not installed, you can install it using pip:
   ```
   pip install mindsdb
   ```
   Alternatively, follow the installation instructions on the [MindsDB GitHub page](https://github.com/mindsdb/mindsdb) or [official documentation](https://docs.mindsdb.com/).
2. **Start MindsDB Server**: Open a terminal or command prompt and run the following command to start the MindsDB server:
   ```
   python -m mindsdb
   ```
   This will launch the MindsDB server on the default port `47334`. Ensure the server is running before starting the application. You can verify it's running by checking the terminal output for a confirmation message or by accessing the MindsDB GUI at `http://localhost:47334` in your web browser.
3. **Troubleshooting**: If MindsDB fails to start or is not accessible, check for port conflicts or ensure no other instances are running. You can specify a different port if needed by using the `--api-port` flag, e.g., `python -m mindsdb --api-port 47335`.

- **CLI Application**:
  1. Open a terminal or command prompt.
  2. Navigate to the `mindsdb-kb-app` directory using the command:
     ```
     cd mindsdb-kb-app
     ```
  3. Run the CLI application with:
     ```
     python cli_app.py
     ```
     This will start the command-line interface for interacting with the knowledge base. If you receive a connection error, ensure MindsDB is running as described in the prerequisite.

- **Web Application**:
  1. Open a terminal or command prompt.
  2. Navigate to the `mindsdb-kb-app/app` directory using the command:
     ```
     cd mindsdb-kb-app/app
     ```
  3. Run the web application with:
     ```
     python app.py
     ```
     This will start the server for the graphical user interface. Open a web browser and go to `http://localhost:5000` (or the port specified in the terminal) to access features like chatting, summarizing, searching, and browsing. If you receive a connection error, ensure MindsDB is running as described in the prerequisite.

## Features

- **Chat**: Engage in conversations with AI assistance.
- **Summarize**: Get concise summaries of content.
- **Search**: Find relevant information within the knowledge base.
- **Browse**: Explore various topics and content interactively.

## Contributing

Contributions to MindsDB are welcome! Please read our contributing guidelines for more information on how to get involved.

## License

This project is licensed under the MIT License - see the LICENSE file for details.
