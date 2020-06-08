Parser is a simple scrypt that provides an ability to find web element on html page regardless it's minor changes.
# Usage 
python parser.py <source_file> <target_file> <element_id>(optional)

Target element is defined by match of class, href attribute, similarity of title and similarity of text. Each parameter contributes 25% to general match score.
