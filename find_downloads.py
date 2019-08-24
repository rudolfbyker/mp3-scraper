#!/usr/bin/env python3

from common import list_pages, sermon_pages, find_mp3, safe_title
import csv


def main():
    domain = 'https://www.desiringgod.org'
    series_url = domain + '/series/romans-the-greatest-letter-ever-written'
    idx = 0

    with open('download.list', 'w') as csvfile:
        writer = csv.DictWriter(csvfile, [
            'download_url',
            'file_name',
        ])
        for list_soup in list_pages(series_url, domain):
            for sermon_soup in sermon_pages(list_soup, domain):
                mp3_url = find_mp3(sermon_soup)
                print("Found {}".format(mp3_url))
                writer.writerow({
                    'download_url': mp3_url,
                    'file_name': "{:03d}_{}.mp3".format(
                        idx,
                        safe_title(sermon_soup.h1.string),
                    ),
                })
                idx += 1


main()
