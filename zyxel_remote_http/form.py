from bs4 import Tag


class Form():
    html_form: Tag
    inputs: list
    
    def __init__(self, html_form):
        self.html_form = html_form
        self.inputs = []
        self.set_fields = {}
        self._parse_form()
    
    def _parse_form(self):
        self.method = self.html_form.attrs['method']
        self.form_action = self.html_form.attrs['action']
        for tag in self.html_form.find_all(attrs={'name': True}):
            # print(tag.prettify())
            input_type = tag.attrs['type'] if tag.name == 'input' else tag.name
            data = {
                'tag': tag,
                'name': tag.attrs['name'],
                'value': tag.attrs['value'] if 'value' in tag.attrs else None,
                'type': input_type,
            }
            if input_type == 'textarea':
                data['value'] = ''.join(tag.strings)
            if 'id' in tag.attrs:
                label_tag = self.html_form.find('label', attrs={'for': tag.attrs['id']})
                if label_tag:
                    data['label'] = ' '.join(label_tag.stripped_strings)
            self.inputs.append(data)
    
    def get_field(self, field_name):
        if field_name in self.set_fields:
            return self.set_fields[field_name]
        for input in self.inputs:
            if input['name'] == field_name:
                return input['value']
        return None
        
    def set_field(self, field_name, field_value):
        self.set_fields[field_name] = field_value

    def print_form(self):
        for input in self.inputs:
            print(input)
    
    def get_form_url_and_data(self):
        data = {}
        types_to_skip = frozenset(['reset'])
        for input in self.inputs:
            if input['type'] not in types_to_skip:
                data[input['name']] = input['value']
        for key, value in self.set_fields.items():
            data[key] = value
        return (self.form_action, data)