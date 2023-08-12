from zyxel_remote_http.zyxel import Zyxel


BACKUP_CMD=5901
RUNNING_CONFIG=1
STARTUP_CONFIG=2
BACKUP_CONFIG=3
FLASH_LOG=6
BUFFER_LOG=7
TECH_SUPPORT=8

class Backup():
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
