# Site source for inheritancetaxexplained.co.uk

The live pages are in the root of this repository (index.html, one folder per video, images/, robots.txt, sitemap.xml, llms.txt).

This folder holds the source used to build them:

- build.py: builds every page from the video data at the top of the file. Run `python3 build.py` from a folder that contains `build.py`, `data/<video>_transcript.tsv` and `static/images/<slug>.jpg`. Output goes to `out/`.
- v1_transcript.tsv, v2_transcript.tsv: the spoken words of each video, one line per caption cue, `m:ss<TAB>text`. Copy them into `data/` before building.
- Thumbnails: the images in `/images` are the `static/images` inputs.

To add a video: add an entry to VIDEOS in build.py (title, id, slug, chapters, key facts, questions and answers, LinkedIn articles), add its transcript TSV and thumbnail, run the build, then upload the new folder, the updated index.html, sitemap.xml and llms.txt to this repository.
