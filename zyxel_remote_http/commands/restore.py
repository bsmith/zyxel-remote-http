# 5896
# {'tag': <input id="XSSID" name="XSSID" type="hidden" value="goPxTA6eICqsK6LeN9MgzwslAhh5zEId"/>, 'name': 'XSSID', 'value': 'goPxTA6eICqsK6LeN9MgzwslAhh5zEId', 'type': 'hidden'}
# {'tag': <input checked="" id="upmethod_0" name="upmethod" onclick="restoreMethodChg()" type="radio" value="0"/>, 'name': 'upmethod', 'value': '0', 'type': 'radio', 'label': 'TFTP'}
# {'tag': <input id="upmethod_1" name="upmethod" onclick="restoreMethodChg()" type="radio" value="1"/>, 'name': 'upmethod', 'value': '1', 'type': 'radio', 'label': 'HTTP'}
# {'tag': <input id="tftp_srvip" maxlength="80" name="tftp_srvip" size="30" type="text" value=""/>, 'name': 'tftp_srvip', 'value': '', 'type': 'text'}
# {'tag': <input id="tftp_file" maxlength="128" name="tftp_file" size="30" type="text" value=""/>, 'name': 'tftp_file', 'value': '', 'type': 'text'}
# {'tag': <input class="file" id="http_file" name="http_file" onchange="Handlechange();" type="file">
# <div class="fakefile">
# <table border="0" cellpadding="0" cellspacing="0"><tr>
# <td valign="center"><input id="filename" type="text"/></td>
# <td style="padding-left:3px;" valign="center"><img id="browseImg" src="/image/btn_browse_normal.png"/> </td>
# </tr></table>
# </div>
# </input>, 'name': 'http_file', 'value': None, 'type': 'file'}
# {'tag': <input name="cmd" type="hidden" value="5897"/>, 'name': 'cmd', 'value': '5897', 'type': 'hidden'}
# {'tag': <input class="font-btn" name="sysSubmit" type="submit" value="Apply"/>, 'name': 'sysSubmit', 'value': 'Apply', 'type': 'submit'}
# {'tag': <input class="font-btn" name="Cancel" onclick="window.location.reload();" type="reset" value="Cancel"/>, 'name': 'Cancel', 'value': 'Cancel', 'type': 'reset'}
from zyxel_remote_http.zyxel import Zyxel


RESTORE_CMD=5896
HTTPUPLOADCGI="/cgi-bin/httpuploadruncfg.cgi"

class Restore():
    def add_options(self, subparser):
        subparser.add_argument('--restore-file', dest='restore_file',
                               required=True, help='File to upload to the switch as the running config')

    def _restore(self, zyxel: Zyxel, filehandle):
        # Request the restore cmd
        response = zyxel.cmd(RESTORE_CMD)

        # handle form_fields
        response.get_form().set_field("upmethod", 1) # http

        # setup the files
        files = {'http_file': ('restore.cfg', filehandle, "text/plain")}

        # submit the form
        (url, data) = response.get_form().get_form_url_and_data()
        del data['http_file'] # included in files, not data
        url = HTTPUPLOADCGI
        response = zyxel.post(url, data, files=files)

        print(response.http_response.text)

        if response.http_response.status_code == 200:
            print('ok')
        else:
            print('fail')


    def do_command(self, zyxel: Zyxel, args):
        if args.verbose:
            print(f"sending config from file {args.restore_file}")

        with open(args.restore_file, "rb") as filehandle:
            self._restore(zyxel, filehandle)
