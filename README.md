# Yandex Metrika Open Check
## Purpose
This is a Python 3 script I have made for my friend who is an online marketer in Russia. He is using it to get a competitive advantage over his compettion.

You can feed this script a huge list of URLs which will then be parsed and checked if Yandex Metrika is present. Yandex Metrika is a Russian based analytics tool similar to Google Analytics.

Then the script uses gathered Metrika IDs to find the ones that have dashboard and therefore all information about website traffic available to public.  

## How it works
You need to put `sites.txt` in the root directory with the script. 

The script will then produce 2 files:
- `results.csv` - main file that has god 
- `unprocessed.txt` - it is a temporary file that saves the list of files that haven't been processed yet. Useful when program crash due to a bug. 

## How to use it
Run `metrika.py` with Python 3 in command line. The script will pick up the rest.

## To-do
- Add an option to choose file with sites list
- Make script generate HTML with clickable links too
- Parse open dashboards for information insights