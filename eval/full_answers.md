# Evaluation

## Q1: What is a markdown file?

### LLM Only:
A Markdown file is a plain text file that uses a simple syntax to format text. It's designed to be easy to read and write, and it can be converted to HTML or other formats. Think of it as a lightweight markup language.

Here's a breakdown:

*   **Plain Text:** Markdown files are just regular text files (like those you'd create in Notepad or TextEdit). This means you can open and edit them with any text editor.

*   **Simple Syntax:** Markdown uses special characters and symbols to indicate formatting. For example:
    *   `#` for headings
    *   `*` or `_` for emphasis (italics)
    *   `**` or `__` for strong emphasis (bold)
    *   `-` or `*` or `+` for lists
    *   `[]()` for links
    *   `` ` `` for inline code
    *   ` ``` ` for code blocks

*   **Human-Readable:** The syntax is designed to be readable even without being rendered. You can generally understand the structure and content of a Markdown file just by looking at the text.

*   **Convertible:** Markdown files can be easily converted to HTML (the language of web pages) or other formats like PDF, DOCX, etc. This is usually done using a Markdown processor or converter.

*   **File Extension:** Markdown files typically have the `.md` or `.markdown` file extension.

**Why use Markdown?**

*   **Simplicity:** It's easy to learn and use.
*   **Portability:** Markdown files can be opened and edited on any platform.
*   **Version Control Friendly:** Plain text files are ideal for version control systems like Git.
*   **Widely Supported:** Many platforms and applications support Markdown, including:
    *   GitHub, GitLab, and other code hosting platforms
    *   Note-taking apps (e.g., Obsidian, Notion, Bear)
    *   Documentation generators (e.g., Jekyll, Hugo)
    *   Content management systems (CMS)

**Example:**

Here's a simple Markdown file:

```markdown
# My Awesome Document

This is a paragraph of text.  It's *easy* to write and **read**.

Here's a list:

*   Item 1
*   Item 2
*   Item 3

### LLM + RAG:
A markdown file is a text file that uses markdown language syntax. It is used to format text by adding elements such as headings, lists, and links using plain text.

---

## Q2: What is the difference between Flask and FastAPI?

### LLM Only:
Flask and FastAPI are both popular Python web frameworks, but they cater to different needs and have distinct design philosophies. Here's a breakdown of their key differences:

**1. Performance:**

*   **FastAPI:** Designed for high performance from the ground up. It leverages asynchronous programming (using `async` and `await`) and the Pydantic library for data validation and serialization. This results in significantly faster execution speeds, especially for I/O-bound operations like API calls.
*   **Flask:** Traditionally synchronous. While you can use asynchronous libraries like `asyncio` with Flask, it's not as deeply integrated as in FastAPI.  Flask's performance is generally good for smaller to medium-sized applications, but it can become a bottleneck in high-traffic scenarios.

**2. Asynchronous Support:**

*   **FastAPI:**  Built-in and first-class support for asynchronous programming.  This makes it ideal for handling concurrent requests efficiently, leading to better performance and scalability.
*   **Flask:**  Requires additional libraries and configurations to implement asynchronous functionality.  While possible, it's not as seamless or performant as FastAPI's native support.

**3. Data Validation and Serialization:**

*   **FastAPI:** Uses Pydantic for data validation and serialization. Pydantic provides type hints and automatically validates incoming data against these types. It also handles serialization to JSON and other formats. This reduces boilerplate code and improves data integrity.
*   **Flask:**  Requires manual data validation and serialization. You typically use libraries like Marshmallow or custom code to handle these tasks. This can be more verbose and error-prone.

**4. Automatic API Documentation:**

*   **FastAPI:**  Automatically generates interactive API documentation using OpenAPI (Swagger UI) and ReDoc. This documentation is based on the type hints and data models defined in your code, making it easy to keep up-to-date.
*   **Flask:**  Requires separate tools like Flask-RESTplus or Flask-Swagger to generate API documentation. This adds extra steps to the development process.

**5. Type Hints:**

*   **FastAPI:**  Heavily relies on Python type hints. Type hints are used for data validation, serialization, and automatic API documentation.
*   **Flask:**  Type hints are optional. While you can use them, they are not as central to the framework's functionality.

**6. Learning Curve:**

*

### LLM + RAG:
- Flask is a micro web framework, offering simplicity and flexibility with extensions for added functionality.
- FastAPI is a modern, high-performance web framework with built-in support for asynchronous code and automatic data validation using type hints.

---

## Q3: How can I handle CORS in Flask?

### LLM Only:
There are several ways to handle CORS (Cross-Origin Resource Sharing) in Flask, ranging from simple solutions for development to more robust and configurable options for production. Here's a breakdown of common approaches:

**1. Using the `Flask-CORS` Extension (Recommended)**

This is the most common and recommended approach for handling CORS in Flask.  It provides a clean and configurable way to manage CORS headers.

*   **Installation:**

    ```bash
    pip install Flask-Cors
    ```

*   **Basic Usage (Allowing all origins):**

    ```python
    from flask import Flask
    from flask_cors import CORS

    app = Flask(__name__)
    CORS(app)  # Enable CORS for all routes

    @app.route("/")
    def hello_world():
        return "<p>Hello, World!</p>"

    if __name__ == '__main__':
        app.run(debug=True)
    ```

    This simple example enables CORS for all routes in your Flask application, allowing requests from any origin.  This is generally **not recommended for production** due to security concerns.

*   **Configuring Allowed Origins (Recommended for Production):**

    ```python
    from flask import Flask
    from flask_cors import CORS

    app = Flask(__name__)
    CORS(app, origins=["http://localhost:3000", "https://www.example.com"])  # Specify allowed origins

    @app.route("/")
    def hello_world():        return "<p>Hello, World!</p>"

    if __name__ == '__main__':
        app.run(debug=True)
    ```

    This is the preferred approach for production.  The `origins` parameter accepts:

    *   A list of specific origins (as shown above).    *   A string representing a single origin.
    *   `"*"` (allow all origins - **use with caution**).
    *   A regular expression pattern (using `re.compile`).
    *   `None` (disable CORS).

*   **Configuring Allowed Methods, Headers, and Credentials:**

    `Flask-CORS` allows fine-grained control over CORS behavior:

    ```python
    from flask import Flask
    from flask_cors import CORS

    app = Flask(__name__)
    CORS

### LLM + RAG:
To handle CORS in Flask, you can use the Flask-CORS extension.

```python
from flask import Flask
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

@app.route("/")
def hello():
    return "Hello World!"

if __name__ == "__main__":
    app.run()
```

This will enable CORS for all routes in your Flask application. You can also configure CORS for specific routes or origins.

---
