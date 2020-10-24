# SRT SUBTITLE AD REMOVER

**Version: 1.0.0**

_Created by Michaël Soetaert_

## Description

This small python script allows you to remove ads from subtitles. This script will go over each line 
in an SRT file and will check against a list of predefined ad identifiers. If a line contains any 
of those ad identifiers, the full subtitle block (meaning all the data needed to display the subtitle, 
including the timestamps) will be removed from the file. 

If an ad isn't being recognized by the script, you can simply add the identifier to the list 
of predefined ad identifiers and it will be deleted when you run the script.

## Preperation

- Install `python3`.
- The following packages are required:
  - requests _(Install with `pip3 install requests`)_
  - sys _(Should be available by default)_
  - glob _(Should be available by default)_
  - os _(Should be available by default)_

## USAGE
 
#### Single file  
_**Syntax**_  
`python srtAdRemover.py "[[PATH-TO-SRT-SUBTITLE-FILE]]"`  

_**Example**_  
`python srtAdRemover.py "/Series/How I Met Your Mother/Season 5/How I Met Your Mother - S05E02.en.srt"`  

#### Bulk  
_**Syntax**_  
`python srtAdRemover.py bulk "[[PATH-TO-FOLDER]]"`  

_**Example**_  
`python srtAdRemover.py "/Series/How I Met Your Mother"`  
`python srtAdRemover.py "/Series/How I Met Your Mother/Season 5"`  

## BAZARR

You can use this script together with Bazarr:
- In your Bazarr instance, navigate to `Settings` > `Subtitles`
- Check `Use Custom Post-Processing`
- Add the following command to `Post-processing command:  
`python [[PATH-TO-THIS-SCRIPT]]/srt-ad-remover.py "{{subtitles}}"`