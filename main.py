from agents import convertLine, format, convertSet
import re
from latexcompiler import LC
import os

from pathlib import Path
from pytask import mark

def replace_expressions(input_string, findicator, bindicator, convert_function=convertLine):
    input_string = str(input_string)
    pattern = re.compile(f'{re.escape(findicator)}(.*?){re.escape(bindicator)}', re.DOTALL)

    def replace(match):
        expression = match.group(1)
        replacement = convert_function(expression)
        return replacement

    result = re.sub(pattern, replace, input_string)
    return result

def purify_list(input_list):
    pattern = r'\w'
    purified_list = []
    for item in input_list:
        if re.search(pattern, item):
            purified_list.append(item)
        else:
            print("Safety Net Deployed")
            print(f"Removed '{item}' from the list as it contains no word characters.")
    return purified_list

def extract_content_between_tags(input_string):
    pattern = r'<<__remove__>>(.*?)<<__remove__>>'
    captures = re.findall(pattern, input_string, re.DOTALL)
    return captures

def full_replace(input_string, findicator, bindicator, convert_function=convertSet):
    input_string = str(input_string)
    pattern = re.compile(f'{re.escape(findicator)}(.*?){re.escape(bindicator)}', re.DOTALL)

    matches = []

    def collect_matches(match):
        expression = match.group(1)
        matches.append(expression)
        return ''

    re.sub(pattern, collect_matches, input_string)

    replacements = extract_content_between_tags(convert_function(str(matches)))
    replacements = purify_list(replacements)
    print(replacements)
    result = re.sub(pattern, lambda _: replacements.pop(0), input_string)

    return result


findicator = "<<"
bindicator = ">>"

file = """
<<The integral from 0 to 5 of sin(x)dx>>

Also this thing down here VV

<<The sum from n=0 to 4 of 1/n>>

David's expression

<<negative b plus or minus the square root of (b squared minus 4ac) all over 2a>>

We're going to go back to the Matrix

<<A matrix [[1, 2, 3] [4, 5, 6]]>>

Elder Starr's

<<e equals m c squared>>

Nathan's:

<<d dx of (x^2 + sinx plus 5e to the x minus bx)>>

This is a true statement:

<<6 in Roman Capital N>>

<<>>

"""

try:
    replaced = full_replace(file, findicator, bindicator)
except:
    print("AI failed to deliver. That dingus")
    print("Moving on to slow but consistent backup plan")
    replaced = replace_expressions(file, findicator, bindicator)
formatted = extract_content_between_tags(format(replaced))[0]
print("\n\n" + formatted)
'''doc = Document(content=formatted)
doc.generate_tex('raw.txt')
doc.generate_pdf('output.pdf', clean_tex=True)'''

path = os.getcwd()
filename = os.path.join(path, 'output.tex')

with open(filename, "w") as f:
    f.write(formatted)

# print(filename)
#
# os.system("latexmk output.tex")

'''LC.compile_document(tex_engine = 'lualatex',
                    bib_engine = 'biber', # Value is not necessary
                    no_bib = True, path = filename, # Provide the full path to the file!
                    folder_name = '.aux_files')'''