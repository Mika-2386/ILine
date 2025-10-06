#!/usr/bin/evn python
import os

from sqlalchemy import asc, desc, or_
from flask import Flask, render_template, request, redirect, url_for

from database import db, General_manager, Manager, Salary_general_manager, Salary_manager, Group_leader, \
    Salary_group_leader, Senior_developer, Salary_senior_developer, Salary_developer, Developer

app = Flask(__name__)
 # Тут ссылаемся на мою БД с таблицами сотрудников
# $env:SQLALCHEMY_DATABASE_URI="postgresql://postgres:123456@localhost:5432/Line"
app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("SQLALCHEMY_DATABASE_URI")

db.init_app(app)

# --- Создаем базу-------
with app.app_context():
    db.create_all()

#----------Поиск сотрудника---------------

@app.route('/search', methods=['GET', 'POST'])

def Search():
    search_query = request.args.get('search', '')


    # Например, ищем по всему ФИО
    if search_query:
        pattern = f"%{search_query}%"

        general = General_manager.query.filter(
            (General_manager.name.ilike(pattern)) |
            (General_manager.surname.ilike(pattern)) |
            (General_manager.patronymic.ilike(pattern))

        ).all()


        managers_ = Manager.query.filter(
            (Manager.name.ilike(pattern)) |
            (Manager.surname.ilike(pattern)) |
            (Manager.patronymic.ilike(pattern))

        ).all()


        group = Group_leader.query.filter(
            (Group_leader.name.ilike(pattern)) |
            (Group_leader.surname.ilike(pattern)) |
            (Group_leader.patronymic.ilike(pattern))
        ).all()


        sd = Senior_developer.query.filter(
            (Senior_developer.name.ilike(pattern)) |
            (Senior_developer.surname.ilike(pattern)) |
            (Senior_developer.patronymic.ilike(pattern))


        ).all()


        dv = Developer.query.filter(
            (Developer.name.ilike(pattern)) |
            (Developer.surname.ilike(pattern)) |
            (Developer.patronymic.ilike(pattern))

        ).all()


    else:
        # если поиска нет — показываем все или по умолчанию
        general = General_manager.query.all()
        managers_ = Manager.query.all()
        group = Group_leader.query.all()
        sd = Senior_developer.query.all()
        dv = Developer.query.all()

    return render_template(
        "all_employees.html",
        general = general,
        managers_=managers_,
        group=group,
        sd=sd,
        dv=dv,
           )


@app.route('/', methods=['GET'])
def Employees():
    models_mapping = {
    'general': General_manager,
    'manager': Manager,
    'group': Group_leader,
    'sd': Senior_developer,
    'dv': Developer
    }

    model_name = request.args.get('model', 'general')
    sort_by = request.args.get('sort_by', 'id')
    order = request.args.get('order', 'asc')


    model_class = models_mapping.get(model_name)
    if not model_class:
        return "Модель не найдена", 404

    allowed_fields = {
        'general': ['name', 'surname', 'patronymic', 'id'],
        'manager': ['name', 'surname', 'patronymic', 'id'],
        'group': ['name', 'surname', 'patronymic', 'id'],
        'sd': ['name', 'surname', 'patronymic', 'id'],
        'dv': ['name', 'surname', 'patronymic', 'id']
    }

    if sort_by not in allowed_fields.get(model_name, []):
        sort_by = 'id'

    column_attr = getattr(model_class, sort_by)

    # Начинаем формировать запрос
    query = model_class.query

         # Сортировка
    if order == 'asc':
        query = query.order_by(asc(column_attr))
    else:
        query = query.order_by(desc(column_attr))

    results = query.all()


    general = General_manager.query.all()
    managers_ = Manager.query.all()
    group = Group_leader.query.all()
    sd = Senior_developer.query.all()
    dv = Developer.query.all()


    return render_template(
        "all_employees.html",
        general=general,
        managers_=managers_,
        group=group,
        sd = sd,
        dv=dv,
        sort_by=sort_by,
        order=order,
        results=results

    )



# ---------------Вывод размера заработной платы и занимаемая должность
@app.route('/salary_general_manager')
def get_salary_general():
    salary_g = Salary_general_manager.query.all()
    return render_template("salary_general.html", salary_g=salary_g)

@app.route('/salary_manager')
def get_salary_manager():
    salary_m = Salary_manager.query.all()
    return render_template("salary_manager.html", salary_m=salary_m)

@app.route('/salary_group_leader')
def get_salary_group():
    salary_gr = Salary_group_leader.query.all()
    return render_template("salary_group.html", salary_gr=salary_gr)

@app.route('/salary_senior_developer')
def get_salary_senior():
    salary_sd = Salary_senior_developer.query.all()
    return render_template("salary_senior.html", salary_sd=salary_sd)



