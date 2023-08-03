import os

from dptools.cli import BaseCLI
from dptools.train.input import DeepInputs


class CLI(BaseCLI):
    """
    Create deepmd-kit training set folder from ASE .db, .traj, or vasprun.xml files.

    :doc:`Complete documentaion here<../commands/input>`

    Examples:

    .. code-block:: console

        $ dptools input 00_system1.db 00_system2.db
        $ dptools input 0*_sys*.db # equivalent to above
        $ dptools input 00_system1/vasprun.xml 00_system2/vasprun.xml
        $ dptools input -p /path/to/dataset/folder 0*.db
    """
    help_info = "Set up deepmd-kit training input from ASE/VASP output"
    def add_args(self):
        self.parser.add_argument("inputs", nargs='+', metavar="input_file",
                help=".db, .traj, or vasprun.xml files")
        self.parser.add_argument("-n", type=int, default=None,
                help="Max number of images to take from each db")
        self.parser.add_argument("-p", "--path", type=str, default="./data",
                help="Specify path to dataset directory")
        self.parser.add_argument("-a", "--append", action="store_true",
                help="Append to dataset if system already exists in dataset directory")
        self.parser.add_argument("--sort", action="store_true",
                help="Sort each image in each input by atomic symbol")

    def main(self, args):
        self.names = []
        for inp in args.inputs:
            self.set_name(inp)
        path = os.path.abspath(args.path)
        thing = DeepInputs(args.inputs,
                           system_names=self.names,
                           path=path,
                           append=args.append,
                           n=args.n,
                           sort=args.sort,
                           )

    def set_name(self, input_file):
        path, ext = os.path.splitext(input_file)
        if ext not in [".db", ".traj", ".xml"]:
            raise ValueError(f"Unrecognized input file type, {input_file}")
        elif ext == ".xml" and path.split("/")[-1] == "vasprun":
            name = path.split("/")[-2]
        else:
            name = path.split("/")[-1]

        if name in self.names:
            raise ValueError(f"Multiple inputs with same system name detected: {name}"\
                    ". Give each input file a unique name.")

        self.names.append(name)
