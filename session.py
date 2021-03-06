class Session(object):
    def __init__(self):
        self.apk_path = ""
        self.classes = []
        self.strings = dict()
        self.methods = dict()
        self.class_to_file = dict()

    def is_valid_session(self):
        return self.apk_path is not ""

    def set_apk_path(self, apkpath):
        self.apk_path = apkpath

    def add_class(self, class_name):
        if class_name not in self.classes:
            self.classes.append(class_name)

    def add_method(self, method_name, class_name):
        self.methods[method_name] = class_name

    def add_string(self, string, class_name):
        self.strings[string] = class_name

    def get_file(self, class_name):
        return self.class_to_file[class_name]

    def add_class_file(self, class_name, file_name):
        self.class_to_file[class_name] = file_name

    def get_methods(self):
        return self.methods

    def get_classes(self):
        return self.classes

    def get_strings(self):
        return self.strings


current_session = Session()


def get_session():
    return current_session
