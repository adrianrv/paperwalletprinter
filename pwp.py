import argparse
import base64
import io
import os

import cairosvg
import qrcode

parser = argparse.ArgumentParser()
parser.add_argument(
    '--address',
    help='Address of the wallet (public)',
    type=str,
    required=True
)
parser.add_argument(
    '--secret_key',
    help='Secret key of the given wallet (private)',
    type=str,
    required=True
)
parser.add_argument(
    '--amount',
    help='Amount to show in the paper wallet',
    type=int,
    required=True
)
parser.add_argument(
    '--template',
    help='Template to user for generating the paper wallet',
    type=str,
    required=True
)
args = parser.parse_args()


def string_to_qr_base64(text):
    qr = qrcode.make(text, box_size=150, border=0)
    mem_file = io.BytesIO()
    qr.save(mem_file, format='png')
    mem_file.seek(0)
    img_bytes = mem_file.read()
    result = base64.b64encode(img_bytes).decode('ascii')
    mem_file.close()
    return result


def set_variable(variable, value, wallet_file):
    os.system('sed -i "s@{}@{}@g" {}'.format(variable, value, wallet_file))


def main():
    # wallet from template
    wallet_file = os.path.join(os.getcwd(), '{}.svg'.format(args.address))
    os.system('cp {} {}'.format(args.template, wallet_file))

    # qr generation
    address_qr = '{}'.format(string_to_qr_base64(args.address))
    secret_key_qr = '{}'.format(string_to_qr_base64(args.secret_key))

    # SVG variable replacement
    set_variable('__amount__', args.amount, wallet_file)
    set_variable('__address__', args.address, wallet_file)
    set_variable('__address_qr__', address_qr, wallet_file)
    set_variable('__secret_key__', args.secret_key, wallet_file)
    set_variable('__secret_key_qr__', secret_key_qr, wallet_file)

    # export to pdf
    pdf = os.path.join(os.getcwd(), '{}.pdf'.format(args.address))
    cairosvg.svg2pdf(url=wallet_file, write_to=pdf)

    # remove svg file
    os.remove(wallet_file)


if __name__ == "__main__":
    main()
