"""
------------------------------------------------------
Collection of utilities for parsing CLI clients output
------------------------------------------------------
"""
#    Licensed under the Apache License, Version 2.0 (the "License"); you may
#    not use this file except in compliance with the License. You may obtain
#    a copy of the License at
#
#         http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#    WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#    License for the specific language governing permissions and limitations
#    under the License.

import re

import prettytable

delimiter_line = re.compile('^\+\-[\+\-]+\-\+$')


# TODO(gdyuldin): refactor after coping from tempest
def tables(output_lines):
    """Find all ascii-tables in output and parse them.

    Return list of tables parsed from cli output as dicts.
    (see OutputParser.table())
    And, if found, label key (separated line preceding the table)
    is added to each tables dict.
    """
    tables_ = []

    table_ = []
    label = None

    start = False
    header = False

    if not isinstance(output_lines, list):
        output_lines = output_lines.split('\n')

    for line in output_lines:
        if delimiter_line.match(line):
            if not start:
                start = True
            elif not header:
                # we are after head area
                header = True
            else:
                # table ends here
                start = header = None
                table_.append(line)

                parsed = table(table_)
                parsed['label'] = label
                tables_.append(parsed)

                table_ = []
                label = None
                continue
        if start:
            table_.append(line)
        else:
            if label is None:
                label = line

    return tables_


# TODO(gdyuldin): refactor after coping from tempest
def table(output_lines):
    """Parse single table from cli output.
    Return dict with list of column names in 'headers' key and
    rows in 'values' key.
    """
    table_ = {'headers': [], 'values': []}
    columns = None

    if not isinstance(output_lines, list):
        output_lines = output_lines.split('\n')

    if not output_lines[-1]:
        # skip last line if empty (just newline at the end)
        output_lines = output_lines[:-1]

    rows = []
    for line in output_lines:
        if delimiter_line.match(line):
            columns = _table_columns(line)
            continue
        if '|' not in line:
            continue
        row = []
        for col in columns:
            row.append(_get_cell(line, *col).strip())
        rows.append(row)

    # Combine multiline cells
    if len(rows[0]) == 2:
        for i in reversed(range(len(rows))):
            if not rows[i][0]:
                rows[i - 1][1] += rows[i][1]
                rows.pop(i)

    table_['headers'] = rows[0]
    table_['values'] = rows[1:]

    return table_


def _get_cell(line, start, end):
    """Returns part of line from `start` to `end` considering char block width.

    Args:
        line (str): unicode line
        start (int): start of desired part of line
        end (int): end of desired part of line

    Returns:
        str: part of string
    """
    pos = 0
    output = []

    for char in line:
        char_width = prettytable._char_block_width(ord(char))
        if pos >= end:
            break
        if pos >= start:
            output.append(char)
        pos += char_width

    return u''.join(output)


# TODO(gdyuldin): refactor after coping from tempest
def _table_columns(first_table_row):
    """Find column ranges in output line.
    Return list of tuples (start,end) for each column
    detected by plus (+) characters in delimiter line.
    """
    positions = []
    start = 1  # there is '+' at 0
    while start < len(first_table_row):
        end = first_table_row.find('+', start)
        if end == -1:
            break
        positions.append((start, end))
        start = end + 1
    return positions


# TODO(gdyuldin): refactor after coping from tempest
def listing(output_lines):
    """Return list of dicts with basic item info parsed from cli output."""

    items = []
    table_ = table(output_lines)
    for row in table_['values']:
        item = {}
        for col_idx, col_key in enumerate(table_['headers']):
            item[col_key] = row[col_idx]
        items.append(item)
    return items
