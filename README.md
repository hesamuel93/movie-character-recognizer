# Movie Character Recognizer
Upload images of a specific movie/TV/comic character that your are a fan of, or even images of original characters that you created/designed yourself.
Then, if you have multiple images of different characters inside a folder, and you want to have them sorted by the specific characters in each image, you can do so using this tool.

## How It's Made
The tool mainly uses the CLIP model from OpenAI, as well as cosine similarity tests, to analyze the images and recognize the characters. The app can be run locally, with a backend built on Python and a frontend built on Javascript and HTML.

## Usage
Once you clone/download this project, you can use it by first executing the *python "app.py"* command.
Then, open the html file or go to *http://127.0.0.1:5000* in your browser to run the web app.
Upload a small amount of images for a character, and when you are done you can press the "Upload Character" button to have that character's embeddings saved.
Then, to sort a folder of different character images, upload the folder using the "Recognize Character" feature. The images will be sorted by character in the 'static/characters' directory.
You can also view the images of a character using the "View Gallery" option.

## Possible Improvements
Compatability for if multiple characters are in a single image, and storage for images with no character matches.
