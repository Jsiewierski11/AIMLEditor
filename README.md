# AIMLEditor
A graphical AIML editor written in python 3 and pyqt5.

# GUI
The editor has 2 different displays.
- A text edit display akin to notepad++
- A graphical view to display conversation flow (Coming soon)
    - The Node Editor for the graph view is borrowed from [here](https://gitlab.com/pavel.krupala/pyqt-node-editor-tutorials)


# Notes about the Project

## To Run the Project
- Simply run the following command in the root directory: 
    ```
    python main.py
    ``` 

## To Run Test Cases
- Make sure you are inside of the Tests directory.
- From there run:
    ```
    python -m unittest -v test_cases.py
    ```

# Using the Editor
- Any time a change is made to the editspace be sure to compile to properly save what you are showing on screen.
- The tabs labeled as "Text Display" and "Graph Display" will turn red when changes are made indicating you need to compile the code.
- Once the code has been properly compiled the tabs will be reset to their normal color.
- A popup window will appear if you have not compiled your code before you try to export.