# Twitch CDN Scraper Proof-of-Concept

An incremental video-retrieval scraper for Twitch's CDN.

**This should only ever be used on your own content. I do not provide support for, condone, or approve of the use of this tool to download content you have not obtained express permission to test with.**

## What is this?
This scraper uses the fact that Twitch internally stores all VODs and Clips on their CDN using an incremental ID to simply iterate through every possible ID, downloading any videos it finds. Because Twitch doesn't delete content from their servers, you can potentially find content from banned users or content that's been deleted. This proof of concept was done on a small sample of 100 clips, the creator of which I obtained prior permission from. Please respect people's privacy.

## How does this work?
Once you specify a nine-digit ID to begin from, this scraper just iterates upwards, making calls to Twitch's CDN for a download using the Python requests module. If it finds a 403, it attempts to download in another format. If it finds a clip, it downloads it and records some information about it in a log file for later viewing.

## How can I configure it?
This scraper doesn't support command-line switches, because it's just a quick and dirty proof-of-concept. To change how it works, open the file. All the configuration options are listed right at the top.
### `increment`
- The initial clip ID that the scraper begins working from. Increments once per iteration.
- Default value: `500000000`
### `try_multiple_formats`
- The default format for clips is AT-cm|{clipID}. Other formats do exist, though they are *much* less common. This results in a more thorough search, but keep in mind this multiplies the search time by however many formats you specify. To specify different formats for clips, see [clip_formats](clip_formats).
- Default value: `False`
### `dl_files`
- The file where the scraper stores a log of attempted and successfully downloaded clips, along with the repsonse code from Twitch's CDN.
- Default value: `"clips/dl.txt"`
### `dl_log`
- The file where the scraper stores debugging and log information. Useful for debugging or seeing the raw HTTP reponses.
- Default value: `"clips/clips.log"`
### `twitch_api_authorization`
- Your personal Twitch API OAuth token. Only used for checking if a clip is still public. Not currently implemented. Don't share your OAuth token with anyone.
- Default value: `""`
### `twitch_api_client_id`
- Your personal Twitch Client-ID. Only used for checking if a clip is still public. Not currently implemented. Don't share your Client-ID with anyone.
- Default value: `""`
### `clip_formats`
- A list of formats that you'd like the downloader to attempt to retrieve from the CDN. Note that only the first one is used when `try_multiple_formats` is `False`. Each different format should have {increment} in place of the clip's id, so it can be properly incremented by the downloader.
- Default value: `[f"AT-cm%7C{increment}.mp4", f"{increment}.mp4", f"AT-cm{increment}.mp4"]`

Feel free to make any issues or pull requests with new formats or potential improvements to this code. Again, this is very much a proof-of-concept, so it isn't perfect. In the future, I'm planning to add support for VODs as well as clips, interactive user-prompting, command-line switches, download sorting based on public visibility, and more.
