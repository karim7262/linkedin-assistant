# LinkedIn scraper for job offers 

[![made-with-python](https://img.shields.io/badge/Made%20with-Python-1f425f.svg)](https://www.python.org/)
[![PyPI license](https://img.shields.io/pypi/l/ansicolortags.svg)](https://opensource.org/licenses/MIT)
[![Maintenance](https://img.shields.io/badge/Maintained%3F-yes-green.svg)](https://github.com/twardzikf/linkedin-jobs-scraper/graphs/commit-activity)

## Description

This project implements a web scraper for LinkedIn. Its purpose is to scrape links to job postings from last week,  including words/phrases given as an input parameter.

## Configuration

All relevant paramenters can be adjusted in query.json file with following fields:

- *username*: username of a linkedin account (job search can be only performed if youa re logged in)
- *password*: password for the account
- *position*: first text field in the search bar in linkedin.com/jobs
- *location* second text field in the search bar
- *content-serch*: text to be search for in the content of job posting

**Libraries used: [Selenium](https://selenium-python.readthedocs.io/)**


