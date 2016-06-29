from accessory.errors import station
from accessory.sys import MainMenu
from accessory.display import Display
from collections import defaultdict
import subprocess, os, time, shutil


class HubStation(object):
    def __init__(self):
        self.MMc = MainMenu().catalog()
        self.dirTime = time.asctime(time.localtime(time.time()))

    def engine(self, message_of_the_day, test_app_root_dir='', local={}):

        local['settings'] = {
            'sys_test_root_dir': test_app_root_dir + '/Test zone',
            'sys_test_pull': '/pull',
            'user_gen_content_dir': '',
            'user_gen_saved_dir': '',
        }

        # Show menu in the terminal
        Display().reset

        if not message_of_the_day:
            message_of_the_day = station.e_catalog()[0]
        else:
            message_of_the_day = message_of_the_day

        Display().menu(self.MMc, message_of_the_day)

        # What option would the user like to select?
        approved_commands = Display().approve_user_input(self.MMc)

        # User would like to cut/sort files
        if approved_commands['nmb'] == 1:
            user_selected_option = shutil.move
        elif approved_commands['nmb'] == 2:
            user_selected_option = shutil.copy2
        else:
            user_selected_option = 0

        Display.reset()

        # Seek the files that match or requirements
        if not local['settings']['user_gen_saved_dir']:
            default_dir = local['settings']['sys_test_root_dir']
        else:
            default_dir = 'user_gen_saved_dir'

        harvested = self.gathering_list(default_dir)

        # Start sorting and building directories
        cl_list_reclusive_files = self.dict_build_listing(harvested)

        self.make_directory(local['settings'], cl_list_reclusive_files, user_selected_option)

    def make_directory(self, x, list_of_file_names, user_sel_cmd):

        directory = [x['sys_test_root_dir'] + "/" + x['sys_test_pull'], x + "/" + self.dirTime]
        print(directory)
        exit()
        WC = WriteContent()

        if WC.read_confirm_location(directory):
            WC.write_location(directory)
            WC.write_transfer_files(list_of_file_names, directory, user_sel_cmd)

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
    def gathering_list(search_defined_directory, names=[], cl_list_gather_files=[]):
        os.chdir(search_defined_directory),
        print("switched dir...%s" % os.getcwd())

        for (search_defined_directory, folder_List, file_List) in os.walk(search_defined_directory):

            # Are there files in the requested directory
            if file_List:

                for eachFile in file_List:

                    # Confirm if a file extension exist
                    if "." in eachFile:
                        search_defined_directory, y = eachFile.split('.')

                        files_dict = {y: search_defined_directory}
                        cl_list_gather_files.append(files_dict)
            else:
                print("No files are listed in that directory")

        if not cl_list_gather_files:
            exit("I'm empty and need content")

        return cl_list_gather_files


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
