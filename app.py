from flask import Flask, jsonify, request
from flask_mysqldb import MySQL

app= Flask(__name__)

# mysql config
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'datasekolah'
mysql = MySQL(app)

@app.route('/')
def root():
    return 'Selamat Datang'

@app.route('/siswa', methods=['GET', 'POST', 'PATCH'])
def siswa():
    if request.method == 'GET':
        cursor = mysql.connection.cursor()
        cursor.execute("SELECT * FROM SISWA")

        column_names = [i[0] for i in cursor.description]
        data = []
        for row in cursor.fetchall():
            data.append(dict(zip(column_names, row)))

        cursor.close()
        return jsonify(data)
    
    elif request.method == 'POST':
        if 'nama' not in request.json or 'umur' not in request.json or 'kelas' not in request.json:
            return jsonify({'error': 'One or more fields are missing'}), 400
        
        nama = request.json['nama']
        umur = request.json['umur']
        kelas = request.json['kelas']

        cursor = mysql.connection.cursor()
        sql = "INSERT INTO SISWA (nama, umur, kelas) VALUES (%s, %s, %s)"
        val = (nama, umur, kelas)
        cursor.execute(sql, val)

        mysql.connection.commit()

        cursor.close()
        return jsonify({'message': 'Data added successfully!'})

    elif request.method == 'PATCH':
        id_siswa = request.args.get('id')
        if id_siswa:
            data = request.json

            cursor = mysql.connection.cursor()
            sql = "UPDATE siswa SET "
            sql_params = []
            val = []

            if 'nama' in data:
                sql_params.append("nama = %s")
                val.append(data['nama'])
            if 'umur' in data:
                sql_params.append("umur = %s")
                val.append(data['umur'])
            if 'kelas' in data:
                sql_params.append("kelas = %s")
                val.append(data['kelas'])

            sql += ", ".join(sql_params)
            sql += " WHERE id_siswa = %s"
            val.append(id_siswa)

            cursor.execute(sql, val)
            mysql.connection.commit()
            cursor.close()

            return jsonify({'message': 'Data patched successfully!'})
        else:
            return jsonify({'error': 'ID not provided'}), 400
        

@app.route('/siswa/details', methods=['GET'])
def detailsiswa():
    id_siswa = request.args.get('id')
    if id_siswa:
        cursor = mysql.connection.cursor()
        sql = "SELECT * FROM SISWA WHERE id_siswa = %s"
        val = (id_siswa,)
        cursor.execute(sql, val)

        column_names = [i[0] for i in cursor.description]
        data = []
        for row in cursor.fetchall():
            data.append(dict(zip(column_names, row)))

        cursor.close()
        return jsonify(data)
    else:
        return jsonify({'error': 'ID not provided'}), 400
    
@app.route('/siswa/edit', methods=['PUT'])
def editsiswa():
    id_siswa = request.args.get('id')
    if id_siswa:
        data = request.json

        cursor = mysql.connection.cursor()
        sql = "UPDATE siswa SET nama=%s, umur=%s, kelas=%s WHERE id_siswa = %s"
        val = (data['nama'], data['umur'], data['kelas'], id_siswa)
        cursor.execute(sql, val)

        mysql.connection.commit()

        cursor.close()
        return jsonify({'message': 'Data updated successfully!'})
    else:
        return jsonify({'error': 'ID not provided'}), 400

@app.route('/siswa/delete', methods=['DELETE'])
def deletesiswa():
    id_siswa = request.args.get('id')
    if id_siswa:
        cursor = mysql.connection.cursor()
        sql = "DELETE FROM SISWA WHERE id_siswa = %s"
        val = (id_siswa,)
        cursor.execute(sql, val)

        mysql.connection.commit()

        cursor.close()
        return jsonify({'message': 'Data deleted successfully!'})
    else:
        return jsonify({'error': 'ID not provided'}), 400

if __name__=='__main__':
    app.run(host='0.0.0.0', port=50, debug=True)
