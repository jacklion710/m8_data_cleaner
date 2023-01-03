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
6) shorten_names() Uses a language model to replace full words with shorter synsets
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
import re
import wave
import struct
import stat
from nltk.corpus import wordnet
from nltk.tokenize import word_tokenize
import soundfile as sf
import pydub
from pydub import AudioSegment
from pathlib import Path

# Converts audio files into WAV type
def convert_to_wav(root_dir):
    for root, dirs, files in os.walk(root_dir):
        for file in files:
            file_path = os.path.join(root, file)
            file_extension = os.path.splitext(file_path)[1]
            try:
                sf.SoundFile(file_path)
            except Exception as e:
                if isinstance(e, sf.SoundFileError):
                    # File is not a valid audio file
                    print(f"{file_path} is not a valid audio file. Do you want to delete it? (y/n)")
                    user_input = input()
                    if user_input.lower() == "y":
                        os.remove(file_path)
                else:
                    # Other error occurred while trying to read file
                    print(f"An error occurred while trying to read {file_path}: {e}")
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
        pattern = r'(?i)(?<=[^s])s|(?<=[^es])es|(?<=[^ies])ies'
        return re.sub(pattern, '', s)

    for root, dirs, files in os.walk(root_dir):
        # Remove plural suffixes from the directory names
        for i, dir in enumerate(dirs):
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

# Enables write permissions for every file in the directory
def enable_write_permissions(root_dir):
    # Recursively traverse the directory tree
    for root, dirs, files in os.walk(root_dir):
        # Enable write permissions for all files
        for file in files:
            file_path = os.path.join(root, file)
            os.chmod(file_path, stat.S_IWRITE)

# Remove redundant and illegal characters from files and folders
def remove_characters_from_filenames(root_dir):
    changed_dirs = True
    changed_files = True
    while changed_dirs or changed_files:
        changed_dirs = False
        changed_files = False
        for root, dirs, files in os.walk(root_dir):
            # Remove illegal characters from the directory names
            for i, dir in enumerate(dirs):
                new_name = re.sub(r'[^a-zA-Z0-9]', '', dir)
                old_name = os.path.join(root, dirs[i])
                new_name = os.path.join(root, new_name)
                if old_name != new_name:
                    os.rename(old_name, new_name)
                    changed_dirs = True
            # Remove illegal characters from the file names
            for file in files:
                f = Path(file)
                name, ext = f.stem, f.suffix
                new_name = re.sub(r'[^a-zA-Z0-9]', '', name)
                new_file_path = os.path.join(root, new_name + ext)
                if os.path.join(root, file) != new_file_path:
                    os.rename(os.path.join(root, file), new_file_path)
                    changed_files = True

# Use a language model to shorten names with synsets
def shorten_names(root_dir):
    def get_synonyms(word):
        synonyms = []
        for syn in wordnet.synsets(word):
            for lemma in syn.lemmas():
                synonyms.append(lemma.name())
        return set(synonyms)

    def remove_plural_suffixes(s):
        pattern = r'(?i)(?<=[^s])s|(?<=[^es])es|(?<=[^ies])ies'
        return re.sub(pattern, '', s)

    for root, dirs, files in os.walk(root_dir):
        # Shorten the names of the files
        for file in files:
            file_path = os.path.join(root, file)
            file_name, file_extension = os.path.splitext(file)
            words = word_tokenize(file_name)
            new_file_name = ''
            for word in words:
                synonyms = get_synonyms(word)
                if len(synonyms) > 0:
                    new_file_name += min(synonyms, key=len)
                else:
                    new_file_name += word
            new_file_name = remove_plural_suffixes(new_file_name)
            new_file_path = os.path.join(root, new_file_name + file_extension)
            os.rename(file_path, new_file_path)

# Strip vowel characters from names
def remove_vowels(root_dir):
    def remove_vowels(s):
        pattern = r'[aeiouAEIOU]'
        return re.sub(pattern, '', s)

    for root, dirs, files in os.walk(root_dir, followlinks=True):
        # Remove vowels from the directory names
        for i, dir in enumerate(dirs):
            old_name = os.path.join(root, dir)
            new_name = remove_vowels(dir)
            new_name = os.path.join(root, new_name)
            if old_name != new_name:
                try:
                    os.rename(old_name, new_name)
                except PermissionError:
                    # Handle the PermissionError here
                    print(f'PermissionError: Unable to rename {old_name}')
        # Remove vowels from the file names
        for file in files:
            old_file_path = os.path.join(root, file)
            name, ext = os.path.splitext(file)
            new_name = remove_vowels(name)
            new_file_path = os.path.join(root, new_name + ext)
            if old_file_path != new_file_path:
                try:
                    os.rename(old_file_path, new_file_path)
                except PermissionError:
                    # Handle the PermissionError here
                    print(f'PermissionError: Unable to rename {old_file_path}')

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
    for root, dirs, files in os.walk(root_dir):
        for file in files:
            if file.endswith('.wav'):
                file_path = os.path.join(root, file)
                with open(file_path, 'rb') as f:
                    # Read the RIFF header
                    riff_header = f.read(12)
                    if riff_header[:4] != b'RIFF':
                        raise ValueError('Not a RIFF file')
                    if riff_header[8:12] != b'WAVE':
                        raise ValueError('Not a WAVE file')

                    # Read the format chunk
                    fmt_chunk_header = f.read(8)
                    if fmt_chunk_header[:4] != b'fmt ':
                        raise ValueError('Not a format chunk')
                    fmt_chunk_size = struct.unpack('<I', fmt_chunk_header[4:8])[0]
                    fmt_chunk_data = f.read(fmt_chunk_size)
                    wFormatTag, nChannels, nSamplesPerSec, nAvgBytesPerSec, nBlockAlign, wBitsPerSample = struct.unpack('<HHIIHH', fmt_chunk_data[:16])

                    # Check if bit depth is greater than the target bit depth
                    if wBitsPerSample > target_bit_depth:
                        # Open a new file for writing
                        new_file_path = file_path + '_temp'
                        with wave.open(new_file_path, 'wb') as f2:
                            # Use the same parameters as the original file, except with the target bit depth
                            params = (nChannels, target_bit_depth // 8, nSamplesPerSec, 0, 'NONE', 'not compressed')
                            f2.setparams(params)
                            # Read and write the samples
                            while True:
                                sample_bytes = f.read(nBlockAlign)
                                if not sample_bytes:
                                    break
                                f2.writeframes(sample_bytes)
                        # Close the original file
                        f.close()
                        # Replace the original file with the new one
                        os.replace(new_file_path, file_path)
                        print(f'Converted {file_path} to {target_bit_depth} bits')

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
    root_dir = 'C:/Users/Jake/Desktop/Breaks'

    # Set variables
    max_name_length = 12 # Desired max length of file and folder names
    min_segment_len = 250 # Legnth of silence at beginning and end of sample required to slice silences in milliseconds
    target_bit_depth = 16 # Set desired bitdepth, M8 supports bit depths less than 32bits but 16bit is reccomended

    # Operations
    convert_to_wav(root_dir)

    check_files(root_dir)

    delete_non_wav_files(root_dir)

    remove_plural_suffixes(root_dir)

    remove_characters_from_filenames(root_dir)

    shorten_names(root_dir)

    remove_vowels(root_dir)

    truncate_names(root_dir, max_name_length)

    convert_bit_depth(root_dir, target_bit_depth)

    check_bit_depth(root_dir)

    split_and_trim_all(root_dir, min_segment_len)

    print("Done")