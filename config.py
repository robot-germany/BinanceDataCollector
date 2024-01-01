from configparser import ConfigParser


def config(section: str, filename: str = "env.ini"):
    parser = ConfigParser()
    parser.read(filename)
    if parser.has_section(section):
        section_params = {param[0]: param[1] for param in parser.items(section)}
        return section_params
    else:
        raise Exception(f"Section {section} is not in the {filename} file.")


if __name__ == "__main__":
    print(config("Key"))
