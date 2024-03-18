import xml.etree.ElementTree as ET
import argparse
import os
import sys


def vprint(*args):
    ''' print for stderr '''

    sys.stderr.write(' '.join(args))
    sys.stderr.write('\n')


def main():
    parser = argparse.ArgumentParser(description="Combine two XML bibles for Glosbe.")

    # Arguments
    parser.add_argument("main_input", help="Path to the main XML bible file.")
    parser.add_argument("lookup_input", help="Path to the lookup XML bible file.")

    # Optional arguments
    parser.add_argument("-v", "--verbose", action="store_true", help="Enable verbose mode.")

    args = parser.parse_args()

    main_input = args.main_input
    lookup_input = args.lookup_input

    # Perform translation
    perform_translation(main_input, lookup_input, verbose=args.verbose)

    if args.verbose:
        vprint("Translation completed successfully.")


def perform_translation(main_xml, lookup_xml, verbose=False):
    tree1 = ET.parse(main_xml)
    tree2 = ET.parse(lookup_xml)
    
    root1 = tree1.getroot()
    root2 = tree2.getroot()
    
    for testament1 in root1.findall('testament'):
        if verbose:
            vprint(f"scanning testament[@name='{testament1}']")
        testament_name = testament1.get('name')
        
        # find corresponding testament in the second xml
        testament2 = root2.find(f"testament[@name='{testament_name}']")
        if testament2 is None:
            if verbose:
                vprint(f"testament[@name='{testament_name}'] not found in {lookup_xml}")
            continue
        
        # Iterate through books
        for book1 in testament1.findall('book'):
            if verbose:
                vprint(f"scanning book[@number='{book1}']")
            book_name = book1.get('number')
            
            book2 = testament2.find(f"book[@number='{book_name}']")
            if book2 is None:
                if verbose:
                    vprint(f"book[@number='{book_name}'] not found in {lookup_xml}")
                continue
            
            for chapter1 in book1.findall('chapter'):
                if verbose:
                    vprint(f"scanning chapter[@number='{chapter1}']")
                chapter_number = chapter1.get('number')
                
                chapter2 = book2.find(f"chapter[@number='{chapter_number}']")
                if chapter2 is None:
                    if verbose:
                        vprint(f"chatper[@number='{chapter_number}'] not found in {lookup_xml}")
                    continue
                
                for verse1 in chapter1.findall('verse'):
                    if verbose:
                        vprint(f"scanning verse[@number='{verse1}']")
                    verse_number = verse1.get('number')
                    
                    verse2 = chapter2.find(f"verse[@number='{verse_number}']")
                    if verse2 is None:
                        if verbose:
                            vprint(f"verse[@number='{verse_number}'] not found in {lookup_xml}")
                        continue

                    verse1_text = verse1.text.replace('\n', ' ').strip()
                    verse2_text = verse2.text.replace('\n', ' ').strip()
                    
                    # Combine matching verses and print
                    print(f"{verse2_text} @ {verse1_text}")


if __name__ == "__main__":
    main()
