# MindsDB Knowledge Base Application

MindsDB is an open-source machine learning platform that enables developers to build, train, and deploy machine learning models directly within their database environments. This repository contains the MindsDB Knowledge Base Application, which provides various functionalities such as chatting, summarizing, searching, and browsing content with the assistance of AI.

---

## 📋 Table of Contents

<details>
<summary><strong>🚀 Setup & Installation</strong></summary>

### Environment Configuration

To use the MindsDB KB App with OpenAI's API, you need to configure your environment with an API key. Follow these steps:

1. **Locate the Environment File**: An environment file named `.env` has been created in the `mindsdb-kb-app` directory.
2. **Add Your OpenAI API Key**: Open the `.env` file and replace `your_openai_api_key_here` with your actual OpenAI API key. The file should look like this:
   ```
   OPENAI_API_KEY=your_actual_api_key
   ```
3. **Protect Your API Key**: Ensure that the `.env` file is not committed to version control. Add it to your `.gitignore` file if necessary to prevent accidental exposure of your API key.

### Prerequisites

**Important**: Ensure that MindsDB is installed and running on your system. MindsDB must be accessible on `localhost:47334` (default port) for the application to connect successfully.

#### Starting MindsDB

1. **Install MindsDB**: If MindsDB is not installed, you can install it using pip:
   ```bash
   pip install mindsdb
   ```
   Alternatively, follow the installation instructions on the [MindsDB GitHub page](https://github.com/mindsdb/mindsdb) or [official documentation](https://docs.mindsdb.com/).

2. **Start MindsDB Server**: Open a terminal or command prompt and run the following command to start the MindsDB server:
   ```bash
   python -m mindsdb
   ```
   This will launch the MindsDB server on the default port `47334`. Ensure the server is running before starting the application.

3. **Verify Installation**: You can verify it's running by checking the terminal output for a confirmation message or by accessing the MindsDB GUI at `http://localhost:47334` in your web browser.

4. **Troubleshooting**: If MindsDB fails to start or is not accessible, check for port conflicts or ensure no other instances are running. You can specify a different port if needed:
   ```bash
   python -m mindsdb --api-port 47335
   ```

</details>

<details>
<summary><strong>🖥️ Running the Applications</strong></summary>

### CLI Application

1. Open a terminal or command prompt.
2. Navigate to the `mindsdb-kb-app` directory:
   ```bash
   cd mindsdb-kb-app
   ```
3. Run the CLI application:
   ```bash
   python cli_app.py
   ```
   This will start the command-line interface for interacting with the knowledge base. If you receive a connection error, ensure MindsDB is running as described in the prerequisites.

### Web Application

1. Open a terminal or command prompt.
2. Navigate to the `mindsdb-kb-app/app` directory:
   ```bash
   cd mindsdb-kb-app/app
   ```
3. Run the web application:
   ```bash
   python app.py
   ```
   This will start the server for the graphical user interface. Open a web browser and go to `http://localhost:5000` (or the port specified in the terminal) to access all features.

</details>

<details>
<summary><strong>✨ Features Overview</strong></summary>

- **💬 Chat**: Engage in conversations with AI assistance
- **📝 Summarize**: Get concise summaries of content
- **🔍 Search**: Find relevant information within the knowledge base
- **🗂️ Browse**: Explore various topics and content interactively
- **➕ Add Documents**: Contribute new content to the knowledge base

</details>

<details>
<summary><strong>📖 Application Usage Guide</strong></summary>

### 💬 Chat Feature
<details>
<summary>Click to expand Chat instructions</summary>

- **Purpose**: Interact with an AI assistant to get answers, discuss topics, or troubleshoot issues.
- **How to Use**:
  - **Web App**: Navigate to the "Chat" section from the main menu. Type your message in the input box at the bottom and press "Send". The AI will respond in the chat window.
  - **CLI App**: Select the chat option from the menu and type your queries when prompted. Responses will be displayed in the terminal.
- **Tips**: Be specific with your questions for more accurate responses. Use follow-up messages to dive deeper into a topic.

</details>

### 📝 Summarize Feature
<details>
<summary>Click to expand Summarize instructions</summary>

- **Purpose**: Quickly condense lengthy documents or content into concise summaries.
- **How to Use**:
  - **Web App**: Go to the "Summarize" page. Paste the text or upload a document in the provided field, then click "Summarize". View the summary below.
  - **CLI App**: Choose the summarize option, input your text or specify a file path, and receive a summary directly in the terminal.
- **Tips**: For best results, ensure the input text is clear and structured. Summaries are ideal for reports, articles, or meeting notes.

</details>

### 🔍 Search Feature
<details>
<summary>Click to expand Search instructions</summary>

- **Purpose**: Locate specific information or documents within the knowledge base.
- **How to Use**:
  - **Web App**: Access the "Search" tab. Enter your query in the search bar and hit "Search". Results will display relevant matches with snippets.
  - **CLI App**: Use the search command, type your query, and review the list of matching entries returned.
- **Tips**: Use keywords or phrases for precise results. Refine your search with filters if available in the web interface.

</details>

### 🗂️ Browse Feature
<details>
<summary>Click to expand Browse instructions</summary>

- **Purpose**: Explore the knowledge base by categories, departments, or topics without a specific query.
- **How to Use**:
  - **Web App**: Click on "Browse" in the navigation menu. You'll see a structured list or grid of topics and categories. Click on any to view detailed content.
  - **CLI App**: Select the browse option to view a list of categories. Navigate through them using the provided menu numbers or commands.
- **Tips**: Great for discovering new content or getting an overview of available resources. Bookmark frequently visited categories for quick access.

</details>

### ➕ Adding Documents
<details>
<summary>Click to expand Add Documents instructions</summary>

- **Purpose**: Contribute to the knowledge base by adding new documents or content.
- **How to Use**:
  - **Web App**: Navigate to "Add Document". Fill out the form with the document content, department, and type, then submit.
  - **CLI App**: Currently, adding documents is primarily supported via the web interface for ease of use.
- **Tips**: Ensure documents are categorized correctly for easier retrieval by others. Include detailed descriptions if possible.

</details>

</details>

<details>
<summary><strong>🤝 Contributing</strong></summary>

Contributions to MindsDB are welcome! We appreciate your interest in improving the project. Here are some ways you can contribute:

- **Bug Reports**: Submit detailed bug reports with steps to reproduce
- **Feature Requests**: Suggest new features or improvements
- **Code Contributions**: Submit pull requests with bug fixes or new features
- **Documentation**: Help improve documentation and examples
- **Testing**: Help test new features and report issues

Please read our contributing guidelines for more information on how to get involved.

</details>

<details>
<summary><strong>📄 License</strong></summary>

This project is licensed under the MIT License - see the LICENSE file for details.

### MIT License Summary
- ✅ Commercial use
- ✅ Modification
- ✅ Distribution
- ✅ Private use
- ❌ Liability
- ❌ Warranty

</details>

---

## 🚀 Quick Start

1. **Install MindsDB**: `pip install mindsdb`
2. **Start MindsDB**: `python -m mindsdb`
3. **Configure API Key**: Add your OpenAI API key to `.env` file
4. **Run Application**: Choose CLI (`python cli_app.py`) or Web (`python app.py`)
5. **Access Web Interface**: Open `http://localhost:5000` in your browser

---

## 📞 Support

If you encounter any issues or have questions:
- Check the troubleshooting section in the setup guide
- Visit the [MindsDB Documentation](https://docs.mindsdb.com/)
- Open an issue on the [MindsDB GitHub repository](https://github.com/mindsdb/mindsdb)

---

**Happy coding with MindsDB! 🎉**
