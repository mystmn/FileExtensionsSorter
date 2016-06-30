from accessory import MainMenu, Display, errors
from collections import defaultdict
from controller.content import WriteContent
import os, shutil, time


class HubStation(object):
    def __init__(self):
        self.MMc = MainMenu().catalog()
        self.dirTime = time.asctime(time.localtime(time.time()))

    def engine(self, message_of_the_day, test_app_root_dir='', local={}):

        local['settings'] = {
            'sys_test_root_dir': test_app_root_dir + '/Test zone',
            'sys_test_pull': '/pull',
            'sys_test_push': '/push',
            'user_gen_content_dir': '',
            'user_gen_saved_dir': '',
        }

        # Show menu in the terminal
        d = Display()
        d.reset

        if not message_of_the_day:
            message_of_the_day = errors.catalog()[0]
        else:
            message_of_the_day = message_of_the_day

        d.menu(self.MMc, message_of_the_day)

        # What option would the user like to select?
        approved_commands = d.approve_user_input(self.MMc)

        # User would like to cut/sort files
        if approved_commands['nmb'] == 1:
            user_selected_option = shutil.move
        elif approved_commands['nmb'] == 2:
            user_selected_option = shutil.copy2
        else:
            user_selected_option = 0

        d.reset()

        # Seek the files that match or requirements
        if not local['settings']['user_gen_saved_dir']:
            user_generated_directory = local['settings']['sys_test_root_dir'] + '/' + local['settings']['sys_test_pull']
            user_generated_saved_dir = local['settings']['sys_test_root_dir'] + '/' + local['settings']['sys_test_push']
        else:
            user_generated_directory = 'user_gen_saved_dir'

        harvested = self.gathering_list(user_generated_directory)

        # Start sorting and building directories
        cl_list_reclusive_files = self.dict_build_listing(harvested)

        self.make_directory(user_generated_directory, user_generated_saved_dir, cl_list_reclusive_files, user_selected_option)

    def make_directory(self, user_generated_directory, user_generated_saved_dir, list_of_file_names, user_sel_cmd):

        directory = [user_generated_directory, user_generated_saved_dir + "/" + self.dirTime]

        print('{}'.format(directory))

        WC = WriteContent()

        if WC.read_confirm_location(directory):
            WC.write_location(directory)
            WC.write_transfer_files(list_of_file_names, directory, user_sel_cmd)

        else:
            print('{}'.format('unable to locate directory'))

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
    def gathering_list(search_defined_directory, cl_list_gather_files=[]):
        os.chdir(search_defined_directory),
        print('{0} {1}'.format('switched dir..', os.getcwd()))

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
                print('{}'.format("No files are listed in that directory"))

        if not cl_list_gather_files:
            exit("I'm empty and need content")

        return cl_list_gather_files
