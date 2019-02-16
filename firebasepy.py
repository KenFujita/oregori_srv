import firebase_admin
from firebase_admin import credentials
from firebase_admin import db

def update_value(path,res):
    cred = credentials.Certificate('./path/to/firebase_key')

    data_list = []
    #初回実行時のみ呼び出しする。2回目以降だと"既にinitializeされている"と怒られる
    if(not len(firebase_admin._apps)):
        firebase_admin.initialize_app(cred, {
            'databaseURL': 'path/to/database_URL'
        })
    data_list = res.split(',')
    url = 'path/to/server_URL'+data_list[0]
    ##databaseに初期データを追加する
    users_ref = db.reference(path)
    users_ref.update({
        'imageUrl': url,
        'percent': data_list[1]
    })

    print(users_ref.get())

if __name__ == '__main__':
    ##データを取得する
    update_value('test/')
