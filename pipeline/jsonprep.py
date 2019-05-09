import json
from collections import OrderedDict
from os import listdir

import xlrd

from pipeline import load_settings


def initialize_sheet(file):
    workbook = xlrd.open_workbook(file)
    sheet = workbook.sheet_by_index(0)
    return sheet


def get_significant_indices(sh):
    quant = -1
    overall = -1
    demo = -1

    try:
        quant = sh.col_values(0).index("Quantitative Summary:")
    except ValueError as e:
        print("no quantitative summary")

    try:
        overall = sh.col_values(1).index("overall rating of teaching")
    except ValueError as e:
        try:
            overall = sh.col_values(1).index("Effectiveness")
        except ValueError as e:
            print("no overall rating")

    try:
        demo = sh.col_values(0).index("Demographic Summary:") + 3
    except ValueError as e:
        print("no demographic summary")

    return [quant, overall, demo]


def get_ranges(sh):
    indices = get_significant_indices(sh)
    print(indices)
    ranges = []
    if indices[0] != -1:
        quant = indices[0]

        course = {'start': 0, 'end': quant - 2}

        ranges.append(course)

    if -1 not in indices:
        overall = indices[1]
        demo = indices[2]

        quant_summ = {'start': quant + 3, 'end': demo - 7}

        ranges += [quant_summ, overall, demo]

    print(ranges)
    return ranges


def get_course(sh, ranges):
    info_1 = OrderedDict()
    info_2 = OrderedDict()

    course_start = ranges[0]['start']
    course_end = ranges[0]['end'] + 1

    for row in range(course_start, course_start + 4):
        id = sh.cell(row, 0)
        val = sh.cell(row, 1)
        info_1[str(id.value)] = val.value

    for row in range(course_start + 4, course_end):
        id = sh.cell(row, 0)
        val = sh.cell(row, 1)
        info_2[str(id.value)] = val.value

    # Replace Responses Incl Declines with Responses in Metadata
    info_2["Responses"] = info_2["Responses Incl Declines"] - info_2["Declines"]
    rid = info_2.pop("Responses Incl Declines", None)
    return [info_1, info_2]


def collect_stats(sh, ranges):
    stats = []
    rownum_start = ranges[1]['start']
    rownum_end = ranges[1]['end'] + 1
    for rownum in range(rownum_start, rownum_end):
        data = OrderedDict()
        row_values = sh.row_values(rownum)
        data['Question-ID'] = row_values[0]
        data['Question Abbrev'] = row_values[1]
        data['Question Text'] = row_values[2]
        data['Strongly Agree (5)'] = row_values[3]
        data['Agree (4)'] = row_values[4]
        data['Neutral (3)'] = row_values[5]
        data['Disagree (2)'] = row_values[6]
        data['Strongly Disagree (1)'] = row_values[7]
        data['Not (-1)'] = row_values[8]
        data['Mean'] = row_values[9]
        data['Median'] = row_values[10]
        data['Std Dev'] = row_values[11]
        data['Response Count'] = row_values[12]
        data['Response Rate'] = row_values[13]
        if data['Question Text'] is not None and len(data['Question Text']) > 0:
            stats.append(data)

    return stats


def overall_stats(sh, ranges):
    data = OrderedDict()
    rownum = ranges[2]
    row_values = sh.row_values(rownum)
    data['Question-ID'] = row_values[0]
    data['Question Abbrev'] = row_values[1]
    data['Question Text'] = row_values[2]
    data['Almost Always Effective (5)'] = row_values[3]
    data['Usually Effective (4)'] = row_values[4]
    data['Sometimes Effective (3)'] = row_values[5]
    data['Rarely Effective (2)'] = row_values[6]
    data['Never Effective (1)'] = row_values[7]
    if row_values[9:12].count(None) == len(row_values[9:12]) or row_values[9:12].count("") == len(row_values[9:12]):
        data['Response Count'] = row_values[8]
    else:
        data['Mean'] = row_values[8]
        data['Median'] = row_values[9]
        data['Std Dev'] = row_values[10]
        data['Response Count'] = row_values[11]
        data['Response Rate'] = row_values[12]

    return data


def hours_spent(sh, ranges):
    data = OrderedDict()
    rownum = ranges[3]
    row_values = sh.row_values(rownum)
    data['Question-ID'] = row_values[0]
    data['Question Abbrev'] = row_values[1]
    data['Question Text'] = row_values[2]
    data['17-20'] = row_values[3]
    data['13-16'] = row_values[4]
    data['9-12'] = row_values[5]
    data['5-8'] = row_values[6]
    data['1-4'] = row_values[7]
    data['Response Count'] = row_values[8]

    return data


def create_json(lst):
    j = json.dumps(lst)
    # print(j)
    with open('data/testy.json', 'w') as f:
        f.write(j)

    return j


def get_single_scores(name):
    print(name)
    data_list = []
    s = initialize_sheet(name)
    ranges = get_ranges(s)
    # data = get_course(s)
    # data_list.append(data)
    data_list += get_course(s, ranges)
    if len(ranges) > 1:
        # stats = collect_stats(s)
        # data_list.append(stats)
        data_list += collect_stats(s, ranges)  # flattens info list
        overall = overall_stats(s, ranges)
        data_list.append(overall)
        hours = hours_spent(s, ranges)
        data_list.append(hours)
    return data_list


def all_xls_names():
    dl_path = load_settings()['Download']
    filenames = listdir(dl_path)
    return [filename.replace(filename, dl_path + "\\" + filename) for filename
            in filenames if filename.endswith('.xls')]


def get_all_scores():
    xls_names = all_xls_names()
    all_scores = [get_single_scores(xls_name) for xls_name in xls_names]
    return all_scores


if __name__ == "__main__":
    create_json(get_all_scores())
