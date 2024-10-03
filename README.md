# League of Legends Gold Efficiency Spreadsheet

## About

This is a small tool built in python using the Riot Games API to pull item data. The goal is to analyze what is known as [Gold Efficiency](https://leagueoflegends.fandom.com/wiki/Gold_efficiency_(League_of_Legends)).

The tool will dynamically calculate gold efficiencies for all of the current items in the game (in the classic gamemode Summoner's Rift) and generate a CSV that can easily be imported to Excel or Google Sheets.

## Dependencies

To use this tool you will need to install Python, requests, and regex. Install Python either through the Microsoft Store or through the [official site](https://www.python.org/downloads/). 

Requests and Regex can be installed via pip:
`pip install requests`
`pip install regex`
will install both.

After installation clone the repository using `git clone https://github.com/crbknight/LOL_Item_Analyzer.git`. Then you can run `main.py` to generate a CSV file of the current League of Legends patch
## Importing to Google Sheets
After generating a CSV file using `main.py` you can import it to Google Sheets via:

`File > Import > Upload`, It is recommended to choose the option `Insert new sheet(s)` but it is not required.

## format.js
Attached is a script called `format.js` which can be used to auto format a Google Sheet. After importing the CSV a blank Google Sheet (or using an existing one) navigate to:

`Extensions > Apps Script`. Then simply copy and paste the code and run.

## Current Google Sheets
If you don't want to create a Google Sheet you may use [this one](https://docs.google.com/spreadsheets/d/17HQ759AxdWPLuvLUE7s0Bj-dD7z98aVPNpgDF0aFgRo/edit?usp=sharing) to quickly view the calculations.

The sheet is up to date as of patch **14.19.1**. 

This read.me may or may not be accurate or the Google Sheet may or may not be up to date. It is recommended to create and upkeep your own.

## General Notes
There are some shortcomings to this sheet. For one it does not take into account any passives or unique bonuses an item has. Second some of the gold efficiencies may be misleading. For example support items upgrade into far better items while only costing `400` gold, so they seem incredibly broken (from a gold efficiency point of view) but really should only be taken by supports. Mejais seems very gold innefficient however the calculations do not include the bonus AP from its stacks. etc.
