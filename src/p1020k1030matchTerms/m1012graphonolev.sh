# transliteration argument is set to False
python m1012graphonolev.py m1012graphonolev-uk-ru-in.txt ua ru Debug None m1012graphonolev-phonetic-features.tsv,m1012graphonolev-phonetic-features0.tsv  >m1012graphonolev-uk-ru-out.txt
python m1012graphonolev.py m1012graphonolev-en-uk-in.txt en ua Debug m1012graphonolev-phonetic-trans-lat2cyr.txt m1012graphonolev-phonetic-features.tsv,m1012graphonolev-phonetic-features0.tsv  >m1012graphonolev-en-uk-out.txt
# ? no!!! ua ua -- for proper use of transliteration: lat2cyr; otherwise : en-ua :: transliteration -- only use for default non-lev computation...