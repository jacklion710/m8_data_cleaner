'''
Title: M8 Sample Data Cleaner
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
6) abbreviate_filenames() Uses a language model to replace full words with shorter synsets
7) remove_vowels() Strips the names of any vowels
8) truncate_names() Takes an integer as a second argument as input to limit the max length of each name
9) convert_bit_depth() Converts every remaining audio file into the target bit depth determined by an integer as the
input for the second argument
10) check_bit_depth() Determines whether the bit_depth is legal for use in the M8
11) split_and_trim_all() Removes silences from the beginning and end of a file. Second input argument determines the
threshold in milliseconds to detect in order for slicing to occur

Further instructions are listed in the main program

Feel free to modify this code to fit your needs or make contributions if you feel, Just don't redistribute as your own.
If you feel like your special case warrants attention, feel free to reach out at jack.lion710@gmail.com
'''

import os
import stat
import nltk
import multiprocessing
import multiprocessing.pool
import soundfile as sf
import pydub
from pydub import AudioSegment
from pathlib import Path
import re

def run_function_in_process(func, *args):
    with multiprocessing.pool.ThreadPool(processes=1) as pool:
        result = pool.apply(func, args)
    return result

# Enables write permissions for every file in the directory
def enable_write_permissions(root_dir):
    # Recursively traverse the directory tree
    for root, dirs, files in os.walk(root_dir):
        # Enable write permissions for all files
        for file in files:
            file_path = os.path.join(root, file)
            os.chmod(file_path, stat.S_IWRITE)

# Discard non audio file types and convert remaining files into .WAV
def convert_to_wav(root_dir, verbose_permission=True):
    for root, dirs, files in os.walk(root_dir):
        for file in files:
            file_path = os.path.join(root, file)
            file_extension = os.path.splitext(file_path)[1]
            try:
                sf.SoundFile(file_path)
            except Exception as e:
                if isinstance(e, sf.SoundFileError):
                    # File is not a valid audio file
                    if file_extension in [".asd", ".alc", ".DS_Store"]:
                        # Automatically delete these file types
                        os.remove(file_path)
                    elif verbose_permission:
                        # Prompt user for permission to delete other file types
                        print(f"{file_path} is not a valid audio file. Do you want to delete it? (y/n)")
                        user_input = input()
                        if user_input.lower() == "y":
                            os.remove(file_path)
                    else:
                        # Automatically delete other file types without prompting
                        os.remove(file_path)
            else:
                if file_extension not in [".wav"]:
                    # Convert file to WAV
                    print(f"Converting {file_path} to WAV...")
                    sound = AudioSegment.from_file(file_path)
                    new_file_path = os.path.splitext(file_path)[0] + ".wav"
                    sound.export(new_file_path, format="wav")
                    os.remove(file_path)

# Delete all non-WAV files
def delete_non_wav_files(root_dir):
    for root, dirs, files in os.walk(root_dir):
        for file in files:
            if not file.endswith('.wav'):
                file_path = os.path.join(root, file)
                os.remove(file_path)

# Confirms whether the files are WAV, another type, or corrupt
def check_files(root_dir):
    corrupt_files = []
    for root, dirs, files in os.walk(root_dir):
        for file in files:
            file_path = os.path.join(root, file)
            if not file.endswith('.wav'):
                print(f'{file_path} is not a WAV file')
            else:
                try:
                    sf.SoundFile(file_path)
                except Exception as e:
                    print(f'{file_path} is corrupt or damaged: {e}')
                    corrupt_files.append(file_path)
    return corrupt_files

