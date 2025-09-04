# Movie Character Recognizer
Upload images of a specific movie/TV/comic character that your are a fan of, or even images of original characters that you created/designed yourself.
Then, if you have more images of characters, and you want to group them together into one collection, you can do so using this tool.

## How It's Made
The tool mainly uses the CLIP model from OpenAI, as well as cosine similarity tests, to analyze the images and recognize the characters. The app can be run on the web, with a backend built on Python and a frontend built on Javascript and HTML.

## Usage
Once you clone/download this project, you can use it by first executing the *python "app.py"* command.
Then, open the html file or go to *http://127.0.0.1:5000* in your browser to run the web app.
You can upload as many images for a character as you want, and when you are done you can press the "Save Character" button to have it saved.
To recognize a character from an image, upload the image and just press the "Recognize Character" button.

## Possible Improvements
I'm working on making it so that you can recognize multiple characters from a folder of images, so that they can eventually be sorted. I also want to display the images of each character in a gallery format, which will require more work on the HTML and Javascript parts of the app.
