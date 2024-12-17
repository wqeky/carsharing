from flask import render_template, request, redirect, url_for, flash
from app import app, db, bcrypt
from app.models import Client
from app.models import Car
from app.models import Fine
from app.models import Trip


@app.before_request
def before_request():
    if request.method == "POST" and "_method" in request.form:
        request.method = request.form["_method"].upper()

@app.route('/')
def index():
    # Получаем статистику
    num_clients = db.session.query(Client).count()
    num_cars = db.session.query(Car).count()
    num_fines = db.session.query(Fine).count()

    # Передаем статистику в шаблон
    return render_template('index.html', num_clients=num_clients, num_cars=num_cars, num_fines=num_fines)


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        lastname = request.form.get('lastname')
        firstname = request.form.get('firstname')
        email = request.form.get('email')
        driver_license = request.form.get('driver_license')
        password = bcrypt.generate_password_hash(request.form.get('password')).decode('utf-8')

        new_client = Client(
            lastname=lastname,
            firstname=firstname,
            email=email,
            driver_license=driver_license,
            password=password
        )

        try:
            db.session.add(new_client)
            db.session.commit()
            return redirect(url_for('index'))
        except Exception as e:
            return f"Ошибка регистрации: {str(e)}"

    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        client = Client.query.filter_by(email=email).first()
        if client and bcrypt.check_password_hash(client.password, password):
            return redirect(url_for('index'))
        else:
            return "Неправильный логин или пароль"

    return render_template('login.html')


# Раздел "Машины"
@app.route('/cars', methods=['GET', 'POST'])
def cars():
    query = Car.query

    # Фильтрация по модели
    model_filter = request.args.get('model')
    if model_filter:
        query = query.filter(Car.model.like(f"%{model_filter}%"))

    # Фильтрация по статусу
    status_filter = request.args.get('status')
    if status_filter:
        query = query.filter(Car.status == status_filter)

    page = request.args.get('page', 1, type=int)
    per_page = 20  # Количество записей на страницу
    cars_paginated = query.paginate(page=page, per_page=per_page)

    return render_template('cars.html', cars=cars_paginated, model_filter=model_filter, status_filter=status_filter)


@app.route('/add_car', methods=['GET', 'POST'])
def add_car():
    if request.method == 'POST':
        # Получаем данные из формы
        model = request.form.get('model')
        status = request.form.get('status')
        location = request.form.get('location')
        license_plate = request.form.get('license_plate')

        # Создаем новую машину
        new_car = Car(model=model, status=status, location=location, license_plate=license_plate)
        db.session.add(new_car)
        db.session.commit()

        # Перенаправляем обратно на страницу машин
        return redirect(url_for('cars'))

    # Если метод GET, отобразим форму
    return render_template('add_car.html')


from flask import request

@app.route('/remove_car/<int:car_id>', methods=['POST', 'DELETE'])
def remove_car(car_id):
    cars = Car.query.get_or_404(car_id)

    try:
        db.session.delete(cars)
        db.session.commit()
        flash("Машина успешно удалена!", "success")
    except Exception as e:
        flash(f"Ошибка при удалении машины: {e}", "error")

    return redirect(url_for('cars'))



# Раздел "Штрафы"
@app.route('/fines', methods=['GET'])
def fines():
    query = Fine.query

    # Получаем значение фильтра (диапазон стоимости)
    amount_filter = request.args.get('amount_filter', type=int, default=5000)  # По умолчанию 5000

    # Если значение фильтра задано, фильтруем штрафы по этой сумме
    if amount_filter is not None:
        query = query.filter(Fine.amount <= amount_filter)  # Показываем штрафы с суммой <= выбранной

    # Пагинация
    page = request.args.get('page', 1, type=int)
    per_page = 15
    fines_paginated = query.paginate(page=page, per_page=per_page)

    return render_template('fines.html', fines=fines_paginated, amount_filter=amount_filter)

@app.route('/delete_fine/<int:fine_id>', methods=['POST'])
def delete_fine(fine_id):
    fine = Fine.query.get_or_404(fine_id)

    try:
        db.session.delete(fine)
        db.session.commit()
        flash("Штраф успешно удален!", "success")
    except Exception as e:
        flash(f"Ошибка при удалении штрафа: {e}", "error")

    return redirect(url_for('fines'))