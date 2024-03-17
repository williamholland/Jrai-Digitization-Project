import xml.etree.ElementTree as ET

def combine_verses(xml_file1, xml_file2):
    tree1 = ET.parse(xml_file1)
    tree2 = ET.parse(xml_file2)
    
    root1 = tree1.getroot()
    root2 = tree2.getroot()
    
    for testament1 in root1.findall('testament'):
        testament_name = testament1.get('name')
        
        # Find corresponding testament in the second XML
        testament2 = root2.find(f"testament[@name='{testament_name}']")
        if testament2 is None:
            continue
        
        # Iterate through books
        for book1 in testament1.findall('book'):
            book_name = book1.get('number')
            
            book2 = testament2.find(f"book[@number='{book_name}']")
            if book2 is None:
                continue
            
            for chapter1 in book1.findall('chapter'):
                chapter_number = chapter1.get('number')
                
                chapter2 = book2.find(f"chapter[@number='{chapter_number}']")
                if chapter2 is None:
                    continue
                
                for verse1 in chapter1.findall('verse'):
                    verse_number = verse1.get('number')
                    
                    verse2 = chapter2.find(f"verse[@number='{verse_number}']")
                    if verse2 is None:
                        continue
                    
                    # Combine matching verses and print
                    print(f"{verse2.text} @ {verse1.text}")
                    
# Example usage
combine_verses('bible/Jrai2016Bible.xml', 'bible/EnglishDarbyBible.xml')
