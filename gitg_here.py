# MIT License

# Copyright (c) 2019 Mateusz

# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:

# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.


import os
import urllib
import subprocess
from gi.repository import Nautilus, GObject


class GitgHere(GObject.GObject, Nautilus.MenuProvider):
    def _gitg(self, menu, directory, *args, **kwargs):
        cmd = ['gitg'] + ["--{}".format(a) for a in args]
        for key, value in kwargs:
            cmd += ["--{}".format(key), str(value)]
        subprocess.Popen(cmd, cwd=directory)

    def _gitg_menuitem(self, name, label, directory, *args, **kwargs):
        menuitem = Nautilus.MenuItem(
            name='GitgHere::{}'.format(name), label=label,
            tip='Execute gitg', icon=''
        )
        menuitem.connect(
            'activate', self._gitg, directory, *args, **kwargs
        )
        return menuitem

    def _gitg_submenu(self, directory):
        if not directory.is_directory() or directory.get_uri_scheme() != 'file':
            return

        directory_path = urllib.unquote(directory.get_uri()[7:])
        if not os.path.exists(os.path.join(directory_path, '.git')):
            return

        submenu = Nautilus.Menu()
        submenu.append_item(self._gitg_menuitem(
            'gitg', 'gitg', directory_path
        ))
        submenu.append_item(self._gitg_menuitem(
            'gitg --all', 'gitg --all', directory_path, 'all'
        ))

        menuitem = Nautilus.MenuItem(
            name='GitgHere::gitg', label='gitg', tip='', icon=''
        )
        menuitem.set_submenu(submenu)
        return menuitem,

    def get_background_items(self, window, directory):
        return self._gitg_submenu(directory)

    def get_file_items(self, window, files):
        if len(files) != 1:
            return

        return self._gitg_submenu(files[0])
