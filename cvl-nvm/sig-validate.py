import argparse
import re
import nvm
import model
from modules.root import ModuleRoot
from modules.css import validate_signature


def find_sec(node, pattern):
    for child in node.children:
        if re.match(pattern, child.get_tree_name()):
            iter = nvm.NvmIterator(child.start(), child.end() - child.start())
            return iter
        res = find_sec(child, pattern)

        if res:
            return res

def sig_validate(node, sec_pattern):
    iter_sec = find_sec(node, sec_pattern)
    sec_name = re.sub(r'\^', '', sec_pattern)
    if iter_sec is not None:
        print(sec_name,"offset: %#x"%iter_sec.offset, " Length: %#x"%iter_sec.length)
        print("Validating signature of", sec_name, "......")
        sig_stat = validate_signature(iter_sec)
        print(sec_name, "signature stat: ", sig_stat, "\n")
    else:
        print(sec_name, "not found!")

def main():

    parser = argparse.ArgumentParser(description='sig validation argparse')
    parser.add_argument('file_name', help='The name of the input NVM file')
    args = parser.parse_args()

    if args.file_name:
        file_name =  args.file_name
    else:
        parser.print_help()
        return 0
    #file_name =  "E810_CQDA2_O_SEC_FW_1p7p0p8_NVM_4p01_PLDMoMCTP_0.18_80013C9B.bin"

    root = None
    try:
         root = model.parse(file_name, True)
    except nvm.OutOfBoundsException as oobe:
         print(oobe)

    sec_patt = [r"^NVM Bank #0", r"^Extended Mini Loader", r"^Recovery Image"]

    for patt in sec_patt:
        sig_validate(root, patt)


if __name__ == "__main__":
    main()

