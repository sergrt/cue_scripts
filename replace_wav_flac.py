import chardet  # chardet2 should be installed
from collections import namedtuple
import glob
import os
import re
import sys


# case-insensitive replace
def replace_all(pattern, repl, string) -> str:
    occurences = re.findall(pattern, string, re.IGNORECASE)
    for occurence in occurences:
        string = string.replace(occurence, repl)
    return string


if __name__ == '__main__':
    if len(sys.argv) != 2:
        print("Please provide target directory")
        sys.exit(0)

    root_dir = sys.argv[1];
    # root_dir needs a trailing slash (i.e. /root/dir/)
    root_dir = os.path.normpath(root_dir)
    if root_dir[:-1] != os.sep:
        root_dir += os.sep

    print("Processing dir: {}".format(root_dir))
    # root_dir = "d:/Music_really_need/Hard Rock, Heavy Metal, Power, Instrumental/Toundra/"
    # root_dir = "d:/Music/"
    error_filenames = []
    ErrorInfo = namedtuple("ErrorInfo", ["filename", "error_text"])

    wav_str = ".wav"
    wav_regex = "\\.wav"
    flac_str = ".flac"
    files_checked = 0
    files_processed = 0
    for filename in glob.iglob(root_dir + '**/*.cue', recursive=True):
        print("Processing file: {}".format(filename))
        files_checked += 1
        # Read in the file
        try:
            encoding_value = None
            try:
                with open(filename, 'r') as file:
                    file.read()
            except:
                print("Trying to guess encoding... ", end='')
                detect = lambda url: chardet.detect(open(filename, 'rb').read())
                encoding = detect(filename)
                print(encoding)
                encoding_value = detect(filename)['encoding']

            # with open(filename, 'r', encoding=encoding_str) as file:
            with open(filename, 'r', encoding=encoding_value) as file:
                filedata = file.read()
                print("Check if file has '.wav'... ", end='')
                if filedata.find(wav_str) == -1:
                    print("No")
                else:
                    print("Yes")

                    backup_filename = filename + "_wav"
                    print("Save backup as {}".format(backup_filename))
                    with open(backup_filename, 'w') as backup_file:
                        backup_file.write(filedata)

                    # Replace the target string
                    print("Replace {} to {}".format(wav_regex, flac_str))
                    filedata = replace_all(wav_regex, flac_str, filedata)

                    # Write the file out again
                    print("Save updated file")
                    with open(filename, 'w') as file:
                        file.write(filedata)

                    files_processed += 1
        except Exception as e:
            error_filenames += ErrorInfo(filename, str(e))

    print("Finished. Files checked: {}, files processed: {}, errors: {}".format(files_checked, files_processed,
                                                                                len(error_filenames)))

    if len(error_filenames) != 0:
        print("-------------------------------------------")
        print("Following files were processed with errors:")
        for f in error_filenames:
            print(f)
