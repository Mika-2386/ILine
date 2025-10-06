from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import relationship

db = SQLAlchemy()

# ------таблица генералный директор------------

class General_manager(db.Model):
    __tablename__ = "general_manager"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    surname = db.Column(db.String)
    patronymic = db.Column(db.String)

    id_salary_general_manager = db.Column(db.Integer, db.ForeignKey("salary_general_manager.id", ondelete="SET NULL"))
    salary_g = relationship("Salary_general_manager", back_populates="general") # связь с зарплатной таблицей saslry_general_manager
    managers_ = relationship("Manager", back_populates="general") #связь с таблицей manager


    def __repr__(self):
         return f"General_manager(surname={self.surname!r})"
# --------- таблица з/п генерального директора
class Salary_general_manager(db.Model):
    __tablename__ = "salary_general_manager"
    id = db.Column(db.Integer, primary_key=True)
    post = db.Column(db.String)
    salary = db.Column(db.Integer)

    general = relationship("General_manager", back_populates="salary_g")

    def __repr__(self):
         return f"Salary_general_manager(post={self.post!r})"


# ------------- таблица менеджер
class Manager (db.Model):
    __tablename__ = "manager"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    surname = db.Column(db.String)
    patronymic = db.Column(db.String)

    id_salary_manager = db.Column(db.Integer, db.ForeignKey("salary_manager.id", ondelete="SET NULL"))
    salary_m = relationship("Salary_manager", back_populates="managers_") # связь с тбл. з.п. менеджеров
    id_general_manager = db.Column(db.Integer, db.ForeignKey("general_manager.id", ondelete="SET NULL")) # связь с таб. генеральный директор
    general = relationship("General_manager", back_populates="managers_") # ссылка на табл. генеральный директор
    group = relationship("Group_leader", back_populates="managers_") # ссылка на табл. руководитель группы


    def __repr__(self):
         return f"Manager(surname={self.surname!r})"

class Salary_manager(db.Model):
    __tablename__ = "salary_manager"
    id = db.Column(db.Integer, primary_key=True)
    post = db.Column(db.String)
    salary = db.Column(db.Integer)

    managers_ = relationship("Manager", back_populates="salary_m")

    def __repr__(self):
        return f"Salary_manager(post={self.post!r})"

class Group_leader (db.Model):
    __tablename__ = "group_leader"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    surname = db.Column(db.String)
    patronymic = db.Column(db.String)

    id_salary_group_leader = db.Column(db.Integer, db.ForeignKey("salary_group_leader.id", ondelete="SET NULL"))
    salary_gr = relationship("Salary_group_leader", back_populates="group")
    id_manager = db.Column(db.Integer, db.ForeignKey("manager.id", ondelete="SET NULL"))
    managers_ = relationship("Manager", back_populates="group")
    sd = relationship("Senior_developer", back_populates="group")



    def __repr__(self):
         return f"Group_leader(surname={self.surname!r})"

class Salary_group_leader (db.Model):
    __tablename__ = "salary_group_leader"
    id = db.Column(db.Integer, primary_key=True)
    post = db.Column(db.String)
    salary = db.Column(db.Integer)
#
    group = relationship("Group_leader", back_populates="salary_gr")
#
    def __repr__(self):
        return f"Salary_group_leader(post={self.post!r})"

class Senior_developer (db.Model):
    __tablename__ = "senior_developer"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    surname = db.Column(db.String)
    patronymic = db.Column(db.String)

    id_salary_senior_developer = db.Column(db.Integer, db.ForeignKey("salary_senior_developer.id", ondelete="SET NULL"))
    salary_sd = relationship("Salary_senior_developer", back_populates="sd")
    id_group_leader = db.Column(db.Integer, db.ForeignKey("group_leader.id", ondelete="SET NULL"))
    group = relationship("Group_leader", back_populates="sd")
    dv = relationship("Developer", back_populates="sd")


    def __repr__(self):
         return f"Senior_developer(surname={self.surname!r})"

class Salary_senior_developer (db.Model):
    __tablename__ = "salary_senior_developer"
    id = db.Column(db.Integer, primary_key=True)
    post = db.Column(db.String)
    salary = db.Column(db.Integer)

    sd = relationship("Senior_developer", back_populates="salary_sd")

    def __repr__(self):
        return f"Salary_senior_developer(post={self.post!r})"

class Developer(db.Model):
    __tablename__ = "developer"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    surname = db.Column(db.String)
    patronymic = db.Column(db.String)

    id_salary_developer = db.Column(db.Integer, db.ForeignKey("salary_developer.id", ondelete="SET NULL"))
    salary_d = relationship("Salary_developer", back_populates="dv")
    id_senior_developer = db.Column(db.Integer, db.ForeignKey("senior_developer.id", ondelete="SET NULL"))
    sd = relationship("Senior_developer", back_populates="dv")

    def __repr__(self):
        return f"Developer(surname={self.surname!r})"

class Salary_developer(db.Model):
    __tablename__ = "salary_developer"
    id = db.Column(db.Integer, primary_key=True)
    post = db.Column(db.String)
    salary = db.Column(db.Integer)

    dv = relationship("Developer", back_populates="salary_d")

    def __repr__(self):
        return f"Salary_developer(post={self.post!r})"