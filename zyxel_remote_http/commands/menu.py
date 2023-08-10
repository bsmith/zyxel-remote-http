# Try to download the menus starting from cmd=0

import re
from zyxel_remote_http.zyxel import Zyxel


class Menu():
    def add_options(self, _):
        # No options to set up
        pass

    def _get_menutree_cmd(self, zyxel: Zyxel):
        response = zyxel.cmd(0)

        frameset_text = response.http_response.text
        menutree_match = re.search(r'parent.menuTree.location.href="[^"]+\?cmd=([0-9]+)"', frameset_text)
        if not menutree_match:
            raise Exception("Couldn't find menuTree")
        return menutree_match.group(1)

    def _fetch_menutree(self, zyxel: Zyxel, menutree_cmd):
        cmd_data = []

        response = zyxel.cmd(menutree_cmd)
        menutree_soup = response.get_soup()
        heading_cmds = []
        for tag in menutree_soup.find_all('a', { 'href': True }):
            title = tag.string
            href_match = re.search(r'\?cmd=([0-9]+)', tag.attrs['href'])
            cmd = href_match.group(1)
            heading_cmds.append(cmd)
            cmd_data.append({'cmd': cmd, 'title': title, 'type': 'heading'})

        for cmd in heading_cmds:
            response = zyxel.cmd(cmd)
            # print(response.http_response.text)
            add_matches = re.finditer(r'd\.add\(\s*(\d+)[^\)\']*\'([^\']+)\'', response.http_response.text)
            for add_match in add_matches:
                (item_cmd, item_title) = add_match.groups()
                cmd_data.append({'cmd': item_cmd, 'title': item_title, 'type': 'item', 'heading_cmd': cmd})

        return cmd_data

    def _print_cmd_data(self, cmd_data):
        heading_titles = {}
        for cmd_datum in cmd_data:
            if cmd_datum['type'] == 'heading':
                heading_titles[cmd_datum['cmd']] = cmd_datum['title']
                print(f"** {cmd_datum['cmd']} {cmd_datum['title']} **")
            elif cmd_datum['type'] == 'item':
                heading_title = heading_titles[cmd_datum['heading_cmd']]
                print(f"{cmd_datum['cmd']:4s}  {heading_title} / {cmd_datum['title']}")
            else:
                print(cmd_datum)

    def do_command(self, zyxel: Zyxel, args):
        menutree_cmd = self._get_menutree_cmd(zyxel)
        if args.verbose:
            print("menutree_cmd =", menutree_cmd)

        cmd_data = self._fetch_menutree(zyxel, menutree_cmd)

        self._print_cmd_data(cmd_data)
