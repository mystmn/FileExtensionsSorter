import os
import subprocess


class SysCommands():
    def execute(var=""):
        return {
            'reset': subprocess.Popen(['reset'], stdout=subprocess.PIPE),
            'cd ': os.chdir(var),
            'ls': subprocess.Popen(['ls'], stdout=subprocess.PIPE),

        }
        # p.stdout.close()
        # p.wait()


class MainMenu():
    @staticmethod
    def catalog():
        # nmb = menu selector
        # mes = Message of display
        # com = command to be executed
        return [
            {
                # Consider this a header Message #
                'nmb': 0,
                'Mes': "Please select your scan option",
                'com': "Thank you",
            },
            {
                'nmb': 1,
                'Mes': "Cut/Sort all files",
                'com': [
                    "jpg",
                    "html",
                    "doc",
                    "bimp",
                ]
            },
            {
                'nmb': 2,
                'Mes': "Copy/Sort all files",
                'com': [
                    "jpg",
                    "html",
                    "doc",
                    "bimp",
                    "png",
                ]
            },
            {
                'nmb': 3,
                'Mes': "Find OS System",
                'com': "Fire the engines"
            }
        ]
