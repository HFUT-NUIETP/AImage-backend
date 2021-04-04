from StegaStamp.md5_word_trans import save_word, resolve_md5

txt = '''{"author":"d","date":"d","contact":"d","copyright":"d","area":"d"}'''
print(type(txt))
key = save_word(txt)
print(key)

print(resolve_md5(key))