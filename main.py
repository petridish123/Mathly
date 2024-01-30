from agents import convertLine, format, convertSet, Center
import re
import sys, os
from pdflatex import PDFLaTeX


out = None

def replace_expressions(center, input_string, findicator, bindicator, convert_function=convertLine):
    input_string = str(input_string)
    pattern = re.compile(f'{re.escape(findicator)}(.*?){re.escape(bindicator)}', re.DOTALL)

    def replace(match):
        expression = match.group(1)
        replacement = convert_function(center, expression)
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

def full_replace(center, input_string, findicator, bindicator, convert_function=convertSet):
    input_string = str(input_string)
    pattern = re.compile(f'{re.escape(findicator)}(.*?){re.escape(bindicator)}', re.DOTALL)

    matches = []

    def collect_matches(match):
        expression = match.group(1)
        matches.append(expression)
        return ''

    re.sub(pattern, collect_matches, input_string)

    replacements = extract_content_between_tags(convert_function(center, str(matches)))
    replacements = purify_list(replacements)
    print(replacements)
    result = re.sub(pattern, lambda _: replacements.pop(0), input_string)

    return result

def output(out):
    # Output the file
    with open("output.tex", "w") as f:
        f.write(out)

    pdf = os.system('pdflatex output.tex')

    # TODO: I'M WORKING ON THIS CODE VVV
    # TODO: THIS CODE VVV IS BASURA. THAT CODE ^^^ IS FANTASTIC
    '''# Load the license
    license = pdf.License()
    license.set_license("Aspose.Total.lic")

    # Create TeXLoadOptions class object
    options = pdf.TeXLoadOptions()

    # Create a Document class object
    document = pdf.Document("output.tex", options)

    # Convert Latex to PDF
    document.save("output.pdf")

    print("Latex to PDF Converted Successfully")'''
    return out

def run(center, file, findicator="<<", bindicator=">>"):
    try:
        replaced = full_replace(center, file, findicator, bindicator)
    except:
        print("AI failed to deliver. That dingus")
        print("Moving on to slow but consistent backup plan")
        replaced = replace_expressions(center, file, findicator, bindicator)

    formatted = extract_content_between_tags(format(center, replaced))[0]
    print("\n\n" + formatted)

    return formatted

file = """

<<
sqrt (9584 / x^3)
>>

Dr. Jones was saying that in order to integrate by parts the formula goes as follows: 

<<integral of udv equals uv - integral of vdu>>
<<pv = nrt>>

"""

def error():
    print("Invalid arguments: Should be: Operation, text")
    print("-s: Standard, text is document to be formatted")
    print("-f: Feedback, calls program again to reformat already outputted doc")
    print("-t: Read File, passes in .txt file, text in file will be formatted")
    raise TypeError

if len(sys.argv) > 2:
    if sys.argv[1] == "-s" or sys.argv[1] == "-t":
        if sys.argv[2] != "__OVERWRITE__":
            if sys.argv[1] == "-s":
                file = sys.argv[2]
            else:
                with open(sys.argv[2], "r") as f:
                    file = f.read()
        center = Center()
        center.create_threads()
        out = run(center, file)
    elif sys.argv[1] == "-f":
        feedback = sys.argv[2]
        out = None
        center = Center()
        if feedback.strip():
            formatted = extract_content_between_tags(
                format(center, f"{feedback} \n Also, make sure you put the output in <<__remove__>> tags still"))[0]
            print("\n\n" + formatted)
            out = formatted



    else:
        error()
else:
    error()


'''doc = Document(content=formatted)
doc.generate_tex('raw.txt')
doc.generate_pdf('output.pdf', clean_tex=True)'''

# path = os.getcwd()

# filename = os.path.join(path, 'output.tex')

"""while True:
    with open(filename, "w") as f:
        f.write(formatted)

    feedback = input("Do you have any feedback, clarification, or suggestions? ")
    if feedback.strip():
        formatted = extract_content_between_tags(format(f"{feedback} \n Also, make sure you put the output in <<__remove__>> tags still"))[0]
        print("\n\n" + formatted)

    else:
        break"""

# print(filename)
#
# os.system("latexmk output.tex")

'''LC.compile_document(tex_engine = 'lualatex',
                    bib_engine = 'biber', # Value is not necessary
                    no_bib = True, path = filename, # Provide the full path to the file!
                    folder_name = '.aux_files')'''

if __name__ == "__main__":
    output(out)
