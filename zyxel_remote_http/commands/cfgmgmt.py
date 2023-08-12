# 5898
# {'tag': <input id="XSSID" name="XSSID" type="hidden" value="3ao1Ot8FvITEhnfFkr3OhVZVDWyuxqg0"/>, 'name': 'XSSID', 'value': '3ao1Ot8FvITEhnfFkr3OhVZVDWyuxqg0', 'type': 'hidden'}
# {'tag': <input checked="" id="srcFile_1" name="srcFile" onclick="srcFileSel(this.value)" type="radio" value="1"/>, 'name': 'srcFile', 'value': '1', 'type': 'radio', 'label': 'Running configuration'}
# {'tag': <input id="srcFile_2" name="srcFile" onclick="srcFileSel(this.value)" type="radio" value="2"/>, 'name': 'srcFile', 'value': '2', 'type': 'radio', 'label': 'Startup configuration'}
# {'tag': <input id="srcFile_3" name="srcFile" onclick="srcFileSel(this.value)" type="radio" value="3"/>, 'name': 'srcFile', 'value': '3', 'type': 'radio', 'label': 'Backup configuration'}
# {'tag': <input checked="" id="dstFile_2" name="dstFile" onclick="dstFileSel(this.value)" type="radio" value="2"/>, 'name': 'dstFile', 'value': '2', 'type': 'radio', 'label': 'Startup configuration'}
# {'tag': <input id="dstFile_3" name="dstFile" onclick="dstFileSel(this.value)" type="radio" value="3"/>, 'name': 'dstFile', 'value': '3', 'type': 'radio', 'label': 'Backup configuration'}
# {'tag': <input name="cmd" type="hidden" value="5899"/>, 'name': 'cmd', 'value': '5899', 'type': 'hidden'}
# {'tag': <input class="font-btn" name="sysSubmit" type="submit" value="Apply"/>, 'name': 'sysSubmit', 'value': 'Apply', 'type': 'submit'}
# {'tag': <input class="font-btn" name="Cancel" onclick="window.location.reload();" type="reset" value="Cancel"/>, 'name': 'Cancel', 'value': 'Cancel', 'type': 'reset'}
from zyxel_remote_http.zyxel import Zyxel


BACKUP_CMD=5901
RUNNING_CONFIG=1
STARTUP_CONFIG=2
BACKUP_CONFIG=3
FLASH_LOG=6
BUFFER_LOG=7
TECH_SUPPORT=8

class Cfgmgmt():
    def add_options(self, subparser):
        subparser.add_argument('--save-running', dest='save_running',
                               help='File to write the running config (type=1) to')
        subparser.add_argument('--save-startup', dest='save_startup',
                               help='File to write the startup config (type=2) to')
        subparser.add_argument('--save-backup', dest='save_backup',
                               help='File to write the backup config (type=3) to')
        subparser.add_argument('--save-flashlog', dest='save_flashlog',
                               help='File to write the flash log (type=6) to')
        subparser.add_argument('--save-bufferlog', dest='save_bufferlog',
                               help='File to write the buffer log (type=7) to')
        subparser.add_argument('--save-tech-support', dest='save_tech_support',
                               help='File to write the tech support dump (type=8) to')

    def _backup(self, zyxel: Zyxel, backup_type, backup_file):
        # Request the backup cmd
        response = zyxel.cmd(BACKUP_CMD)

        # handle form_fields
        response.get_form().set_field("type", backup_type)
        response.get_form().set_field("upmethod", 1)

        # submit the form
        (url, data) = response.get_form().get_form_url_and_data()
        response = zyxel.post(url, data)
        response = zyxel.follow_redirect_if_present(response)

        # write out the config data
        with open(backup_file, "w", encoding="UTF-8") as file:
            print(response.http_response.text, file=file)
        print(f"wrote {backup_file}")

    def do_command(self, zyxel: Zyxel, args):
        configs={
            'save_running': RUNNING_CONFIG,
            'save_startup': STARTUP_CONFIG,
            'save_backup': BACKUP_CONFIG,
            'save_flashlog': FLASH_LOG,
            'save_bufferlog': BUFFER_LOG,
            'save_tech_support': TECH_SUPPORT,
            }

        for (args_key, backup_type) in configs.items():
            backup_file = getattr(args, args_key, None)
            if backup_file is not None:
                self._backup(zyxel, backup_type, backup_file)
