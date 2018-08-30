import xlrd
from collections import OrderedDict
import json
import authentication as auth
from os import listdir
from multiprocessing import Pool


def initialize_sheet(file):
    workbook = xlrd.open_workbook(file)
    sheet = workbook.sheet_by_index(0)
    return sheet


def get_course(sh):
    info_1 = OrderedDict()
    info_2 = OrderedDict()
    for row in range(4):
        id = sh.cell(row, 0)
        val = sh.cell(row, 1)
        info_1[str(id.value)] = val.value

    for row in range(3):
        id = sh.cell(row + 4, 0)
        val = sh.cell(row + 4, 1)
        info_2[str(id.value)] = val.value

    # Replace Responses Incl Declines with Responses in Metadata
    info_2["Responses"] = info_2["Responses Incl Declines"] - info_2["Declines"]
    rid = info_2.pop("Responses Incl Declines", None)
    return [info_1, info_2]


def collect_stats(sh):
    stats = []
    for rownum in range(11, 40):
        data = OrderedDict()
        row_values = sh.row_values(rownum)
        data['Question-ID'] = row_values[0]
        data['Question Abbrev'] = row_values[1]
        data['Question Text'] = row_values[2]
        data['Strongly Agree (5.0)'] = row_values[3]
        data['Agree (4.0)'] = row_values[4]
        data['Neutral (3.0)'] = row_values[5]
        data['Disagree (2.0)'] = row_values[6]
        data['Strongly Disagree (1.0)'] = row_values[7]
        data['Not (-1.0)'] = row_values[8]
        data['Mean'] = row_values[9]
        data['Median'] = row_values[10]
        data['Std Dev'] = row_values[11]
        data['Response Count'] = row_values[12]
        data['Response Rate'] = row_values[13]

        stats.append(data)

    return stats


def overall_stats(sh):
    data = OrderedDict()
    row_values = sh.row_values(41)
    data['Question-ID'] = row_values[0]
    data['Question Abbrev'] = row_values[1]
    data['Question Text'] = row_values[2]
    data['Almost Always Effective (5.0)'] = row_values[3]
    data['Usually Effective (4.0)'] = row_values[4]
    data['Sometimes Effective (3.0)'] = row_values[5]
    data['Rarely Effective (2.0)'] = row_values[6]
    data['Never Effective (1.0)'] = row_values[7]
    data['Mean'] = row_values[8]
    data['Median'] = row_values[9]
    data['Std Dev'] = row_values[10]
    data['Response Count'] = row_values[11]
    data['Response Rate'] = row_values[12]

    return data


def hours_spent(sh):
    data = OrderedDict()
    row_values = sh.row_values(46)
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
    with open('data.json', 'w') as f:
        f.write(j)

    return j


def get_single_scores(name):
    data_list = []
    s = initialize_sheet(name)
    # data = get_course(s)
    # data_list.append(data)
    data_list += get_course(s)
    # stats = collect_stats(s)
    # data_list.append(stats)
    data_list += collect_stats(s)  # flattens info list
    overall = overall_stats(s)
    data_list.append(overall)
    hours = hours_spent(s)
    data_list.append(hours)
    return data_list


def all_xls_names():
    dl_path = auth.load_settings()['Download']
    filenames = listdir(dl_path)
    return [filename.replace(filename, dl_path + "\\" + filename) for filename
            in filenames if filename.endswith('.xls')]


def get_all_scores():
    xls_names = all_xls_names()
    p = Pool(4)
    all_scores = p.map(get_single_scores, xls_names)
    p.close()
    p.join()
    # all_scores = [get_single_scores(xls_name) for xls_name in xls_names]
    return all_scores


if __name__ == "__main__":
    print(get_all_scores())
