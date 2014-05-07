__author__ = 'sakuratanoshiminaki'


#import uvent
#uvent.install()
import gevent.monkey
gevent.monkey.patch_all()

import threading
import words
import os
import os.path
# -*- coding: utf-8 -*-

###########################################################################
## Python code generated with wxFormBuilder (version Sep 12 2010)
## http://www.wxformbuilder.org/
##
## PLEASE DO "NOT" EDIT THIS FILE!
###########################################################################

import wx

###########################################################################
## Class MyFrame1
###########################################################################

class MyFrame1(wx.Frame):
    def __init__(self, parent):
        wx.Frame.__init__(self, parent, id=wx.ID_ANY, title="Wordtool", pos=wx.DefaultPosition,
                          size=wx.Size(500, 300), style=wx.DEFAULT_FRAME_STYLE | wx.TAB_TRAVERSAL)

        self.index=False
        self.shuffle=False
        self.definition=False
        self.redundancy=False

        bSizer1 = wx.BoxSizer(wx.VERTICAL)

        bSizer2 = wx.BoxSizer(wx.HORIZONTAL)

        self.m_staticText1 = wx.StaticText(self, wx.ID_ANY, "Input File:", wx.DefaultPosition, wx.DefaultSize, 0)
        self.m_staticText1.Wrap(-1)
        bSizer2.Add(self.m_staticText1, 1, wx.ALL, 5)

        self.file_path = wx.TextCtrl(self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize,
                                     wx.TE_MULTILINE|wx.TE_READONLY)
        self.file_path.Enable(False)

        bSizer2.Add(self.file_path, 4, wx.ALL, 5)

        self.browser = wx.Button(self, wx.ID_ANY, "browse", wx.DefaultPosition, wx.DefaultSize, 0)
        bSizer2.Add(self.browser, 1, wx.ALL, 5)

        bSizer1.Add(bSizer2, 1, wx.EXPAND, 5)

        bSizer3 = wx.BoxSizer(wx.HORIZONTAL)

        bSizer4 = wx.BoxSizer(wx.VERTICAL)

        self.index_chk_box = wx.CheckBox(self, wx.ID_ANY, "Index", wx.DefaultPosition, wx.DefaultSize, 0)
        bSizer4.Add(self.index_chk_box, 0, wx.ALL, 5)

        self.def_chk_box = wx.CheckBox(self, wx.ID_ANY, "Definition", wx.DefaultPosition, wx.DefaultSize, 0)
        bSizer4.Add(self.def_chk_box, 0, wx.ALL, 5)

        self.sfl_chk_box = wx.CheckBox(self, wx.ID_ANY, "Shuffle", wx.DefaultPosition, wx.DefaultSize, 0)
        bSizer4.Add(self.sfl_chk_box, 0, wx.ALL, 5)

        self.rdn_chk = wx.CheckBox( self, wx.ID_ANY, "Solve Redundancy", wx.DefaultPosition, wx.DefaultSize, 0 )
        bSizer4.Add( self.rdn_chk, 0, wx.ALL, 5 )

        bSizer3.Add(bSizer4, 1, wx.EXPAND, 5)

        bSizer5 = wx.BoxSizer(wx.VERTICAL)

        bSizer3.Add(bSizer5, 1, wx.EXPAND, 5)

        bSizer1.Add(bSizer3, 5, wx.EXPAND, 5)

        self.m_button2 = wx.Button(self, wx.ID_ANY, "Start", wx.DefaultPosition, wx.DefaultSize, 0)
        bSizer1.Add(self.m_button2, 1, wx.ALL, 5)


        self.SetSizer(bSizer1)
        self.Layout()

        self.Centre(wx.BOTH)

        # Connect Events
        self.browser.Bind(wx.EVT_BUTTON, self.on_brw_clk)
        self.index_chk_box.Bind(wx.EVT_CHECKBOX, self.on_idx_chk)
        self.def_chk_box.Bind(wx.EVT_CHECKBOX, self.on_def_chk)
        self.sfl_chk_box.Bind(wx.EVT_CHECKBOX, self.on_sfl_chk)
        self.rdn_chk.Bind( wx.EVT_CHECKBOX, self.on_rdn_chk )
        self.m_button2.Bind(wx.EVT_BUTTON, self.on_start)

    def __del__(self):
        pass


    # Virtual event handlers, overide them in your derived class
    def on_brw_clk(self, event):
        dlg = wx.FileDialog(
            self,
            "Select input files",
            os.getcwd(),
            "",
            "*.txt",
            wx.FD_OPEN | wx.FD_MULTIPLE
        )
        if dlg.ShowModal() == wx.ID_OK:
            self.paths = dlg.GetPaths()
        dlg.Destroy()
        self.file_path.Clear()
        self.file_path.AppendText("\n".join(self.paths))

    def on_idx_chk(self, event):
        self.index=event.IsChecked()

    def on_def_chk(self, event):
        self.definition=event.IsChecked()

    def on_sfl_chk(self, event):
        self.shuffle=event.IsChecked()
    def on_rdn_chk(self, event):
        self.redundancy=event.IsChecked()
    def on_start(self, event):
        window = self
        def run():
            word_list = words.load_words(*self.paths)
            word_list.set_def(self.definition)
            word_list.set_idx(self.index)
            if self.shuffle:
                word_list.shuffle()
            if self.redundancy:
                word_list.solve_redundancy()
            jobs = [gevent.spawn(word.get_definition) for word in word_list]
            gevent.joinall(jobs)
            output_dir = [os.path.dirname(os.path.abspath(path)) for path in self.paths][0]
            output = os.path.join(output_dir, "output.txt")
            with open(output, mode="wt") as f:
                f.write(repr(word_list))
                f.flush()
        t = threading.Thread(target=run)
        t.run()
class MainWindow(wx.Frame):
    def __init__(self, parent, title):
        wx.Frame.__init__(self, parent, title=title, size=(200, 100))

        self.button = wx.Button(self, label="browse")

    def btn_on_clk(self, event):
        dlg = wx.FileDialog(
            self,
            "Select input files",
            self.dirname,
            "",
            "*.txt",
            wx.FD_OPEN | wx.FD_MULTIPLE
        )
        if dlg.ShowModal() == wx.ID_OK:
            self.paths = dlg.GetPaths()
        dlg.Destroy()

app = wx.App(False)  # Create a new app, don't redirect stdout/stderr to a window.
frame = MyFrame1(None) # A Frame is a top-level window.
frame.Show(True)     # Show the frame.
app.MainLoop()