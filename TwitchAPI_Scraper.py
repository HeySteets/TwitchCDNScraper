import requests
import logging
import os

# The number of the first clip ID you want to try downloading. Usually 9 digits. Will increment +1 until stopped.
increment = 500000000
# Try formats of a clip other than AT-cm%7C{ID}.mp4? Turn on for a more thorough search at the cost of multiplying
# the download time by the formats. Add more formats by modifying clip_formats below. Defaults to False.
try_multiple_formats = False
# The file where you would like to store downloads and their results. Defaults to clips/dl.txt.
dl_files = "clips/dl.txt"
# The file where you would like to store debugging and log information. Defaults to clips/clips.log.
dl_log = "clips/clips.log"
# Your Twitch API Authorization. Only used for checking if a clip is public (not currently implemented).
twitch_api_authorization = ""
# Your Twitch API Client-ID. Only used for checking if a clip is public (not currently implemented).
twitch_api_client_id = ""


def clips_formats():
    global clip_formats
    clip_formats = [
        # Add different formats of clip names here, with {increment} as the number to increment.
        f"AT-cm%7C{increment}.mp4",
        f"{increment}.mp4",
        f"AT-cm{increment}.mp4"
    ]


# Sets up the clips directory so the log files can be written correctly.
if not os.path.isdir("clips"):
    os.makedirs("clips")
# Set up the logger.
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s | %(name)-23s | %(levelname)-7s | %(message)s',
                    datefmt='%m-%d-%y %H:%M:%S', filename=dl_log, filemode='a')
console = logging.StreamHandler()
console.setLevel(logging.INFO)
logFormat = logging.Formatter('%(levelname)-7s   %(message)s')
console.setFormatter(logFormat)
logging.getLogger().addHandler(console)
log = logging.getLogger('Scraper')


def get_clip():
    # Iterates through all defined clip formats.
    for count in range(len(clip_formats)):
        # If the clip isn't already in the archive, run the request.
        if clip_formats[count] not in clips_archive:
            clip_get = requests.get(f"https://clips-media-assets2.twitch.tv/{clip_formats[count]}")
            if clip_get.status_code == 200:
                log.warning(f"[{clip_get.status_code}] Successfully found clip {clip_formats[count]}")
                # If the clip doesn't already exist, create it.
                if not os.path.isfile(f"clips/{clip_formats[count]}"):
                    with open(f"clips/{clip_formats[count]}", "wb") as clip_handle:
                        clip_handle.write(clip_get.content)
                # If we get a 200, write the log and return the function - we're all set.
                with open(dl_files, "a") as dl_logfile:
                    dl_logfile.write(f"{clip_formats[count]} | {clip_get.status_code}\n")
                return
            else:
                # If we get an error (most likely a 403), print the debug log and let it iterate through.
                log.debug(f"[{clip_get.status_code}] Can't download {clip_formats[count]} with format {count}.")
            if try_multiple_formats:
                # If we can try multiple formats but we've run through all of them, log it and return the function.
                if count == len(clip_formats):
                    log.info(f"[{clip_get.status_code}] No recognized downloads for {clip_formats[count]}")
                    with open(dl_files, "a") as dl_logfile:
                        dl_logfile.write(f"{clip_formats[count]} | {clip_get.status_code}\n")
                    return
                else:
                    log.info(f"[{clip_get.status_code}] FORMAT {count} can't download {clip_formats[count]} ")
            else:
                log.info(f"[{clip_get.status_code}] Can't download {clip_formats[count]}, it may be in another format.")
                with open(dl_files, "a") as dl_logfile:
                    dl_logfile.write(f"{clip_formats[count]} | {clip_get.status_code}\n")
                return
        else:
            log.warning(f"{clip_formats[count]} already exists in download archive, skipping...")
            return


log.info("If you'd like to configure additional options, please open this script in a text editor.")
# Sort the archive file in numerical / alphabetical order.
if os.path.isfile(dl_files):
    current_lines = open(dl_files, "r").readlines()
    with open(dl_files, "w") as cleanup:
        current_lines.sort()
        for lines in current_lines:
            lines.replace("\n", "")
            cleanup.write(lines)
        log.debug(current_lines)
        log.info("Archive file sorted.")
else:
    # If the file doesn't already exist, make one.
    with open(dl_files, "w"):
        pass

# Read the current dl_files file into memory for later.
clips_archive = open(dl_files, "r").read()
# Actually begin downloading the clips. Runs 100000000 times.
for i in range(100000000):
    clips_formats()
    get_clip()
    increment += 1
