#!/usr/bin/env python3
from __future__ import absolute_import
import os

from System.Text.RegularExpressions import *

from Deadline.Plugins import *
from Deadline.Jobs import *
from Deadline.Scripting import *


######################################################################
# This is the function that Deadline calls to get an instance of the
# main DeadlinePlugin class.
######################################################################
def GetDeadlinePlugin():
    return MvxSplitterPlugin()


def CleanupDeadlinePlugin(deadlinePlugin):
    deadlinePlugin.Cleanup()


######################################################################
# This is the main DeadlinePlugin class for the MvxSplitter plugin.
######################################################################
class MvxSplitterPlugin(DeadlinePlugin):

    def __init__(self):
        self.InitializeProcessCallback += self.InitializeProcess
        self.RenderExecutableCallback += self.RenderExecutable
        self.RenderArgumentCallback += self.RenderArgument

    def Cleanup(self):
        for stdoutHandler in self.StdoutHandlers:
            del stdoutHandler.HandleCallback

        del self.InitializeProcessCallback
        del self.RenderExecutableCallback
        del self.RenderArgumentCallback

    def InitializeProcess(self):
        # Set the plugin specific settings.
        self.SingleFramesOnly = False

        # Set the process specific settings.
        self.StdoutHandling = True
        self.PopupHandling = True

        # Ignore 'mvxsplitter' Pop-up dialogs
        self.AddPopupIgnorer(".*Rendering.*")
        self.AddPopupIgnorer(".*Wait.*")

    def RenderExecutable(self):
        return self.GetRenderExecutable("RenderExecutable", "MvxSplitter Render")

    def RenderArgument(self):
        arguments = self.GetPluginInfoEntry("Arguments").strip()
        arguments = arguments.replace("<QUOTE>", "\"")
        return arguments

