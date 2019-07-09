#python3

"""
Take English text and translate (that is transliterate) into Al Bhed.
"""

import unidecode
import unicodedata as ud
from absl import app
from absl import flags


FLAGS = flags.FLAGS
flags.DEFINE_string('text', None, 'Text to translate')
# ISO code 'en' for English and pseudo-ISO code 'ab' for Al Bhed.
flags.DEFINE_boolean('en_to_ab', True, 'English to Al Bhed')
flags.DEFINE_boolean('allow_diacritics', False, 'Remove diacritics')

# Required flags.
flags.mark_flag_as_required('text')

def main(argv):
  del argv # Unused.
  text = FLAGS.text
  en_to_ab = FLAGS.en_to_ab
  allow_diacritics = FLAGS.allow_diacritics

  def read_character_mapping(mapping):
    # Return NFC of string
    with open(mapping) as f:
      raw = f.read()
    return raw


  def remove_diacrtics(accented_string):
    # Removes diacritics regardless if in NFC/NFD normalized etc.
    # https://www.fonts.com/content/learning/fontology/level-3/signs-and-symbols/accents
    normalized_string = unidecode.unidecode(accented_string)
    return normalized_string


  def tsv_to_strings(tsv):
    first = []; second = []
    pairs = tsv.splitlines()
    for pair in pairs:
      char = pair.split('\t')
      first.append(char[0] + char[0].lower())
      second.append(char[1] + char[1].lower())
    return ''.join(first), ''.join(second)


  def create_mapping_table(trans_direction, lang1, lang2):
    if trans_direction == True:
      table = ''.maketrans(lang1, lang2)
      return table
    else:
      table = ''.maketrans(lang2, lang1)
      return table


  def prenormalize_text(text, allow_diacritics):
    if allow_diacritics == False:
      normalized_text = remove_diacrtics(text)
      return normalized_text
    else:
      nfd_normalized_text = ud.normalize('NFD', text)
      return nfd_normalized_text

  def translate(text, table):
    passthrough = False
    processed_chars = []
    for char in text:
      if passthrough == False:
        if char == '*':
          passthrough = True
          processed_chars.append(char)
        else:
          processed_chars.append(char.translate(table))
      else:
        if char == '*':
          passthrough = False
          processed_chars.append(char)
        else:
          processed_chars.append(char)
    return ''.join(processed_chars)


  def remove_break_character(text):
    return text.replace('*', '')





  # Character mapping source.
  # https://finalfantasy.fandom.com/wiki/Al_Bhed
  tsv = read_character_mapping('ab_en_mapping.txt')
  ab, en = tsv_to_strings(tsv)
  table = create_mapping_table(en_to_ab, en, ab)
  prenormalized_text = prenormalize_text(text, allow_diacritics)
  translation = translate(prenormalized_text, table)
  nfc_normalized_text = ud.normalize('NFC', translation)
  clean_translation = remove_break_character(nfc_normalized_text)
  print(clean_translation)

if __name__ == '__main__':
  app.run(main)