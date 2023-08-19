from flask import Flask, jsonify
import mysql.connector

app = Flask(__name__)

# Kết nối cơ sở dữ liệu MySQL
db = mysql.connector.connect(
    host='103.97.126.24',
    user='beohbrrl_admin',
    password='nguyen2004nam',
    database='beohbrrl_note_app_data'
)

# Định nghĩa các endpoint API
@app.route('/api/get_data', methods=['GET'])
def get_data():
    cursor = db.cursor()
    try:
        # Thực hiện truy vấn để lấy dữ liệu từ cơ sở dữ liệu
        query = 'SELECT * FROM data'
        cursor.execute(query)
        data = cursor.fetchall()
        # Chuyển đổi dữ liệu thành một danh sách các đối tượng Python
        result = []
        for row in data:
            record = {
                'id': row[0],
                'product': row[1],
                'date': row[2],
                'MustHave': row[4],
                'NiceToHave': row[5],
                'Wasted': row[6],
                # Thêm các cột khác tùy ý
            }
            print(data)
            result.append(record)
        return jsonify(result)
    except Exception as e:
        return jsonify({'error': str(e)})
    finally:
        cursor.close()

if __name__ == '__main__':
    app.run()
