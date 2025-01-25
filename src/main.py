import os
import shutil
from blocks import markdown_to_html_node


def static_to_public():
    if os.path.exists("./public"):
        shutil.rmtree("./public")
    os.mkdir("./public")
    file_to_copy = recursive_search("./static") 
    for file in file_to_copy:
        if os.path.isfile(file):
            shutil.copy(file,file.replace("./static","./public"))
        if os.path.isdir(file): 
            os.mkdir(file.replace("./static","./public"))
       
def recursive_search(folder_path):
    file_tocopy = []
    for item in os.listdir(folder_path):
        item_path = f"{folder_path}/{item}"
        if os.path.exists(item_path):
            if os.path.isfile(item_path):
                file_tocopy.append(item_path)
            else:
                file_tocopy.append(item_path)
                file_tocopy.extend(recursive_search(item_path))
    return file_tocopy

def extract_title(markdown):
    for line in markdown.split("\n"):
        if line.startswith("# "): 
            return line.replace("# ","")
    raise Exception("Title cant be found")

def generate_page(from_path, template_path, dest_path):
    if not os.path.exists(from_path):
        raise Exception(f"Invalid path: {from_path}")
    if not os.path.exists(template_path):
        raise Exception(f"Invalid path: {template_path}")
    print(f"Genereting a page from {from_path} to {dest_path} using {template_path}.")
    with open(f"{from_path}","r") as markdown:
        markdown_store = markdown.read()
    with open(f"{template_path}","r") as template:
        template_store = template.read()
    template_store = template_store.replace("{{ Content }}",markdown_to_html_node(markdown_store).to_html())
    template_store = template_store.replace("{{ Title }}",extract_title(markdown_store))
    dir_path = os.path.dirname(dest_path)
    if not os.path.exists(dir_path):
        os.makedirs(dir_path)
    with open(dest_path,"w") as html:
        html.write(template_store)

def generate_pages_recursive(dir_path_content, template_path, dest_dir_path):
    items = recursive_search(dir_path_content)
    for item in items:
        if ".md" in item:
            dest = item.replace("content",dest_dir_path)
            dest = dest.replace(".md", ".html")
            generate_page(item,template_path,dest)
        
    


def main():

    static_to_public()
    generate_pages_recursive("./content/","./template.html","./public/")

if __name__ == "__main__":
    main()
