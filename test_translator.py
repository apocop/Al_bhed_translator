import translator



def test_read_character_mapping():
    # Tests that a string instance is produced.
    assert type(translator.read_character_mapping('ab_en_mapping.txt')) == type('')


def test_tsv_to_strings():
    # Tests that the two generated strings are the same length, demonstrating that every character has a mapping.
    tsv = translator.read_character_mapping('ab_en_mapping.txt')
    first, second = translator.tsv_to_strings(tsv)
    assert len(first) == len(second)


def test_remove_diacritics():
    # Test removal of diacritics from a token.
    test_pair = [
        ('maté', 'mate'),
        ('füher', 'fuher'),
        ('Thaïs', 'Thais'),
        ('résumé', 'resume'),
        ('façade', 'facade')
        ('è', 'e')
    ]
    for pair in test_pair:
        assert translator.remove_diacrtics(pair[0]) == pair[1]