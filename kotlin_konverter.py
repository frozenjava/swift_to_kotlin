#!/usr/bin/env python3

#
# Josh Artuso
# Thursday, August 24th, 2017
# A simple script to convert plain swift objects to plain kotlin objects
# specifies gson @SerializedName and @Expose

import sys


def cap_first_letter(string_to_cap):
    """
    Capitalize the first letter of a string and leave the rest untouched.
    :param string_to_cap: The string to pop a cap in
    :return:
    """
    return ' '.join(s[0].upper() + s[1:] for s in string_to_cap.split(' '))


def un_swiftify(string_to_unswift):
    """
    Replace switch key words with the holy Kotlin key words.
    :param string_to_unswift: The string to replace stuff from
    :return:
    """
    swift_to_kotlin_dict = {
        'nil': 'null',
        'Bool': 'Boolean',
        'Decimal': 'Double',
        'Int64': 'Int'
    }

    s = string_to_unswift
    for swift_key, kotlin_value in swift_to_kotlin_dict.items():
        s = str(s).replace(swift_key, kotlin_value)
    return s


def konvert_line_to_kotlin(swift_line):
    """
    Do the conversion
    :param swift_line: The line of Swift code to convert to Kotlin.
    :return:
    """

    # If the line doesn't start with var then its something that we don't care to convert so just return.
    if swift_line and not str(swift_line).startswith('var'):
        return None

    var_name = swift_line[4:].split(':')[0]
    var_type_and_val = swift_line[(4 + len(var_name) + 2):]

    serialized_name = cap_first_letter(var_name)
    k_type = un_swiftify(var_type_and_val)

    print('@SerializedName("{}")'.format(serialized_name))
    if ": Date" in k_type:
        print("@JsonAdapter(GsonDateSerializer::class)")
    print('@Expose')
    print('var {0!s}: {1!s}'.format(var_name, k_type).strip('\n'))
    print()


def read_swift_file(path_to_swift_source):
    with open(path_to_swift_source, 'r') as f:
        for line in f.readlines():
            konvert_line_to_kotlin(line.replace('    ', ''))

if __name__ == '__main__':
    read_swift_file(sys.argv[1])
