class ColourPrint:
    @staticmethod
    def print_bg_red(*text):
        text = ' '.join(text)
        coloured_text = f"\033[41m{text}\033[0m"
        print(coloured_text)

    @staticmethod
    def print_green(*text):
        text = ' '.join(text)
        coloured_text = f"\033[92m{text}\033[0m"
        print(coloured_text)

    @staticmethod
    def print_yellow(*text):
        text = ' '.join(text)
        coloured_text = f"\033[93m{text}\033[0m"
        print(coloured_text)

    @staticmethod
    def print_blue(*text):
        text = ' '.join(text)
        coloured_text = f"\033[94m{text}\033[0m"
        print(coloured_text)

    @staticmethod
    def print_pink(*text):
        text = ' '.join(text)
        coloured_text = f"\033[95m{text}\033[0m"
        print(coloured_text)

    @staticmethod
    def print_turquoise(*text):
        text = ' '.join(text)
        coloured_text = f"\033[96m{text}\033[0m"
        print(coloured_text)