@app.route('/salary_developer')
def get_salary_developerr():
    salary_dv = Salary_developer.query.all()
    return render_template("salary_developer.html", salary_dv=salary_dv)

# ------------ ссылка на сотрудников по руководителям-------------------

@app.route('/managers/<int:id_general_manager>')
def director_by_manager(id_general_manager):
    general = General_manager.query.get_or_404(id_general_manager)
    return render_template("managers.html", # страница вывода сотрудников
                           general_name = general.name, # для заголовка страницы
                           general_surname=general.surname, # для заголовка страницы
                           general_patronymic=general.patronymic, # для заголовка страницы
                           general_salary_post = general.salary_g.post, # для заголовка страницы
                           # m_name = general.managers_.name,
                           managers_=general.managers_, #  передаем список сотрудников с руководителем
                           )

@app.route('/group_leader/<int:id_manager>')
def director_by_leader(id_manager):
    managers_ = Manager.query.get_or_404(id_manager)
    return render_template("leader.html",
                           managers__name = managers_.name,
                           managers__surname=managers_.surname,
                           managers__patronymic=managers_.patronymic,
                           managers__salary_post = managers_.salary_m.post,
                           group=managers_.group,
                           )

@app.route('/senior_developer/<int:id_group_leader>')
def director_by_senior(id_group_leader):
    group = Group_leader.query.get_or_404(id_group_leader)
    return render_template("senior.html",
                           group_name = group.name,
                           group_surname=group.surname,
                           group__patronymic=group.patronymic,
                           group_salary_post = group.salary_gr.post,
                           sd=group.sd,
                           )

@app.route('/developer/<int:id_senior_developer>')
def director_by_developer(id_senior_developer):
    sd = Senior_developer.query.get_or_404(id_senior_developer)
    return render_template("developer.html",
                           sd_name = sd.name,
                           sd_surname=sd.surname,
                           sd_patronymic=sd.patronymic,
                           sd_salary_post = sd.salary_sd.post,
                           dv=sd.dv,
                           )



#--------Смена руководителя---------------


@app.route('/update_group_leader/<int:id_group_leader>', methods=['GET', 'POST'])
def update_group_leader(id_group_leader):
    group = Group_leader.query.get_or_404(id_group_leader)
    if request.method == 'POST':
        # Получаем новые данные из формы
        new_manager_id = request.form.get('id_manager')
        # Обновляем
        if new_manager_id:
            group.id_manager = new_manager_id
        db.session.commit()
        return redirect(url_for('Employees'))

    # Для GET — показываем форму
    managers_ = Manager.query.all()
    return render_template('update_group.html',
                           group_id = id_group_leader,
                           group_name=group.name,
                           group_surname=group.surname,
                           group_patronymic=group.patronymic,
                           managers_surname=group.managers_.surname,
                           managers_name=group.managers_.name,
                           managers_patronymic=group.managers_.patronymic,
                           managers_=managers_,
                           group=group)

@app.route('/update_senior_developer/<int:id_senior_developer>', methods=['GET', 'POST'])
def update_senior_developer(id_senior_developer):
    sd = Senior_developer.query.get_or_404(id_senior_developer)
    if request.method == 'POST':
        # Получаем новые данные из формы
        new_group_id = request.form.get('id_group')
        # Обновляем
        if new_group_id:
            sd.id_group = new_group_id
        db.session.commit()
        return redirect(url_for('Employees'))

    # Для GET — показываем форму
    group = Group_leader.query.all()
    return render_template('update_senior_developer.html',
                           sd_id = sd.id,
                           sd_name=sd.name,
                           sd_surname=sd.surname,
                           sd_patronymic=sd.patronymic,
                           group_surname=sd.group.surname,
                           group_name=sd.group.name,
                           group_patronymic=sd.group.patronymic,
                           group=group,
                           sd=sd)

@app.route('/update_developer/<int:id_developer>', methods=['GET', 'POST'])
def update_developer(id_developer):
    dv = Developer.query.get_or_404(id_developer)
    if request.method == 'POST':
        # Получаем новые данные из формы
        new_sd_id = request.form.get('id_sd')
        # Обновляем
        if new_sd_id:
            dv.id_sd = new_sd_id
        db.session.commit()
        return redirect(url_for('Employees'))

    # Для GET — показываем форму
    sd = Senior_developer.query.all()
    return render_template('update_developer.html',
                           dv_id = dv.id,
                           dv_name=dv.name,
                           dv_surname=dv.surname,
                           dv_patronymic=dv.patronymic,
                           sd_surname=dv.sd.surname,
                           sd_name=dv.sd.name,
                           sd_patronymic=dv.sd.patronymic,
                           dv=dv,
                           sd=sd)

if __name__ == '__main__':
    app.run()


