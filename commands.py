import sublime
import sublime_plugin

class GotoNamedMark(sublime_plugin.TextCommand):
  def run(self, edit, name = 'user', unset = True, set = False, set_name = None,
    set_icon = 'dot'):

    selelctions = []
    for sel_item in self.view.sel():
      selelctions.append([sel_item.a, sel_item.b])

    regions = self.view.get_regions(name)
    if len(regions) == 0:
      return

    self.view.sel().clear()
    self.view.sel().add_all(regions)

    if unset:
      self.view.erase_regions(name)

    if len(self.view.sel()) == 1:
      self.view.show(self.view.sel()[0].a)

    if set:
      self.view.run_command('set_named_mark', {
        "name": set_name or name,
        "icon": set_icon,
        "sel": selelctions,
      })

class DeleteToNamedMark(sublime_plugin.TextCommand):
  def run(self, edit, name = 'user', reset = True):
    regions = self.view.get_regions(name)
    if len(regions) == 0:
      return

    start_sel = self.view.sel()[0]
    start = min(start_sel.a, start_sel.b)

    end_sel = regions[0]
    end = max(end_sel.a, end_sel.b)

    self.view.erase(edit, sublime.Region(start, end))

    if reset:
      self.view.erase_regions(name)

class SelectToNamedMark(sublime_plugin.TextCommand):
  def run(self, edit, name = 'user', reset = True):
    regions = self.view.get_regions(name)
    if len(regions) == 0:
      return

    start_sel = self.view.sel()[0]
    start = min(start_sel.a, start_sel.b)

    end_sel = regions[0]
    end = max(end_sel.a, end_sel.b)

    self.view.sel().clear()
    self.view.sel().add(sublime.Region(start, end))

    if reset:
      self.view.erase_regions(name)

class SetNamedMark(sublime_plugin.TextCommand):
  def run(self, edit, name = 'user', icon = 'dot', sel = None):
    regions = self.view.get_regions(name)
    without_add = False
    if len(regions) == 1 and regions[0] == self.view.sel()[0]:
      without_add = True

    self.view.erase_regions(name)

    if sel == None:
      sel = self.view.sel()
    else:
      new_sel = []
      for sel_part in sel:
        new_sel.append(sublime.Region(sel_part[0], sel_part[1]))
      sel = new_sel

    if not without_add:
      self.view.add_regions(name, sel, "?", icon, sublime.HIDDEN)

class UnsetNamedMark(sublime_plugin.TextCommand):
  def run(self, edit, names = ['user', 'user_fallback', 'mark']):
    regions = self.view.get_regions(name)
    if len(regions) == 0:
      return

    self.view.erase_regions(name)