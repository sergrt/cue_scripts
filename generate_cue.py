import glob
import os
import sys

if __name__ == '__main__':
    if len(sys.argv) != 2:
        print("Please provide target directory")
        sys.exit(0)

    root_dir = sys.argv[1]
    # root_dir needs a trailing slash (i.e. /root/dir/)
    root_dir = os.path.normpath(root_dir)
    if root_dir[:-1] != os.sep:
        root_dir += os.sep

    print("Processing dir: {}".format(root_dir))
    generated_count = 0

    for subdir, _, _ in os.walk(root_dir):  # subdir, dirs, files
        print("Processing dir: {}".format(subdir))

        # check cue file is present
        cue_path = glob.glob(os.path.join(glob.escape(subdir), "*.cue"))
        if len(cue_path) != 0:
            print("CUE is present, skipping: {}".format(cue_path))
            continue

        playable_mask = ["*.flac", "*.ape"]
        for mask in playable_mask:
            # check cue is needed
            audio_file_paths = glob.glob(os.path.join(glob.escape(subdir), mask))
            if len(audio_file_paths) == 0:
                # print("No audio files found")
                continue

            audio_files = [os.path.basename(file) for file in audio_file_paths]
            # print("Found audio files: {}".format(audio_files))

            if len(audio_files) == 1:  # do not process single cue
                print("Only one file found, skipping")
                continue

            cue_file_name = os.path.join(subdir, os.path.basename(subdir) + "_generated.cue")
            print("No CUE file found. Creating {}".format(cue_file_name))

            encoding_value = "utf-8"
            with open(cue_file_name, 'w', encoding=encoding_value) as file:
                track_index = 1
                for audio_file in audio_files:
                    file.write('FILE "{}" WAVE\n'.format(audio_file))
                    file.write('  TRACK {} AUDIO\n'.format(track_index))
                    file.write('    INDEX 01 00:00:00\n')
                    track_index = track_index + 1
                file.write('\n')

            print("File generated")
            generated_count = generated_count + 1
            # Do not process other extensions if something generated
            break

    print("\nDone processing. Total files generated: {}".format(generated_count))
