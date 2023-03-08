import configparser

def extract_secrets(config_file) -> list:
    config = configparser.ConfigParser()
    config.read_file(config_file)

    sections = config.sections()

    secrets = []
    if sections:
        for section in sections:
            for item in config.items(section):
                secrets.append([item[0].upper(), item[1]])

    return secrets
