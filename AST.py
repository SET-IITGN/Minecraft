import ast
import extract_lines
from tree_sitter import Language, Parser

Language.build_library(
  # Store the library in the `build` directory
  './build/my-languages.so',

  # Include one or more languages
  [
    './build/tree-sitter-c/',
    './build/tree-sitter-java/',
    './build/tree-sitter-cpp/',
    './build/tree-sitter-python/'
  ]
)

JAVA_LANGUAGE = Language('./build/my-languages.so', 'java')
CPP_LANGUAGE = Language('./build/my-languages.so', 'cpp')
C_LANGUAGE = Language('./build/my-languages.so', 'c')
PY_LANGUAGE = Language('./build/my-languages.so', 'python')

py_parser, cpp_parser, c_parser, jave_parser = Parser(), Parser(), Parser(), Parser()
py_parser.set_language(PY_LANGUAGE)
cpp_parser.set_language(CPP_LANGUAGE)
c_parser.set_language(C_LANGUAGE)
jave_parser.set_language(JAVA_LANGUAGE)


def helper(tree, line_number):
    children = tree.child_count
    # print(children)
    # print('first',tree.named_children)
    if tree.type == 'function_definition' or tree.type == 'method_declaration':
        return tree
    for child in range(children):
        # print('second',child, tree.children[child].type)
        if tree.children[child].start_point[0]<=line_number<=tree.children[child].end_point[0]:
            # print('third',tree.children[child].type)
            return helper(tree.children[child], line_number)
    
    
# start_line = 5
# end_line = 10
# output = []
def traverse_outside_fun(node,line_number, source_code):

    start_line = line_number - 5
    if start_line < 0:
        start_line = 0
    end_line = line_number + 5
    if end_line > len(source_code):
        end_line = len(source_code)
    for line_no in range(start_line, end_line):
        source_code[line_no] = str(line_no+1) + ' ' +source_code[line_no]
    return source_code[start_line:end_line]

def traverse_inside_fun(start_line, end_line, source_code):
    start_line = start_line - 3
    if start_line < 0:
        start_line = 0
    end_line = end_line + 3
    if end_line > len(source_code):
        end_line = len(source_code)
    for line_no in range(start_line, end_line):
        source_code[line_no] = str(line_no+1) + ' ' +source_code[line_no]
    return source_code[start_line:end_line]




def extract_function_by_line(file_path, line_number):
    
    with open(file_path, 'r') as file:
        source_code = file.readlines()

    if file_path.endswith('.py'):
        parser = py_parser
    elif file_path.endswith('.cpp'):
        parser = cpp_parser
    elif file_path.endswith('.c'):
        parser = c_parser
    elif file_path.endswith('.java'):
        parser = jave_parser

    tree = parser.parse(''.join(source_code).encode())
    function_node = helper(tree.root_node, line_number-1)
    # print(function_node)
    if function_node is None:
        function_node = traverse_outside_fun(tree.root_node, line_number-1, source_code)
        return ''.join(function_node)
    
    start_line = function_node.start_point[0]
    end_line = function_node.end_point[0]
    function_body = traverse_inside_fun(start_line, end_line, source_code)
    return ''.join(function_body)
    
    
    

# function_name, function_body = extract_function_by_line_number('/home/saikrishna/Documents/pyVulEvo/ASE/2023/geocoder/geocoder/__init__.py',11)
# print(function_name)
# print(function_body)
#print(extract_function_body('/home/saikrishna/Documents/pyVulEvo/ASE/2023/geocoder/prev/geocoder/__init__.py', 'google'))
# print(extract_function_by_line('/home/saikrishna/Downloads/__init__.py',31))