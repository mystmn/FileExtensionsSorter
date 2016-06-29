class WriteContent(object):
    @staticmethod
    def write_transfer_files(read_file_list, directory, user_sel_cmd, s="/"):

        if isinstance(read_file_list, dict):

            for extensions, titles in read_file_list.items():
                os.makedirs(extensions)
                print("made directories ../%s " % extensions)

                for per_title in titles:
                    user_sel_cmd(directory[0] + s + per_title + '.' + extensions,
                                 directory[1] + s + extensions + s + per_title + '.' + extensions)
        else:
            print("array type isn't dict{} \nPausing app...")

    @staticmethod
    def read_confirm_location(x):
        if not os.path.exists(x[1]):
            return True
        else:
            return False

    @staticmethod
    def write_location(x):
        os.makedirs(x[1])
        os.chdir(x[1])
        print("'%s' has been created" % x[1])

