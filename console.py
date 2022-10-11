#!/usr/bin/python3
"""
The console for AirBnb project
Contains the entry point of the command interpreter
"""
from ast import arg
import cmd
import shlex
from models.base_model import BaseModel
from models.user import User
from models.state import State
from models.review import Review
from models.place import Place
from models.city import City
from models.amenity import Amenity
from models import storage


class HBNBCommand(cmd.Cmd):
    """
    custom console class
    """

    prompt = '(hbnb) '

    classes = [
        'BaseModel', 'User', 'Place', 'State', 'City', 'Amenity', 'Review'
        ]

    dot_cmds = ['all', 'count', 'show', 'destroy', 'update']

    types = {
             'number_rooms': int, 'number_bathrooms': int,
             'max_guest': int, 'price_by_night': int,
             'latitude': float, 'longitude': float
            }

    def do_quit(self, line):
        """Handles the 'quit' command

        Args:
            line(args): input argument for quiting
            the terminal

        """
        return True

    def help_quit(self):
        """
        Help instructions for the quit command
        """
        print('Quit command to exit the program\n')

    def do_EOF(self, line):
        """Quits command interpreter with ctrl+d

         Args:
            line(args): input argument for quiting
            the terminal

        """
        print()
        return True

    def emptyline(self):
        """
        Eliminates empty lines
        """
        pass

    def _key_value_parser(self, args):
        """creates a dictionary from a list of strings"""
        new_dict = {}
        for arg in args:
            if "=" in arg:
                kvp = arg.split('=', 1)
                key = kvp[0]
                value = kvp[1]
                if value[0] == value[-1] == '"':
                    value = shlex.split(value)[0].replace('_', ' ')
                else:
                    try:
                        value = int(value)
                    except Exception:
                        try:
                            value = float(value)
                        except Exception:
                            continue
                new_dict[key] = value
        return new_dict

    def do_show(self, line):
        """Prints a string representation of an instance.

        Args:
            line(line): to enter with command <class name> <id>
            Example: 'show User 1234-1234-1234'

        """
        args = line.split(" ")
        if not line:
            print('** class name missing **')
            return False
        elif args[0] not in self.classes:
            print("** class doesn't exist **")
            return False
        elif len(args) != 2:
            print("** instance id missing **")
            return False

        all_objs = storage.all()
        for obj_id in all_objs.keys():
            if obj_id == args[0]+'.'+args[1]:
                obj = all_objs[obj_id]
                print(obj)
                return False
        print('** no instance found **')

    def do_create(self, line):
        """Creates a new instance of @cls_name class,
        and prints the new instance's ID.

        Args:
            line(args): Arguments to enter with command: <class name>
            Example: 'create User'

        """
        args = line.split(" ")
        if not line:
            print('** class name missing **')
            return False
        elif args[0] not in self.classes:
            print("** class doesn't exist **")
            return False
        """
        args[0] contains class name, create new instance
        of that class updates 'updated_at' attribute,
        and saves into JSON file
        """
        new_dict = self._key_value_parser(args[1:])

        obj = eval(args[0])()
        obj.save()
        print(obj.id)
        com = "{} {} {}".format(args[0], obj.id, new_dict)
        self.do_update(com)

    def do_destroy(self, line):
        """Prints a string representation of an instance.

        Args:
            line(line): to enter with command <class name> <id>
            Example: 'show User 1234-1234-1234'

        """
        args = line.split(" ")
        if not line:
            print('** class name missing **')
            return False
        elif args[0] not in self.classes:
            print("** class doesn't exist **")
            return False
        elif len(args) < 2:
            print("** instance id missing **")
            return False

        all_objs = storage.all()
        for obj_id in all_objs.keys():
            if obj_id == args[0]+'.'+args[1]:
                storage.all().pop(obj_id)
                storage.save()
                return False
        print('** no instance found **')

    def do_all(self, line):
        """Prints a string representation of all instance.

        Args:
            line(line): to enter with command <class name> <id>
            Example: 'all BaseModel 1234-1234-1234'

        """
        args = line.split(" ")
        if args[0] not in self.classes:
            print("** class doesn't exist **")
            return False

        all_objs = storage.all()
        lis = []
        for obj_id in all_objs.keys():
            sp = obj_id.split('.')
            if args[0] in sp:
                lis.append(str(all_objs[obj_id]))
        print(lis)

    def do_update(self, args):
        """ Updates a certain object with new info """
        c_name = c_id = att_name = att_val = kwargs = ''

        # isolate cls from id/args, ex: (<cls>, delim, <id/args>)
        args = args.partition(" ")
        if args[0]:
            c_name = args[0]
        else:  # class name not present
            print("** class name missing **")
            return
        if c_name not in HBNBCommand.classes:  # class name invalid
            print("** class doesn't exist **")
            return

        # isolate id from args
        args = args[2].partition(" ")
        if args[0]:
            c_id = args[0]
        else:  # id not present
            print("** instance id missing **")
            return

        # generate key from class and id
        key = c_name + "." + c_id

        # determine if key is present
        if key not in storage.all():
            print("** no instance found **")
            return

        # first determine if kwargs or args
        if '{' in args[2] and '}' in args[2] and type(eval(args[2])) is dict:
            kwargs = eval(args[2])
            args = []  # reformat kwargs into list, ex: [<name>, <value>, ...]
            for k, v in kwargs.items():
                args.append(k)
                args.append(v)
        else:  # isolate args
            args = args[2]
            if args and args[0] == '\"':  # check for quoted arg
                second_quote = args.find('\"', 1)
                att_name = args[1:second_quote]
                args = args[second_quote + 1:]

            args = args.partition(' ')

            # if att_name was not quoted arg
            if not att_name and args[0] != ' ':
                att_name = args[0]
            # check for quoted val arg
            if args[2] and args[2][0] == '\"':
                att_val = args[2][1:args[2].find('\"', 1)]

            # if att_val was not quoted arg
            if not att_val and args[2]:
                att_val = args[2].partition(' ')[0]

            args = [att_name, att_val]

        # retrieve dictionary of current objects
        new_dict = storage.all()[key]

        # iterate through attr names and values
        for i, att_name in enumerate(args):
            # block only runs on even iterations
            if (i % 2 == 0):
                att_val = args[i + 1]  # following item is value
                if not att_name:  # check for att_name
                    print("** attribute name missing **")
                    return
                if not att_val:  # check for att_value
                    print("** value missing **")
                    return
                # type cast as necessary
                if att_name in HBNBCommand.types:
                    att_val = HBNBCommand.types[att_name](att_val)

                # update dictionary with name, value pair
                new_dict.__dict__.update({att_name: att_val})

        new_dict.save()  # save updates to file

    def do_count(self, args):
        """Count current number of class instances"""
        count = 0
        for k, v in storage.all().items():
            if args == k.split('.')[0]:
                count += 1
        print(count)

    def help_count(self):
        """ """
        print("Usage: count <class_name>")

    def precmd(self, line):
        """Reformat command line for advanced command syntax.

        Usage: <class name>.<command>([<id> [<*args> or <**kwargs>]])
        (Brackets denote optional fields in usage example.)
        """
        _cmd = _cls = _id = _args = ''  # initialize line elements

        # scan for general formating - i.e '.', '(', ')'
        if not ('.' in line and '(' in line and ')' in line):
            return line

        try:  # parse line left to right
            pline = line[:]  # parsed line

            # isolate <class name>
            _cls = pline[:pline.find('.')]

            # isolate and validate <command>
            _cmd = pline[pline.find('.') + 1:pline.find('(')]
            if _cmd not in HBNBCommand.dot_cmds:
                raise Exception

            # if parantheses contain arguments, parse them
            pline = pline[pline.find('(') + 1:pline.find(')')]
            if pline:
                # partition args: (<id>, [<delim>], [<*args>])
                pline = pline.partition(', ')  # pline convert to tuple

                # isolate _id, stripping quotes
                _id = pline[0].replace('\"', '')
                # possible bug here:
                # empty quotes register as empty _id when replaced

                # if arguments exist beyond _id
                pline = pline[2].strip()  # pline is now str
                if pline:
                    # check for *args or **kwargs
                    if pline[0] == '{' and pline[-1] == '}'\
                            and type(eval(pline)) is dict:
                        _args = pline
                    else:
                        _args = pline.replace(',', '')
                        # _args = _args.replace('\"', '')
            line = ' '.join([_cmd, _cls, _id, _args])

        except Exception as mess:
            pass
        finally:
            return line


if __name__ == '__main__':
    HBNBCommand().cmdloop()
