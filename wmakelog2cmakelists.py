import re

def remove_duplicates(seq):
    """
    Remove duplicates from the seq list and maintain the original order
    """
    seen = set()
    return [x for x in seq if not (x in seen or seen.add(x))]

def preprocess_lines(lines):
    """
    Merge multiple lines with newline characters
    """
    merged_lines = []
    current_line = ""

    for line in lines:
        stripped_line = line.strip()
        if stripped_line.endswith('\\'):
            current_line += stripped_line[:-1].strip() + ' '
        else:
            current_line += stripped_line
            merged_lines.append(current_line)
            current_line = ""

    return merged_lines

def parse_wmake_log(log_file):
    """
    There may be multiple compilation targets; distinguish between compilation and linking.
    """
    with open(log_file, 'r') as file:
        lines = file.readlines()

    # Preprocess line merging
    lines = preprocess_lines(lines)

    # Initialize data storage
    source_files = set()
    compile_options = []
    link_options = []
    link_libraries = []
    link_directories = set()
    include_directories = set()
    compile_definitions = set()
    output_file = ""
    cxx_standard = ""

    for line in lines:
        if 'g++' in line:
            # Check for C++ standard settings
            cxx_match = re.search(r'-std=c\+\+(\d+)', line)
            if cxx_match:
                cxx_standard = cxx_match.group(1)

            # Determine if it's a compile or link statement
            if '-Xlinker' in line or '-Wl,' in line:
                # Link statement
                output_file = re.search(r'-o\s+(\S+)', line).group(1)
                lib_matches = re.findall(r'-l(\S+)', line)
                for lib in lib_matches:
                    if lib not in link_libraries:
                        link_libraries.append(lib)
                link_directories.update(re.findall(r'-L(\S+)', line))

                options = re.findall(r'( -\S+)', line)
                # Handle -Xlinker options
                xlinker_options = re.findall(r'-Xlinker\s+(\S+)', line)
                link_options.append(f'-Wl,{",".join(xlinker_options)}')
            else:
                # Compile statement
                source_files.update(re.findall(r'-c\s+(\S+)\s+-o', line))
                include_directories.update(re.findall(r'-I(\S+)', line))
                compile_definitions.update(re.findall(r'-D(\S+)', line))
                options = re.findall(r'(-\S+)', line)
                exclude_prefixes = ('-I', '-D', '-o', '-c', '-std=c++')
                compile_options.extend(opt for opt in options if not any(
                    opt.startswith(prefix) for prefix in exclude_prefixes))

    # Handle specific include directories
    include_directories = {f"${{CMAKE_SOURCE_DIR}}/{dir}" if dir ==
                           'lnInclude' else dir for dir in include_directories}
    include_directories.add("${CMAKE_SOURCE_DIR}")

    objfile_split = output_file.split('/')[-1].split('.')
    objname = objfile_split[0]
    objstr = ''
    if len(objfile_split) == 1:
        objstr = f'add_executable({objname} {" ".join(source_files)})'
    elif objfile_split[1] == 'so':
        objstr = f'add_library({objname} SHARED {" ".join(source_files)})'
    elif objfile_split[1] == 'a':
        objstr = f'add_library({objname} STATIC {" ".join(source_files)})'

    # Handle the issue of link and target having the same name
    link_libraries = [lib if lib != objname else f'lib{
        lib}.so' for lib in link_libraries]

    # Create CMakeLists.txt content
    cmake_content = f"""cmake_minimum_required(VERSION 3.10)
project({output_file.split('/')[-1].split('.')[0]})
set(CMAKE_CXX_COMPILER g++)
set(CMAKE_CXX_STANDARD {cxx_standard})
set(CMAKE_EXPORT_COMPILE_COMMANDS ON)

{objstr}

target_include_directories({objname} PRIVATE {" ".join(include_directories)})
target_compile_definitions({objname} PRIVATE {" ".join(compile_definitions)})
target_compile_options({objname} PRIVATE {" ".join(remove_duplicates(compile_options))})
target_link_directories({objname} PRIVATE {" ".join(remove_duplicates(link_directories))})
target_link_libraries({objname} {" ".join(remove_duplicates(link_libraries))})
target_link_options({objname} PRIVATE {" ".join(link_options)})
"""
    return cmake_content

def write_cmake_file(content, output_filename="CMakeLists.txt"):
    with open(output_filename, 'w') as file:
        file.write(content)

if __name__=="__main__":
    # Use functions to parse the log and write CMakeLists.txt
    cmake_content = parse_wmake_log("log.wmake")
    write_cmake_file(cmake_content)
    print("CMakeLists.txt has been generated successfully.")