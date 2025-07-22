# class ColourPrint:
#     @staticmethod
#     def print_bg_red(*text):
#         text = ' '.join(text)
#         coloured_text = f"\033[41m{text}\033[0m"
#         print(coloured_text)
#
#     @staticmethod
#     def print_green(*text):
#         text = ' '.join(text)
#         coloured_text = f"\033[92m{text}\033[0m"
#         print(coloured_text)
#
#     @staticmethod
#     def print_yellow(*text):
#         text = ' '.join(text)
#         coloured_text = f"\033[93m{text}\033[0m"
#         print(coloured_text)
#
#     @staticmethod
#     def print_blue(*text):
#         text = ' '.join(text)
#         coloured_text = f"\033[94m{text}\033[0m"
#         print(coloured_text)
#
#     @staticmethod
#     def print_pink(*text):
#         text = ' '.join(text)
#         coloured_text = f"\033[95m{text}\033[0m"
#         print(coloured_text)
#
#     @staticmethod
#     def print_turquoise(*text: object) -> None:
#         text = ' '.join(*text)
#         coloured_text = f"\033[96m{text}\033[0m"
#         print(coloured_text)



class ColourPrint:

    __reset = '\033[0m'
    __bg_red = "\033[41m"
    __green = "\033[92m"
    __yellow = "\033[93m"
    __blue = "\033[94m"
    __pink = "\033[95m"
    __turquoise = "\033[96m"


    @staticmethod
    def _stringify(obj, *, use_repr=False):
        choice = repr if use_repr else str
        converted = [choice(o) for o in obj]
        return converted

    @classmethod
    def print_bg_red(cls,*text,use_repr=False):
        coloured_text_list = cls._stringify(text,use_repr=use_repr)
        coloured_text = " ".join(coloured_text_list)
        print(f"{cls.__bg_red}{coloured_text}{cls.__reset}")

    @classmethod
    def print_green(cls, *text, use_repr=False):
        coloured_text_list = cls._stringify(text, use_repr=use_repr)
        coloured_text = " ".join(coloured_text_list)
        print(f"{cls.__green}{coloured_text}{cls.__reset}")

    @classmethod
    def print_yellow(cls, *text, use_repr=False):
        coloured_text_list = cls._stringify(text, use_repr=use_repr)
        coloured_text = " ".join(coloured_text_list)
        print(f"{cls.__yellow}{coloured_text}{cls.__reset}")

    @classmethod
    def print_blue(cls, *text, use_repr=False):
        coloured_text_list = cls._stringify(text, use_repr=use_repr)
        coloured_text = " ".join(coloured_text_list)
        print(f"{cls.__blue}{coloured_text}{cls.__reset}")

    @classmethod
    def print_pink(cls, *text, use_repr=False):
        coloured_text_list = cls._stringify(text, use_repr=use_repr)
        coloured_text = " ".join(coloured_text_list)
        print(f"{cls.__pink}{coloured_text}{cls.__reset}")

    @classmethod
    def print_turquoise(cls, *text, use_repr=False):
        coloured_text_list = cls._stringify(text, use_repr=use_repr)
        coloured_text = " ".join(coloured_text_list)
        print(f"{cls.__turquoise}{coloured_text}{cls.__reset}")


# if __name__=='__main__':
    # ColourPrint.print_green('text, green,',2)
    # ColourPrint.print_blue('blue')
    # ColourPrint.print_yellow('yellow')
    # ColourPrint.print_bg_red('red')
    # ColourPrint.print_pink('pink', 'the')
    # ColourPrint.print_pink(2)
    # ColourPrint.print_turquoise('torq')

