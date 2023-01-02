m8_data_cleaner
A tool designed for the task of preparing a directory of samples for use in a Dirtywave M8.

Author
Jacob Leone aka Jack.lion - @jack.lion710@gmail.com

Linktree: linktr.ee/Jack.Lion

License
This work is licensed under the Creative Commons Attribution-NoDerivatives 4.0 International License. To view a copy of this license, visit http://creativecommons.org/licenses/by-nd/4.0/.

Warning
PLEASE READ BEFORE USE!! This is a destructive process, meaning the changes it makes can not be undone. It is HIGHLY recommended to make duplicates of your target directory before using this to avoid unwanted changes or lost data. The code has been tested on the author's system and works well, but the author cannot accept responsibility for any lost or damaged data. Once you try the functions out and are comfortable with the configuration you have, then you may feel free to commit your changes to the files.

Description
This is the author's first public Python project. The goal of this script is to prepare a directory tree of samples for use in the Dirtywave M8. This script has several functions, each of which is designed to work independently. You can comment out or reorder the functions as desired. The default configuration is biased towards the author's preferences and the full script strips as much as possible while attempting to preserve legibility.

Functionality
convert_to_wav() - Converts different audio file types to WAV type
check_files() - Determines whether the conversion worked or not and asks the user if they wish to delete corrupt files
delete_non_wav_files() - Deletes any junk files such as .txt files and more
remove_plural_suffixes() - Strips plural suffixes such as 's', 'ies', and 'es'
remove_characters_from_filenames() - Removes illegal or potentially problematic or redundant characters
shorten_names() - Uses a language model to replace full words with shorter synonyms
remove_vowels() - Strips the names of any vowels
truncate_names() - Takes an integer as a second argument as input to limit the max length of each name
convert_bit_depth() - Converts every remaining audio file into the target bit depth determined by an integer as the input for the second argument
check_bit_depth() - Determines whether the bit depth is legal for use in the M8
split_and_trim_all() - Removes silences from the beginning and end of a file. The second input argument determines the threshold in milliseconds to detect in order for slicing to occur.
Instructions
Further instructions are listed in the main program.

Modification and Contribution
Feel free to modify this code to fit your needs or make contributions if you feel they are necessary. Just don't redistribute as your own work. If you feel like your special case warrants attention, feel free to contact the author at jack.lion710@gmail.com.

Installation
Download Python
Download the latest version of Python from https://www.python.org/downloads/.
