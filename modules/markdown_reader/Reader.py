from pathlib import Path

class Md_reader:

# instance attributes
    def __init__(self):
        self.markdown_path = Path("./markdown").resolve().as_posix()
        self.content_list = []

    # instance method
    def get_full_path(self):
        return str(self.markdown_path)
    
    def read_a_single_file(self, passed_route):
        content = ""
        with open(passed_route,"r") as f:
            lines = f.readlines()
            for line in lines:
                content += line
        return content

    def get_md_contents(self):
        try:
            path = self.get_full_path()
            md_files = Path(path).rglob("*.md")
            for md_file in md_files:
                file_name = md_file.resolve().name
                file_route = md_file.resolve().as_posix()
                file_content = self.read_a_single_file(file_route)
                ob = {
                "file_name":file_name,
                "file_route":file_route,
                "file_content":file_content   
                }
                self.content_list.append(ob)
            return self.content_list
        except Exception as e:
            print(f"Exception: {e}")