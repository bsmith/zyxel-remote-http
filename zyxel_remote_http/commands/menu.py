# Try to download the menus starting from cmd=0

import re
from zyxel_remote_http.zyxel import Zyxel


class Menu():
    def add_options(self, subparser):
        # No options to set up
        pass

    def do_command(self, zyxel: Zyxel, args):
        response = zyxel.cmd(0)

        frameset_text = response.http_response.text
        menutree_match = re.search(r'parent.menuTree.location.href="[^"]+\?cmd=([0-9]+)"', frameset_text)
        if (not menutree_match):
            return
        menutree_cmd = menutree_match.group(1)
        if args.verbose:
            print("menutree_cmd =", menutree_cmd)

        cmd_data = []

        response = zyxel.cmd(menutree_cmd)
        menutree_soup = response.get_soup()
        heading_titles = {}
        heading_cmds = []
        for tag in menutree_soup.find_all('a', { 'href': True }):
            title = tag.string
            href_match = re.search(r'\?cmd=([0-9]+)', tag.attrs['href'])
            cmd = href_match.group(1)
            heading_cmds.append(cmd)
            heading_titles[cmd] = title
            cmd_data.append({'cmd': cmd, 'title': title, 'type': 'heading'})

        for cmd in heading_cmds:
            response = zyxel.cmd(cmd)
            # print(response.http_response.text)
            add_matches = re.finditer(r'd\.add\(\s*(\d+)[^\)\']*\'([^\']+)\'', response.http_response.text)
            for m in add_matches:
                (item_cmd, item_title) = m.groups()
                cmd_data.append({'cmd': item_cmd, 'title': item_title, 'type': 'item', 'heading_cmd': cmd})

        for cmd_datum in cmd_data:
            if cmd_datum['type'] == 'heading':
                print("** %s %s **" % (cmd_datum['cmd'], cmd_datum['title']))
            elif cmd_datum['type'] == 'item':
                heading_title = heading_titles[cmd_datum['heading_cmd']]
                print("%4s  %s / %s" % (cmd_datum['cmd'], heading_title, cmd_datum['title']))
            else:
                print(cmd_datum)