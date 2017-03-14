import os,shutil,sys
from subprocess import call

BAKSMALI_PATH = os.getcwd() + "/bin/baksmali.jar"
CACHE_PATH = os.getcwd() + "/cache/"

STRING_OPCODE = "const-string"
METHOD_OPCODE = ".method"
METHOD_ACCESS_TYPES = [
    "public",
    "private",
    "final",
    "native",
    "synchronized",
    "constructor",
    "static",
    "abstract",
    "synthetic",
    "protected"
]


'''
Use baksmali to disassemble the APK.
'''
def disassemble_apk(apk_path, session):
    sys.stdout.write('Disassembling APK ...\n')
    sys.stdout.flush()
    call(["java", "-jar", BAKSMALI_PATH, "d", str(apk_path), "-o", CACHE_PATH])
    process_bytecode(session)
    print_dissassemble_stats(session)

def process_bytecode(session):
    sys.stdout.write("Processing bytecode ...")
    for subdir, dirs, files in os.walk(CACHE_PATH):
        for file in files:
            full_path = os.path.join(subdir, file)
            with open(full_path, 'r') as f:
                class_name = ""
                for line in f:
                    if line.startswith(".class"):
                        class_line = line.strip("\n")
                        class_name = extract_class_name(class_line)
                        session.add_class(class_name)

                    if line.startswith(METHOD_OPCODE):
                        method_line = line.strip("\n")
                        method_name = extract_method_name(method_line)
                        session.add_method(method_name,class_name)

                    if (STRING_OPCODE in line):
                        string = extract_string(line.strip("\n"))
                        session.add_string(string,class_name)



                if class_name == "":
                    sys.stdout.write("ERR: Could not parse class name from "
                                     "%s" % full_path)


def extract_string(smali_line):
    string = smali_line.split(",")[1].replace("\"","")
    return string

def print_dissassemble_stats(session):
    print "Processed %s classes" % str(len(session.get_classes()))
    print "Processed %s methods" % str(len(session.get_methods()))
    print "Extracted %s strings" % str(len(session.get_strings()))


def extract_method_name(method_line):
    for el in method_line.split(" "):
        if el not in METHOD_ACCESS_TYPES and not el.startswith(".method"):
            print "Adding %s \n" % el
            return el

'''
Extract class name from a smali source line. Every class name is represented
as a classdescriptor that starts zith 'L' and ends with ';'.
'''
def extract_class_name(class_line):
    for el in class_line.split(" "):
        if el.startswith("L") and el.endswith(";"):
            return el

'''
Clear the cache directory.
'''
def clear_cache():
    try:
        shutil.rmtree(CACHE_PATH)
        os.makedirs(CACHE_PATH)
    except OSError:
        os.makedirs(CACHE_PATH)
