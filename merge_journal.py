#!/usr/bin/env python

"""
Read several "journal" files and output a merged version.

These "journal" files are files that I write as, well, a journal. They
are simple text files that follow the format:

01 May 2013
-----------

Bla bla bla

Etc

07 May 2013
-----------

Even more bla bla bla.
"""

import sys
import os
import time
from argparse import ArgumentParser, RawTextHelpFormatter as hlpfmt


class journal_reader(object):

    """Reads the entries in my journal format"""

    def __init__(self, filenames):
        self.last_line = ''
        self.entry = ''  # current entry being filled
        self.last_was_date = False  # last line was a date?

        self.entries = [e for f in filenames for e in self.get_from_file(f)]
        self.entries = sorted(set(self.entries), key=entry2time)
        # This allows to merge journals with repeated entries. If not,
        # we could just do: self.entries.sort(key=entry2time)

    def get_from_file(self, fname):
        "Generator of entries from a journal file"

        for line in open(fname):
            if self.last_was_date and line.startswith('--------'):
                # we already started a new entry, yield and start counting
                last_entry = self.entry.strip()
                if last_entry:  # can be empty, for the beginning of the file
                    yield last_entry

                self.entry = self.last_line + line
                self.last_line = ''
                continue

            parts = line.split()
            if len(parts) == 3 and parts[0].isdigit() and parts[2].isdigit():
                self.last_was_date = True
            else:
                self.last_was_date = False

            self.entry += self.last_line
            self.last_line = line

        self.entry += self.last_line
        yield self.entry.strip()

    def __str__(self):
        "Returns a string with a nice content representation of the entries"

        result = ''
        for entry in self.entries:
            lines = entry.split('\n')
            if len(lines) < 12:
                result += entry + '\n\n'
            else:
                result += '\n'.join(lines[:6]) + '\n  [...]\n' + \
                    '\n'.join(lines[-3:]) + '\n\n'
        return result

    def __getitem__(self, i):
        return self.entries[i]


def main():
    parser = ArgumentParser(description=__doc__, formatter_class=hlpfmt)
    parser.add_argument('files', metavar='FILE', nargs='+', help='journal file')
    parser.add_argument('-o', '--outfile', help='output file (- for stdout)')
    gr = parser.add_mutually_exclusive_group()
    gr.add_argument('--html', action='store_true', help='output in html format')
    gr.add_argument('--summary', action='store_true', help='output a summary')
    gr.add_argument('--dates', action='store_true', help='output dates only')
    args = parser.parse_args()

    # Check that the journal files exist
    for fname in args.files:
        if not os.path.exists(fname):
            sys.exit('Cannot find input file "%s".' % fname)

    # Output
    if not args.outfile or args.outfile == '-':
        fout = sys.stdout
    else:
        if os.path.exists(args.outfile):
            sys.exit('Output file "%s" already exists.' % args.outfile)
        fout = open(args.outfile, 'wt')

    # Process them
    journal = journal_reader(args.files)

    # Output
    if args.html:
        fout.write("""<!DOCTYPE html>
<html>
<head>
  <title>Journal</title>
  <meta charset="utf-8">
  <style>
    div.date { color: blue; font-weight: bold; }
  </style>
</head>

<body>
""")
        for entry in journal:
            fout.write(entry2html(entry))
        fout.write("""
</body>
</html>""")
    elif args.summary:
        fout.write(str(journal))  # shows a summary of all entries
    elif args.dates:
        for entry in journal:
            fout.write(entry.split('\n', 1)[0] + '\n')  # show date
    else:  # default - output in plain text
        for entry in journal:
            fout.write(entry + '\n\n\n')



month2num = {'January': 1, 'Enero': 1,
             'February': 2, 'Febrero': 2,
             'March': 3, 'Marzo': 3,
             'April': 4, 'Abril': 4,
             'May': 5, 'Mayo': 5,
             'June': 6, 'Junio': 6,
             'July': 7, 'Julio': 7,
             'August': 8, 'Agosto': 8,
             'September': 9, 'Septiembre': 9,
             'October': 10, 'Octubre': 10,
             'November': 11, 'Noviembre': 11,
             'December': 12, 'Diciembre': 12}

def entry2time(entry):
    "Get the unix time of an entry in the journal"
    day, month, year = entry.split('\n', 1)[0].split()  # 1st line is the date
    date = '%s %d %s' % (day, month2num[month], year)
    return time.mktime(time.strptime(date, '%d %m %Y'))


def entry2html(entry):
    date, _, body = entry.split('\n', 2)
    return """
<div class="entry">
<div class="date">%s</div>
<p>
%s
</p>
</div>
""" % (date, body.strip().replace('\n\n', '\n</p>\n<p>\n'))




if __name__ == '__main__':
    main()
