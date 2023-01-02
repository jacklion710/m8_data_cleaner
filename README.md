# m8_data_cleaner
A tool designed for the task of preparing a directory of samples for use in a Dirtywave M8
Author: Jacob Leone aka Jack.lion - @jack.lion710@gmail.com
Linktree: linktr.ee/Jack.Lion

This work is licensed under the Creative Commons Attribution-NoDerivatives 4.0 International License. To view a copy of
this license, visit http://creativecommons.org/licenses/by-nd/4.0/.

PLEASE READ BEFORE USE!!
This is a destructive process meaning the changes it makes can not be undone. I would HIGHLY reccomend making duplicates
of your target directory before using this to avoid unwanted changes or lost data. The code has been tested on my system
and works well for me but I can not accept responsibility for any lost or damaged data. Once you try the functions out
and are comfortable with the configuration you have, then you may feel free to commit your changes.

Description: This is my first public python project. The goal of this script is to prepare a directory tree of samples
for use in the dirtywave m8. This script does a few things. Each function is designed to work independantly so feel free
to comment out functions you don't wish to use in the main program. You can even reorder them if you prefer. The default
state is biased towards my preferences and the full script strips as much as possible by attempting to preserve
legibility.

Functionality:
1) convert_to_wav() Converts different audio file types to WAV type
2) check_files() Determines whether the conversion worked or not and asks the user if they wish to delete corrupt files
3) delete_non_wav_files() Deletes any junk files such as .txt files and more
4) remove_plural_suffixes() Strips plural suffixes such as s, ies, and es
5) remove_characters_from_filenames() Removes illegal or potentially problematic or redundant characcters
6) shorten_names() Uses a language model to replace full words with shorter synsets
7) remove_vowels() Strips the names of any vowels
8) truncate_names() Takes an integer as a second argument as input to limit the max length of each name
9) convert_bit_depth() Converts every remaining audio file into the target bit depth determined by an integer as the
input for the second argument
check_bit_depth() Determines whether the bit_depth is legal for use in the M8
split_and_trim_all() Removes silences from the beginning and end of a file. Second input argument determines the
threshold in milliseconds to detect in order for slicing to occur

Further instructions are listed in the main program

Feel free to modify this code to fit your needs or make contributions if you feel, Just don't redistribute as your own.
If you feel like your special case warrants attention, feel free to reach out at jack.lion710@gmail.com

================================================================================================================================================

Download python: https://www.python.org/downloads/

I reccomend downloading pycharm for use: https://www.jetbrains.com/pycharm/
But this code should be easy enough to port into something else if you choose.

To install the necessary modules and packages, you can use the following pip commands:
pip install os
pip install re
pip install wave
pip install struct
pip install stat
pip install nltk
pip install soundfile
pip install pydub
pip install AudioSegment
pip install pathlib

To install the necessary packages in PyCharm, you can follow these steps:

Open PyCharm and go to the "Preferences" menu (on Mac) or "Settings" menu (on Windows).
In the left panel, navigate to "Project: [Your Project Name] > Project Interpreter".
Click the "+" button in the top right corner of the window.
In the search bar, type the name of the package you want to install (e.g. "os") and press Enter.
Select the package you want to install and click the "Install Package" button.
You will need to repeat these steps for each of the necessary packages. You may also need to run the following nltk commands to download the necessary data:

import nltk
nltk.download('punkt')
nltk.download('wordnet')
