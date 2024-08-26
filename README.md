# Duplicate-Media-Finder: A Robust Solution for Detecting Duplicates in Images and Videos

## Description
Duplicate Media Finder is a Python-based application designed to identify and remove duplicate images and videos from a directory or multiple directories. By leveraging cryptographic hash functions, this application efficiently scans media files, stores their checksums, and compares them across different runs, allowing for the detection of duplicates even when new files are added later.

## Features
* Image and Video Support: The program can process both images and videos to detect duplicates.
* Hash-based Comparison: The program computes cryptographic hash values to uniquely identify files, ensuring that even files with different names are detected as duplicates if their content is identical.
* Persistent Hash Storage: Hashes of previously scanned files are saved, allowing for efficient rescanning of directories to detect duplicates among newly added files.
* Excel Export: The program generates an Excel file listing original and duplicate files with their paths.
* File and Directory Support: Accepts both single file and directory inputs for flexible processing, and automatically scans the subfolders.

## Installation
1. Clone the repository
2. Install the required dependencies: <pre><code>pip install -r requirements.txt</code></pre>

## Usage
* update the directory path in the dup_finder.py and run.
* the checksums will be stored in checksums.json and duplicates if found would be stored in duplicates.xlsx
* run delete_duplicates.py to automatically delete all the found duplicates
* run compare_and_delete to visually confirm the duplicates and then delete.
* delete the duplicates.xlsx afterwards 

## Contribution
If you find any issues or have feature suggestions, feel free to open an issue or submit a pull request.
