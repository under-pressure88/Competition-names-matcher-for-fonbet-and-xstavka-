from html.parser import HTMLParser
from html.entities import name2codepoint


class DefaultParser(HTMLParser):
    def handle_starttag(self, tag, attrs):
        print("Start tag:", tag)
        for attr in attrs:
            print("     attr:", attr)

    def handle_endtag(self, tag):
        print("End tag  :", tag)

    def handle_data(self, data):
        print("Data     :", data)

    def handle_comment(self, data):
        print("Comment  :", data)

    def handle_entityref(self, name):
        c = chr(name2codepoint[name])
        print("Named ent:", c)

    def handle_charref(self, name):
        if name.startswith('x'):
            c = chr(int(name[1:], 16))
        else:
            c = chr(int(name))
        print("Num ent  :", c)

    def handle_decl(self, data):
        print("Decl     :", data)
        


class DataParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.data = {'children': []}
        self.current_node = self.data
        self.current_way = [0]
        
    def handle_starttag(self, tag, attrs):
        self.current_node['children'].append({**{'tag': tag, **dict(attrs)}, 'children': []})
        self.current_way.append(len(self.current_node['children']) - 1)
        self.current_node = self.current_node['children'][-1]       
        

    def handle_endtag(self, tag):
        def getPosition(indices):
            el = self.data['children'][indices[0]]
            
            for idx in indices[1:]:
                el = el['children'][idx]
            return el
        
        self.current_way.pop()
        self.current_node = getPosition(self.current_way)

    def handle_data(self, data):
        self.current_node.update({'text': data})
        

class TableParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.dfs = []
        self.values = []
        self.cell = ''
        self.record_flag = False
        
    def handle_starttag(self, tag, attrs):
        if tag == 'tr':
            self.values.append([])
        elif tag in ('th', 'td'):
            self.record_flag = True

    def handle_endtag(self, tag):
        if tag in ('th', 'td'):
            self.record_flag = False
            self.values[-1].append(self.cell)
            self.cell = ''
            
        elif tag == 'tbody':
            columns = ['tmp'] + self.values[0]
            self.df = pd.DataFrame(self.values[1:], columns=columns) #bad moment
            if len(columns) == 16:
                self.dfs.append(self.df)
            self.values = []
            

    def handle_data(self, data):
        if self.record_flag:
            self.cell += data

    def handle_comment(self, data):
        pass
    
    def handle_entityref(self, name):
        c = chr(name2codepoint[name])
        print("Named ent:", c)

    def handle_charref(self, name):
        if name.startswith('x'):
            c = chr(int(name[1:], 16))
        else:
            c = chr(int(name))
        print("Num ent  :", c)

    def handle_decl(self, data):
        print("Decl     :", data)
        
        
    def get_data_frame(self):        
        return pd.concat(self.dfs)
    
    
    def get_data_frames(self):        
        return self.dfs
    