# Strips plural suffixes
def remove_plural_suffixes(root_dir):
    def remove_plural_suffixes(s):
        print(f"Removing plural suffixes from {root_dir}")
        pattern = r'(?i)(?<=[^s])s|(?<=[^es])es|(?<=[^ies])ies'
        #pattern = r'(?i)(?:[^s]|^)s(?=$|[^a-z])|(?i)(?:[^es]|^)es(?=$|[^a-z])|(?i)(?:[^ies]|^)ies(?=$|[^a-z])|(?i)(?:[^\'en]|^)[\'en](?=$|[^a-z])'
        return re.sub(pattern, '', s)

    for root, dirs, files in os.walk(root_dir):
        # Remove plural suffixes from the directory names
        for i, dir in enumerate(dirs):
            print(f"Removing plurals from directory {dir}")
            old_name = os.path.join(root, dir)
            new_name = remove_plural_suffixes(dir)
            new_name = os.path.join(root, new_name)
            try:
                os.rename(old_name, new_name)
            except FileNotFoundError:
                # Handle the error here
                pass
        # Remove plural suffixes from the file names
        for file in files:
            print(f"Removing plurals from file {file}")
            old_file_path = os.path.join(root, file)
            name, ext = os.path.splitext(file)
            new_name = remove_plural_suffixes(name)
            new_file_path = os.path.join(root, new_name + ext)
            if old_file_path != new_file_path:
                try:
                    os.rename(old_file_path, new_file_path)
                except FileNotFoundError:
                    # Handle the error here
                    pass

# Remove redundant and illegal characters from files and folders
def remove_characters_from_filenames(root_dir):
    def remove_characters_from_string(s):
        return re.sub(r'[^a-zA-Z0-9]', '', s)

    def process_directories(root, dirs):
        subdirs = []
        for dir in dirs:
            old_name = os.path.join(root, dir)
            new_name = remove_characters_from_string(dir)
            if old_name != os.path.join(root, new_name):
                os.rename(old_name, os.path.join(root, new_name))
                subdirs.append(new_name)
        return subdirs

    def process_files(root, files):
        for file in files:
            old_file_path = os.path.join(root, file)
            name, ext = os.path.splitext(file)
            new_name = remove_characters_from_string(name)
            new_file_path = os.path.join(root, new_name + ext)
            counter = 1
            while os.path.exists(new_file_path):
                new_name = f"{new_name}_{counter}"
                new_file_path = os.path.join(root, new_name + ext)
                counter += 1
            if old_file_path != new_file_path:
                os.rename(old_file_path, new_file_path)

    subdirs = []
    for root, dirs, files in os.walk(root_dir):
        subdirs = process_directories(root, dirs)
        process_files(root, files)
        for subdir in subdirs:
            remove_characters_from_filenames(os.path.join(root, subdir))

# Use a language model to shorten names with synsets
def abbreviate_filenames(root_dir):
    def abbreviate_string(s):
        words = nltk.word_tokenize(s)
        abbreviated_words = []
        for word in words:
            synonyms = nltk.corpus.wordnet.synsets(word)
            if synonyms:
                lemmas = [lemma.name() for synset in synonyms for lemma in synset.lemmas()]
                shortest_lemma = min(lemmas, key=len)
                abbreviated_words.append(shortest_lemma if len(shortest_lemma) < len(word) else word)
            else:
                abbreviated_words.append(word)
        return "".join(abbreviated_words)

    def process_directories(root, dirs):
        subdirs = []
        for dir in dirs:
            old_name = os.path.join(root, dir)
            new_name = abbreviate_string(dir)
            if old_name != os.path.join(root, new_name):
                os.rename(old_name, os.path.join(root, new_name))
                subdirs.append(new_name)
        return subdirs

    def process_files(root, files):
        for file in files:
            old_file_path = os.path.join(root, file)
            name, ext = os.path.splitext(file)
            new_name = abbreviate_string(name)
            new_file_path = os.path.join(root, new_name + ext)
            counter = 1
            while os.path.exists(new_file_path):
                new_name = f"{new_name}_{counter}"
                new_file_path = os.path.join(root, new_name + ext)
                counter += 1
            if old_file_path != new_file_path:
                os.rename(old_file_path, new_file_path)

    subdirs = []
    for root, dirs, files in os.walk(root_dir):
        subdirs = process_directories(root, dirs)
        process_files(root, files)
        for subdir in subdirs:
            abbreviate_filenames(os.path.join(root, subdir))

