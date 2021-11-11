import os

if __name__ == "__main__":

    basedir = os.path.abspath(os.path.dirname(__file__))

    compilecmd = "sass.cmd {} {}".format(os.path.join(basedir, 'material-dashboard.scss'),
                                         os.path.join(basedir, '../css/material-dashboard.css'))
    os.system(compilecmd)
