import io
import base64
from turtle import color
from nbt.nbt import TAG_List, TAG_Compound, NBTFile
import re

colors = {
    '§0': '\033[0;30m',
    '§1': '\033[0;34m',
    '§2': "\033[0;32m",
    '§3': "\033[0;36m",
    '§4': '\033[0;31m',
    '§5': "\033[0;45m",
    '§6': '\033[0;93m',
    '§7': '\033[38;4;236m',
    '§8': '\033[0;40m',
    '§9': '\033[0;94m',
    '§a': '\033[0;92m',
    '§b': '\033[0;96m',
    '§c': '\033[0;91m',
    '§d': '\033[0;35m',
    '§e': '\033[0;93m',
    '§f': '\033[0m',
    '§g': '\033[0m',
}

motd_colors = {
  '\u00A74': '§4',
  '\u00A7c': '§c',
  '\u00A76': '§6',
  '\u00A7e': '§e',
  '\u00A72': '§2',
  '\u00A7a': '§a',
  '\u00A7b': '§b',
  '\u00A73': '§3',
  '\u00A71': '§1',
  '\u00A79': '§9',
  '\u00A7d': '§d',
  '\u00A75': '§5',
  '\u00A7f': '§f',
  '\u00A77': '§7',
  '\u00A78': '§8',
  '\u00A70': '§0',
  '\u00A7r': '§r',
  '\u00A7l': '§l',
  '\u00A7o': '§o',
  '\u00A7n': '§n',
  '\u00A7m': '§m',
  '\u00A7k': '§k',
}


def decode_nbt(raw):
    """
    Decode a gziped and base64 decoded string to an NBT object
    """

    return NBTFile(fileobj=io.BytesIO(base64.b64decode(raw)))


def unpack_nbt(tag):
    """
    Unpack an NBT tag into a native Python data structure.
    Taken from https://github.com/twoolie/NBT/blob/master/examples/utilities.py
    """

    if isinstance(tag, TAG_List):
        return [unpack_nbt(i) for i in tag.tags]
    elif isinstance(tag, TAG_Compound):
        return dict((i.name, unpack_nbt(i)) for i in tag.tags)
    else:
        return tag.value


def parse_color(string: str, rev = False) -> str:

    if rev:
      regex = r"\\u00A7[0-9a-or]"

      matches = re.finditer(regex, string, re.MULTILINE)

      for _matchNum, match in enumerate(matches, start=1):
        k = match.group()
        if k in motd_colors:
          string = string.replace(k, motd_colors[k])

      string = string + '§r'

    else:
      color_regex = r"§[a-g0-9]"

      matches = re.finditer(color_regex, string, re.MULTILINE)

      for _matchNum, match in enumerate(matches, start=1):
        k = match.group()
        if k in colors:
          string = string.replace(k, colors[k])

      string = string + '\033[0m'

    return string

