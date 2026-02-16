from flask import Flask, render_template, request
import requests

app = Flask(__name__)


@app.route("/", methods=["GET", "POST"])
def index():
    books = []
    error = None
    if request.method == "POST":
        query = request.form.get("book_name")
        if query:
            try:
                url = f"https://openlibrary.org/search.json?q={query}&limit=50"
                response = requests.get(url)
                response.raise_for_status()
                data = response.json()
                docs = data.get("docs", [])
                if not docs:
                    error = "NO books found"
                else:
                    for doc in docs:
                        title = doc.get("title", "No title")
                        authors = ", ".join(doc.get("author_name", ["Unknown author"]))
                        year = doc.get("first_publish_year", "Unknown year")
                        books.append(f"{title} by {authors} ({year})")
            except Exception as e:
                error = str(e)
    return render_template("index.html", books=books, error=error)


if __name__ == "__main__":
    app.run(debug=True)