# # Strip vowel characters from names
def remove_vowels(root_dir):
    def remove_vowels_from_string(s):
        pattern = r'[aeiouAEIOU]'
        return re.sub(pattern, '', s)

    def process_directories(root, dirs):
        subdirs = []
        for dir in dirs:
            old_name = os.path.join(root, dir)
            new_name = remove_vowels_from_string(dir)
            if old_name != os.path.join(root, new_name):
                try:
                    os.rename(old_name, os.path.join(root, new_name))
                except PermissionError:
                    print(f'PermissionError: Unable to rename {old_name}')
            subdirs.append(new_name)
        return subdirs

    def process_files(root, files):
        for file in files:
            old_file_path = os.path.join(root, file)
            name, ext = re.split(f"{os.extsep}(?!.*{os.extsep})", file)
            new_name = remove_vowels_from_string(name)
            counter = 1
            while os.path.exists(os.path.join(root, f"{new_name}{ext}")):
                new_name = f"{new_name}_{counter}"
                counter += 1
            if old_file_path != os.path.join(root, f"{new_name}{ext}"):
                try:
                    os.rename(old_file_path, os.path.join(root, f"{new_name}{ext}"))
                except PermissionError:
                    print(f'PermissionError: Unable to rename {old_file_path}')

    subdirs = []
    for root, dirs, files in os.walk(root_dir, followlinks=True):
        subdirs = process_directories(root, dirs)
        process_files(root, files)
        for subdir in subdirs:
            remove_vowels(os.path.join(root, subdir))

# Clip filename and directory name lengths
def truncate_names(root_dir, length):
    # Enable write permissions for all files and directories
    enable_write_permissions(root_dir)

    file_names = {}  # Dictionary to store the new names of the files

    # Truncate file names
    for root, dirs, files in os.walk(root_dir):
        for file in files:
            f = Path(file)
            name, ext = f.stem, f.suffix
            if len(name) > length:
                old_name = os.path.join(root, file)
                new_name = os.path.join(root, name[:length] + ext)
                counter = 1
                while os.path.exists(new_name):
                    new_name = os.path.join(root, name[:length] + "-" + str(counter) + ext)
                    counter += 1
                try:
                    os.rename(old_name, new_name)
                except PermissionError:
                    # Skip the file or directory that caused the error
                    continue
                file_names[old_name] = new_name  # Store the new name in the dictionary

    # Truncate directory names
    for root, dirs, files in os.walk(root_dir):
        for dir in dirs:
            if len(dir) > length:
                old_name = os.path.join(root, dir)
                new_name = os.path.join(root, dir[:length])
                counter = 1
                while os.path.exists(new_name):
                    new_name = os.path.join(root, dir[:length] + "-" + str(counter))
                    counter += 1
                try:
                    os.rename(old_name, new_name)
                except PermissionError:
                    # Skip the file or directory that caused the error
                    continue

                # Update the names of the files in the directory
                for file in files:
                    old_file_name = os.path.join(old_name, file)
                    new_file_name = os.path.join(new_name, file)
                    if old_file_name in file_names:
                        file_names[new_file_name] = file_names[old_file_name]
                        del file_names[old_file_name]

# Traverse the directory tree and convert all audio files bitdepth
def convert_bit_depth(root_dir, target_bit_depth):
    # Use os.walk() to loop through all the subdirectories in the tree
    for root, dirs, files in os.walk(root_dir):
        # Loop through all the files in the current directory
        for filename in files:
            # Check if the file is an audio file
            if filename.endswith(".mp3") or filename.endswith(".wav"):
                # Set the input and output filenames
                input_filename = os.path.join(root, filename)
                print(f"Converting {input_filename} to {target_bit_depth} bits")
                # Get the base name and extension of the input file
                filename, file_extension = os.path.splitext(input_filename)
                output_path = os.path.dirname(input_filename)
                output_filename = os.path.join(output_path, filename + "_converted" + file_extension)
                # Read the audio data from the input file
                data, samplerate = sf.read(input_filename)
                try:
                    # Write the audio data to the output file with the desired bit depth
                    sf.write(output_filename, data, samplerate, subtype=f'PCM_{target_bit_depth}')
                except TypeError as e:
                    if "No format specified" in str(e):
                        print(
                            f"Unable to write file {output_filename} because the format could not be determined from the file extension")
                        # Print an error message and continue with the next file
                        continue
                    else:
                        # If the error is not related to the format not being specified, re-raise the error
                        raise e
                # Delete the original file and rename the new file
                os.remove(input_filename)
                os.rename(output_filename, input_filename)

