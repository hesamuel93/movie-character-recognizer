# Recognize and Sort Movie/Cartoon Characters from Images
Suppose that you have collected images of your favorite movie/TV/comic characters, perhaps by mass downloading from online image galleries. You put all the images in one folder, but it ends up being too large and messy, with too many different characters. You can use this tool to sort them into smaller, more accessible subfolders.

## Uploading Images for Recognition
Upload 3 to 5 images of a specific movie/TV/comic character that your are a fan of, or even images of original characters that you created/designed yourself. These characters will be "memorized" by storing their embeddings and patterns.

## Organize/Sort By Character
Have a folder with all the character images that you want to be sorted. Upload this folder, making sure that it only contains the allowed image files. Afterwards, the images should be sorted into the proper subfolders by their character embeddings (You can find these subfolders inside the 'static/characters' directory). If the program did not recognize a character from the image (e.g. the character's embeddings were not initially uploaded, or the image did not pass the accuracy threshold), the image will be stored in a subfolder called 'UNKNOWN'.

## How It's Made
The tool mainly uses the CLIP model from OpenAI, as well as cosine similarity tests, to analyze the images and recognize the characters. The app can be run locally, with a backend built on Python and a frontend built on Javascript and HTML.

## Usage
Once you clone/download this project, you can use it by first executing the *python "app.py"* command in your terminal.
Then, go to *http://127.0.0.1:5000* in your browser to run the web app.
Upload 3 to 5 images for a character, and when you are done you can press the "Upload Character" button to have that character's embeddings saved.
Then, to sort a folder of different character images, upload the folder using the "Recognize Characters" feature. The images will be sorted by character in the 'static/characters' directory.
You can view the total images of a character using the "View Gallery" option.

## Potential Future Updates
The program currently does not work accurately when a character does not occupy the bulk of an image, which is common for images that contain multiple characters. The application can be more useful if it splits images using their embeddings to pinpoint each character, and then adding the images to each respective folder.
