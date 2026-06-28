import os  # Import the "os" module to work with file paths and directories in the Flask application.
from flask import Flask, request, render_template, url_for

app = Flask(__name__)

# Set the upload folder for storing uploaded files by using the constant "UPLOAD_FOLDER" and relative path "static/uploads".
app.config["UPLOAD_FOLDER"] = "static/uploads"

if not os.path.exists(app.config["UPLOAD_FOLDER"]):
    os.makedirs(app.config["UPLOAD_FOLDER"])


@app.route("/", methods=["GET", "POST"])
def upload_file():

    # Set the variable "image_url" to None to initialize it before processing any uploaded files.
    image_url = None

    if request.method == "POST" and "my_image" in request.files:
        # Get the uploaded file from the request files and store it in the variable "file".
        file = request.files["my_image"]

        if file and file.filename is not None and file.filename != "":
            # Create the full path to save the uploaded file by joining the upload folder path and the filename of the uploaded file using "os.path.join".
            save_path = os.path.join(app.config["UPLOAD_FOLDER"], file.filename)

            file.save(save_path)

            image_url = url_for(
                "static", filename=f"uploads/{file.filename}"
            )  # Generate the URL for the uploaded image by using the "url_for" function and passing the "static" endpoint and the filename of the uploaded file.

    # Render the 'index.html' template, passing the 'image_url' value from Python to the HTML variable for displaying the uploaded image.
    return render_template("index.html", image_url=image_url)


if __name__ == "__main__":
    app.run(
        debug=True, port=5001
    )  # Run the Flask application in debug mode on port 5001.