# Double check to make sure bitdepth was downsampled properly
def check_bit_depth(root_dir):
    all_files_32bit = True
    failing_files = []
    for root, dirs, files in os.walk(root_dir):
        for file in files:
            if file.endswith('.wav'):
                file_path = os.path.join(root, file)
                with sf.SoundFile(file_path) as f:
                    # Check the subtype of the WAV file
                    if f.subtype in ["PCM_32", "FLOAT"]:
                        all_files_32bit = False
                        failing_files.append(file_path)
    if all_files_32bit:
        print('All files are less than 32 bits')
    else:
        print('The following files have a bit depth of at least 32 bits:')
        for file in failing_files:
            print(file)

# Removes silences from the beginning and end of smaples
def split_and_trim_all(root_dir, min_segment_len):
    # Recursively traverse the directory tree
    for root, dirs, files in os.walk(root_dir):
        # Split and trim each audio file
        for file in files:
            file_path = os.path.join(root, file)
            try:
                # Load the audio file
                sound = AudioSegment.from_file(file_path)
            except pydub.exceptions.CouldntDecodeError as e:
                # Couldn't decode the file
                print(f"An error occurred while trying to decode {file_path}: {e}")
                continue

            # Split the audio file into segments based on periods of silence
            segments = []
            start = 0
            while start < len(sound):
                end = start + min_segment_len  # Split the audio file into segments of min_segment_len milliseconds
                segment = sound[start:end]
                rms = segment.rms
                if rms < 50:  # Threshold for silence
                    # Append the segment to the list of segments
                    segments.append(segment)
                start = end

            # Trim the segments that are too short
            segments = [segment for segment in segments if len(segment) > min_segment_len]

            # Save the segments to new files
            for i, segment in enumerate(segments):
                new_file_path = f"{file_path.rsplit('.', 1)[0]}_{i + 1}.wav"
                segment.export(new_file_path, format="wav")

'''
Main program
you can rearrange these functions below into any order you prefer, delete or comment our functions don't wish to use and
even add your own functionality.
'''

if __name__ == '__main__':

    # Set the directory where the audio files are located
    root_dir = 'C:/Users/Jake/Desktop/Tree'

    # Set variables
    max_name_length = 12 # Desired max length of file and folder names
    min_segment_len = 250 # Length of silence at beginning and end of sample required to slice silences in milliseconds
    target_bit_depth = 16 # Set desired bitdepth, M8 supports bit depths less than 32bits but 16bit is recommended
    Verbose_Permissions = False # 'True' enables user permissions before deletion of files. False deletes all non audio files

    # Operations
    # convert_to_wav(root_dir, Verbose_Permissions)
    #
    # check_files(root_dir)
    #
    # delete_non_wav_files(root_dir)
    #
    # remove_plural_suffixes(root_dir)
    #
    # remove_characters_from_filenames(root_dir)
    #
    # # abbreviate_filenames(root_dir)
    #
    # # remove_vowels(root_dir)
    #
    # truncate_names(root_dir, max_name_length)

    convert_bit_depth(root_dir, target_bit_depth) # CHECK THIS FUNCTION

    check_bit_depth(root_dir)

    # split_and_trim_all(root_dir, min_segment_len) # EXPERIMENTAL Try in a small batch first.

    print("Done")
