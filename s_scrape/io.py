import pickle


class IO():

    @staticmethod
    def save_list(fname, list_name):
        with open(fname,'w') as f:
            for l in list_name:
                f.write("%s\n" % l)

    @staticmethod
    def load_list(fname):
        loaded = []
        with open(fname,'r') as f:
            for line in f:
                loaded.append(line)
        return loaded

    @staticmethod
    def pickle_dump(fname,objname):
        with open(fname, 'wb') as f:
            pickle.dump(objname, f)

    @staticmethod
    def pickle_load(fname):
        with open(fname, 'rb') as f:
            return pickle.load(f)

    @staticmethod
    def flatten_list(inp_list):
        return_list = []
        for sublist in inp_list:
            for item in sublist:
                return_list.append(item)
        return return_list
