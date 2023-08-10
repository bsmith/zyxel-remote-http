from argparse import ArgumentParser
import sys

from zyxel_remote_http.zyxel import Zyxel


class Cmd():
    def __init__(self):
        pass

    def add_options(self, subparser: ArgumentParser):
        subparser.add_argument('--cmd', '-c', dest='cmd',
                            required=True, help='cmd')
        subparser.add_argument('--dump-html', dest='dump_html', action='store_true',
                                help='Dump the HTML of the page.')
        subparser.add_argument('--extract-table', '--extract-tables', dest='extract_table', action='store_true',
                                help='Extract a table of information.')
        subparser.add_argument('--show-form', dest='show_form', action="store_true",
                            help='Extract and show any form on the returned page.')
        subparser.add_argument('--form-field', dest='form_fields', action="append",
                            help='Fill in a form field, key=value.')
        subparser.add_argument('--submit-form', dest='submit_form', action="store_true",
                            help='Submit the form on the returned page.')
        subparser.add_argument('--save-response', dest='save_response',
                                help='File to save the final response to.')

    def do_command(self, zyxel: Zyxel, args):
        # Request the given cmd
        response = zyxel.cmd(args.cmd)

        # dump the html
        if args.dump_html:
            print(response.http_response.text)

        # extract a table
        if args.extract_table:
            dataset = response.extract_table()
            for row in dataset:
                print(row)

        # show the form
        if args.show_form:
            response.get_form().print_form()

        # handle form_fields
        if args.form_fields:
            for field in args.form_fields:
                if args.verbose:
                    print("form-field:", field.split('='), file=sys.stderr)
                [field_name, field_value] = field.split('=')
                response.get_form().set_field(field_name, field_value)

        # submit the form
        if args.submit_form:
            (url, data) = response.get_form().get_form_url_and_data()
            response = zyxel.post(url, data)
            response = zyxel.follow_redirect_if_present(response)
            if args.dump_html:
                print("response html")
                print(response.http_response.text)
            response_form = response.get_form()
            if response_form and args.show_form:
                print("response form")
                response_form.print_form()
            if args.save_response:
                with open(args.save_response, "w", encoding="UTF-8") as file:
                    print(response.http_response.text, file=file)
                print(f"wrote {args.save_response}")
