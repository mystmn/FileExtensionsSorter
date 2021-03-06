from accessory import MainMenu, errors
import subprocess


class Display(object):
    @staticmethod
    def menu(list_options, x, display_list=[]):

        for y in list_options[1:]:
            display_list.append(("%s) %s" % (y['nmb'], y['Mes'])))

        i = "*" * 4
        print('{0}, {1}, {2}'.format(i, x, i))
        print('{}'.format(list_options[0]['Mes']))

        for each_line in display_list:
            print('{}'.format(each_line))

    def approve_user_input(self, list_options):

        try:
            x = int(input("Please Select > "))

            for each in MainMenu().catalog()[1:]:  # 0 is a Header Message

                if x is each['nmb']:
                    return list_options[x]

            print('{}'.format(errors.catalog()[1]))

            return self.approve_user_input(list_options)

        except ValueError:
            print('{}'.format(errors.catalog()[2]))
            return self.approve_user_input(list_options)

    @staticmethod
    def reset():
        p = subprocess.Popen(['reset'], stdout=subprocess.PIPE)
        p.stdout.close()
        p.wait()


if __name__ == "__main__":
    pass
