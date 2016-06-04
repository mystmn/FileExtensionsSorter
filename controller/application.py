from accessory.errors import station
from accessory.sys import MainMenu
from collections import defaultdict
import subprocess, os, time, shutil


class HubStation(object):
    def __init__(self):
        self.MMc = MainMenu().catalog()
        self.dirTime = time.asctime(time.localtime(time.time()))

    def engine(self, message_of_the_day, app_root_dir=''):

        s = [
            app_root_dir + '/test',
        ]

        # Show menu in the terminal
        Display().reset

        if not message_of_the_day:
            message_of_the_day = station.e_catalog()[0]
        else:
            message_of_the_day = message_of_the_day

        Display().menu(self.MMc, message_of_the_day)

        # What option would the user like to select?
        approved_commands = Display().approve_user_input(self.MMc)

        Display.reset()

        # Start sorting and building directories
        l = self.dict_build_listing(self.seek_find(s[0]))

        self.make_directory(s[0], l)

    def make_directory(self, app_root_dir, list_of_file_names):

        directory = [app_root_dir, app_root_dir + "/" + self.dirTime]
        WC = WriteContent()

        if WC.read_confirm_location(directory):
            WC.write_location(directory)
            WC.write_transfer_files(list_of_file_names, directory)

        else:
            print("unable to locate directory")

    @staticmethod
    def dict_build_listing(classify, fL=defaultdict(list)):

        for each in classify:
            for key, value in each.items():
                fL[key].append(value)

        return fL

    @staticmethod
    def compare_user_path_to_sys_dict(listing, sys_input, files_validated=[], file_extensions=[]):

        for key in listing:
            for fileName, fileFormat in key.items():  # fileName . fileFormat
                for a in sys_input['com']:
                    if a in fileFormat:
                        file_approved = "%s.%s" % (fileName, fileFormat)
                        files_validated.append(file_approved)
                        file_extensions.append(a)

        # Set returns unique names
        return set(file_extensions), set(files_validated)

    @staticmethod
    def seek_find(x, names=[], files_list=[]):
        os.chdir(x),

        for (x, dir_names, f_names) in os.walk(x):
            names.extend(f_names)

            if f_names:  # If list not empty
                for eachF in names:
                    # Confirm if a file extension exist
                    if "." in eachF:
                        x, y = eachF.split('.')

                        files_dict = {y: x}
                        files_list.append(files_dict)
        return files_list


class WriteContent(object):
    @staticmethod
    def write_transfer_files(read_file_list, directory):

        if isinstance(read_file_list, dict):
            s = "/"

            for extensions, titles in read_file_list.items():
                os.makedirs(extensions)
                print("made directories ../%s " % extensions)

                for per_title in titles:
                    shutil.move(directory[0] + s + per_title + '.' + extensions,
                                directory[1] + s + extensions + s + per_title + '.' + extensions)
        else:
            print("array type isn't dict{} \nPausing app...")

    @staticmethod
    def read_confirm_location(x):
        if not os.path.exists(x[1]):
            print("Top tier folder doesn't exist..let's create one")
            return True
        else:
            return False

    @staticmethod
    def write_location(x):
        os.makedirs(x[1])
        os.chdir(x[1])
        print("%s has been created" % x[1])


class Display(object):
    @staticmethod
    def menu(list_options, x, display_list=[]):

        for y in list_options[1:]:
            display_list.append(("%s) %s" % (y['nmb'], y['Mes'])))

        i = "*" * 4
        print("%s %s %s" % (i, x, i))
        print(list_options[0]['Mes'])

        for each_line in display_list:
            print("%s" % each_line)

    def approve_user_input(self, list_options):

        try:
            x = int(input("Please Select > "))

            for each in MainMenu().catalog()[1:]:  # 0 is a Header Message

                if x is each['nmb']:
                    return list_options[x]

            print(station.e_catalog()[1])
            return self.approve_user_input(list_options)

        except ValueError:
            print(station.e_catalog()[2])
            return self.approve_user_input(list_options)

    @staticmethod
    def reset():
        p = subprocess.Popen(['reset'], stdout=subprocess.PIPE)
        p.stdout.close()
        p.wait()
