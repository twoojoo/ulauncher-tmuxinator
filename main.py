from ulauncher.api.client.Extension import Extension
from ulauncher.api.client.EventListener import EventListener
from ulauncher.api.shared.event import KeywordQueryEvent, ItemEnterEvent
from ulauncher.api.shared.item.ExtensionResultItem import ExtensionResultItem
from ulauncher.api.shared.action.RenderResultListAction import RenderResultListAction
from ulauncher.api.shared.action.ExtensionCustomAction import ExtensionCustomAction

import glob
import os
import subprocess

class SublProjectsExtension(Extension):
    def __init__(self):
        super(SublProjectsExtension, self).__init__()
        self.subscribe(KeywordQueryEvent, KeywordQueryEventListener())
        self.subscribe(ItemEnterEvent, ItemEnterEventListener())

class KeywordQueryEventListener(EventListener):
    def on_event(self, event, extension):
        presets_dir = os.path.expanduser(extension.preferences['presets_dir'])
        home_dir = os.path.expanduser('~')
        presets_dir = presets_dir.replace('~', home_dir, 1)
        items = []
        
        arg = event.get_argument()
        items = []

        for name in  glob.glob(presets_dir + "/*.yml"):
            if arg and arg.lower() not in name.lower():
                continue

            name = os.path.basename(name).replace('.yml', '')

            item = ExtensionResultItem(
                icon = 'images/icon.png',
                name = name,
                description = 'Path: %s' % name,
                on_enter = ExtensionCustomAction(name)
            )
            items.append(item)

        return RenderResultListAction(items)

class ItemEnterEventListener(EventListener):
    def on_event(self, event, extension):
        name = event.get_data()
        subprocess.call(["alacritty", "-e", "bash", "-c", f"echo -e '\\e]2;$choice\\007'; tmuxinator start '{name}'\""])

if __name__ == '__main__':
    SublProjectsExtension().run()
