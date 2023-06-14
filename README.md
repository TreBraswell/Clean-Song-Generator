# Clean Song Generator

**Note: This project is currently in progress and not yet complete.**

Censor Song is a Python application that allows you to censor explicit content in a mp3 audio file. It provides options to use Shazam for extra timestamps and Audacity for audio editing. The application creates a graphical user interface (GUI) using the Tkinter library for easy interaction.

## Prerequisites

Before running the Censor Song application, ensure that you have the following:

- Python 3.x installed on your machine
- Tkinter library installed (included with most Python installations)
- Audacity installed (if using the Audacity option)

## Installation

1. Clone the repository to your local machine:

```bash
git clone https://github.com/TreBraswell/Clean-Song-Generator.git
```

2. Change into the project directory:

```bash
cd Clean-Song-Generator
```

3. Install the required Python dependencies:

```bash
pip install -r requirements.txt
```

## Usage

1. Open the terminal and navigate to the project directory.

2. Run the following command to start the Censor Song application:

```bash
python main.py
```

3. The GUI window will appear with the following options:

   - **Use Shazam to get extra timestamps:** Enable this option if you want to use Shazam for additional timestamps.
   - **Use Audacity:** Enable this option if you want to use Audacity for audio editing.
   - **Delete Audacity tracks after finishing:** Enable this option if you want to delete the Audacity tracks once the censoring process is complete.

4. Click on the **Press when done** button when you have made your selections.

5. A file dialog will appear. Select the WAV audio file you want to censor.

6. The censoring process will start, and it may take a few minutes to complete. Progress and status will be displayed in the terminal.

7. Once the censoring process finishes, the censored audio file will be saved in the same directory as the original file.

## Contributing

Contributions to the Censor Song project are welcome! If you find any issues or have suggestions for improvements, please create an issue or submit a pull request.

## Acknowledgments

- The Censor Song project is inspired by the need to provide a convenient tool for censoring explicit content in audio files.

## Contact

If you have any questions, suggestions, or feedback, please feel free to contact [Tre Braswell](mailto:trebraswell@gmail.com).
