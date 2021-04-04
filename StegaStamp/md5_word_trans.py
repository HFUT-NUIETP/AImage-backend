import MySQLdb
import hashlib

db = MySQLdb.connect("localhost", "root", "123456", "md5_word")


def save_word(word):
    cursor = db.cursor()
    md5 = hashlib.md5(word.encode(encoding='UTF-8')).hexdigest()
    md5_7 = md5[0:7]
    cursor.execute('''SELECT word FROM md5_word_chart WHERE md5='%s';''' % md5_7)
    if cursor.rowcount == 0:
        cursor.execute(
            '''INSERT INTO md5_word_chart(md5, word) VALUES ('%s','%s');''' % (md5_7, word))
    else:
        cursor.execute('''UPDATE md5_word_chart SET word='%s' WHERE md5='%s';''' % (word, md5_7))
    db.commit()
    return md5_7


def resolve_md5(md5_pre7):
    cursor = db.cursor()
    cursor.execute('SELECT word FROM md5_word_chart WHERE md5="%s"' % md5_pre7)
    results = cursor.fetchone()
    word = results[0]
    return word

# for test
if __name__ == '__main__':
    md5 = save_word('hahahahh')
    print(md5)
    print(resolve_md5(md5))
