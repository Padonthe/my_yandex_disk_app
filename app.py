from flask import Flask, render_template, request, redirect, url_for, flash
import requests
import os

app = Flask(__name__)
app.secret_key = '024e59f8c70743e8b7f1d7547b8c3c07' 

# Токен доступа
access_token = 'y0_AgAAAAA7AHP-AAzoXgAAAAEbOmVuAACM61xH8IlPe5ptUuW5zR5-rlhIqw'

# Главная страница
@app.route('/')
def home():
    return render_template('index.html')

# Страница для отображения списка файлов
@app.route('/list_files', methods=['POST'])
def list_files():
    public_key = request.form['public_key']
    headers = {'Authorization': f'OAuth {access_token}'}
    url = 'https://cloud-api.yandex.net/v1/disk/resources'
    params = {'path': public_key}

    try:
        response = requests.get(url, headers=headers, params=params)
        response.raise_for_status()  # Проверяем на успешный статус код
        files = response.json()['_embedded']['items']
        return render_template('file_list.html', files=files)
    except requests.exceptions.RequestException as e:
        flash(f"Ошибка при получении данных: {e}")
        return redirect(url_for('home'))

# Страница для скачивания файла
@app.route('/download_file/<file_path>')
def download_file(file_path):
    headers = {'Authorization': f'OAuth {access_token}'}
    url = f'https://cloud-api.yandex.net/v1/disk/resources/download?path={file_path}'
    
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()  # Проверяем на успешный статус код
        download_url = response.json()['href']

        # Создание папки для загрузки, если она не существует
        download_dir = './downloads'
        if not os.path.exists(download_dir):
            os.makedirs(download_dir)

        # Скачивание файла
        file_response = requests.get(download_url)
        file_response.raise_for_status()

        with open(f'{download_dir}/{file_path.split("/")[-1]}', 'wb') as f:
            f.write(file_response.content)

        flash("Файл успешно загружен!")
    except requests.exceptions.RequestException as e:
        flash(f"Ошибка при скачивании файла: {e}")
    
    return redirect(url_for('home'))

if __name__ == '__main__':
    app.run(debug=True)
