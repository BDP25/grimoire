# Evaluation

## Q1: What is a markdown file?

### LLM Only:
A Markdown file is a plain text file that uses a simple syntax to format text. This syntax, called Markdown, allows you to add elements like headings, lists, links, and emphasis (bold, italics) to your text without using complex word processing software.

Here's a breakdown:

*   **Plain Text:** Markdown files are just text files (like `.txt` files). You can open and edit them with any text editor (Notepad, VS Code, Sublime Text, etc.).  This makes them highly portable and future-proof.

*   **Markdown Syntax:**  The key is the special characters and conventions used to indicate formatting.  For example:

    *   `#` at the beginning of a line creates a heading.  `# Heading 1`, `## Heading 2`, `### Heading 3`, etc.
    *   `*` or `_` around text creates italics: `*italics*` or `_italics_`
    *   `**` or `__` around text creates bold: `**bold**` or `__bold__`
    *   `-` or `*` or `+` at the beginning of a line creates a bulleted list.
    *   `[Link Text](URL)` creates a hyperlink.
    *   `` `code` `` creates inline code.
    *   ```
        code block
        ``` creates a code block.

*   **File Extension:** Markdown files typically have the extension `.md` or `.markdown`.

*   **Purpose:** Markdown is designed to be easy to read in its raw form and easy to convert to other formats like HTML, PDF, or even Word documents.

*   **Conversion:**  A "Markdown processor" or "Markdown parser" is used to convert the Markdown syntax into formatted output.  Many text editors, websites (like GitHub, Reddit, Stack Overflow), and tools have built-in Markdown processors.

**Why use Markdown?**

*   **Simplicity:**  Easy to learn and use.
*   **Readability:**  Markdown files are readable even without being processed.
*   **Portability:**  Plain text files can be opened and edited on any platform.
*   **Versatility:**  Can be converted to various formats.
*   **Version Control Friendly:**  Plain text files are ideal for version control systems like Git.
*   **Widely Supported:**

### LLM + RAG:
Grimoire 🔮:

---

## Q2: What is the difference between Flask and FastAPI?

### LLM Only:
Flask and FastAPI are both popular Python web frameworks, but they cater to different needs and have distinct design philosophies. Here's a breakdown of their key differences:

**1. Performance:**

*   **FastAPI:** Designed for high performance from the ground up. It leverages asynchronous programming (using `async` and `await`) and is built on top of Starlette and Pydantic. This makes it significantly faster than Flask, especially for I/O-bound operations like API calls.
*   **Flask:** Traditionally synchronous. While you can use asynchronous libraries with Flask, it's not as deeply integrated or as performant as FastAPI in asynchronous scenarios.  Flask's performance is generally good for smaller to medium-sized applications, but it can become a bottleneck for high-traffic APIs.

**2. Data Validation and Serialization:**

*   **FastAPI:** Uses Pydantic for data validation and serialization. Pydantic provides automatic data validation, serialization, and documentation generation based on Python type hints. This significantly reduces boilerplate code and ensures data consistency.
*   **Flask:** Requires manual data validation and serialization. You typically use libraries like Marshmallow or Cerberus for these tasks, which adds complexity and code.

**3. Automatic API Documentation:**

*   **FastAPI:** Generates interactive API documentation (using OpenAPI and Swagger UI or ReDoc) automatically based on your code and type hints. This is a huge time-saver and ensures your API documentation is always up-to-date.
*   **Flask:** Requires manual creation and maintenance of API documentation, often using tools like Flask-RESTful or third-party libraries.

**4. Asynchronous Programming:**

*   **FastAPI:** Embraces asynchronous programming as a core feature. It's designed to handle concurrent requests efficiently, making it ideal for applications that need to handle a large number of simultaneous connections.
*   **Flask:** Primarily synchronous. While you can use asynchronous libraries like `asyncio` with Flask, it requires more effort and doesn't offer the same level of performance as FastAPI.

**5. Dependency Injection:**

*   **FastAPI:** Has built-in support for dependency injection. This allows you to easily manage dependencies and write more testable and maintainable code.
*   **Flask:** Doesn't have built-in dependency injection. You can implement it using third-party libraries, but it's not as seamless as in FastAPI.

**6. Learning

### LLM + RAG:
Grimoire 🔮:

---

## Q3: How can I handle CORS in Flask?

### LLM Only:
There are several ways to handle CORS (Cross-Origin Resource Sharing) in Flask, ranging from simple solutions for development to more robust and configurable approaches for production. Here's a breakdown of common methods:

**1. Using the `Flask-CORS` Extension (Recommended)**

This is the most common and recommended approach for handling CORS in Flask.  It provides a clean and configurable way to manage CORS headers.

   * **Installation:**

     ```bash
     pip install Flask-Cors
     ```

   * **Basic Usage (Allowing all origins):**

     ```python
     from flask import Flask
     from flask_cors import CORS

     app = Flask(__name__)
     CORS(app)  # Enable CORS for all routes

     @app.route("/")
     def hello():
         return "Hello World!"

     if __name__ == "__main__":
         app.run(debug=True)
     ```

     This simple example enables CORS for *all* routes in your Flask application, allowing requests from *any* origin.  This is generally **not recommended for production** due to security concerns.

   * **Configuring Allowed Origins (Recommended for Production):**

     ```python
     from flask import Flask
     from flask_cors import CORS

     app = Flask(__name__)
     CORS(app, origins=["http://localhost:3000", "https://www.example.com"])  # Specify allowed origins

     @app.route("/")
     def hello():
         return "Hello World!"

     if __name__ == "__main__":
         app.run(debug=True)
     ```

     This is the preferred approach for production.  The `origins` parameter specifies a list of allowed origins.  Only requests from these origins will be allowed.

   * **More Configuration Options:**

     `Flask-CORS` offers many configuration options:

     * `origins`:  A list of allowed origins (strings or regular expressions).  Use `"*"` to allow all origins (not recommended for production).
     * `methods`: A list of allowed HTTP methods (e.g., `["GET", "POST", "PUT", "DELETE"]`).  Defaults to `["GET", "HEAD", "OPTIONS"]`.
     * `allow_headers`: A list of allowed headers.  Defaults to `["Content-Type", "Authorization"]

### LLM + RAG:
Grimoire 🔮:

---
