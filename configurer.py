import re

class Config:
    """
    Reads config files.
    
    config files follow the format of headers (eg. [header1]) with values underneath (eg. value1 = 1)
    config files allow comments (eg. #This is a comment) and refrences to other values under the same header (eg. value2 = <value1>*2)

    a Config object takes the comment character, refrence braces, and the equality sign. Deafults are #, <>, and = respectively
    to read a file call object.read_config(file_name)
    """
    def __init__(self, comment="#", reference="<>", equality="=:"):
        self.comment = comment #defines the character used to escape comments
        self.reference = reference #defines the pair of characters that denote refrences
        self.equality = equality #defines the characters that signify assignment

        self.references_ex = r"({}[^\>]*?{})".format(self.reference[0], self.reference[1]) #regex used to find refrences
        self.equality_ex = r"[{}]".format(self.equality) #regex used to find assignments

    @staticmethod
    def replace(str1, str2, start, end):
        """Replace the section str1[start:end] with str2

        Input:
            str1 : Outer string with the section that is replaced
            str2 : Substring to be insterted in the place of section
            start : Index of str1 to start replacement
            end : Index of str1 to end replacement
        Output: str1[:start]+str2+str1[end:]
        """
        return str1[:start]+str2+str1[end:]

    def read_section(self, section):
        """Read in a section of a config file
        Input:
            section : List form with strings of each line of the section
        Output: Dictionary with header keys and matching values
        """
        #make sure each line conatins one assignment
        for item in section:
            if sum([item.count(x) for x in self.equality]) != 1:
                raise Exception("In {}, can only have one equality symbol".format(item))
        #split each line into the value name and value assigment
        section = [re.split(self.equality_ex, item) for item in section]
        section = {item[0].strip():item[1].strip() for item in section}
        #reslove all refrences including multilelved ones
        loops = 0
        while any(re.search(self.references_ex, item) for item in section.values()):
            loops += 1
            if loops > len(section)+1:
                raise Exception("Recursion error")
            for key in section:
                match = re.search(self.references_ex, section[key])
                if match.group(0)[1:-1] in section.keys() if match else False:
                    section[key] = self.replace(section[key], section[match.group(1)[1:-1]], match.span()[0], match.span()[1])
                    if re.search(r"<{}>".format(key), section[key]):
                        raise Exception("References cannot loop")

        #turn all assigments into python data-types
        section = {key:eval(value) for key, value in section.items()}

        return section

    def read_config(self, file_name):
        #parse all the data into a string with no extra white space or comments
        self.file = file_name
        with open(file_name) as config_file:
            data = [line.strip() for line in config_file]
            #remove lines that are only whitespace
            data = [line for line in data if not re.match(r"[^\S]+", line) and len(line) > 0] 
            #group all non comment lines into one string
            data = "\n".join(line for line in data if line[0] != self.comment)

        #find headers in the file (denoted by [header name])
        headers = [*re.finditer(r"(?<![^\n])\n*\[([^{}]+)\]\n*".format(self.equality), data)] 

        if len({header.group(1) for header in headers}) != len(headers):
            raise Exception("All headers must be unique")

        #isolate each section into it's own string
        sections = {header.group(1):data[header.span()[1]:len(data) if n+1 == len(headers) else headers[n+1].span()[0]] for n, header in enumerate(headers[:])}

        #split the section into lines
        sections = {key:value.strip().split("\n") for key, value in sections.items()}

        self.config = {}
        for header in sections:
            self.config[header] = self.read_section(sections[header])

    def __getattr__(self, attr, *args):
        if attr == "config":
            raise KeyError("Must read a file before retrieving data")
        else:
            return self[attr]

    def __getitem__(self, index):
        if index in self.config.keys():
            return self.config[index]
        elif sum((list(subsection.keys()) for subsection in self.config.values()), []).count(index) == 1:
            return {key:subsection[key] for subsection in self.config.values() for key in subsection.keys()}[index]
        else:
            raise KeyError("{} not found in config file or defined more than once. Check file {}".format(repr(index), self.file))

    def __str__(self):
        return str(self.config)

    def keys(self):
        return self.config.keys()

    def items(self):
        return self.config.items()

    def clear(self):
        self.config.clear()


if __name__ == '__main__':
    con = Config()
    con.read_config("quad.config")
    print(con.keys) 
