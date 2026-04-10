# import mysql.connector




# conn = mysql.connector.connect(
#     host="sql.freedb.tech",
#     user="freedb_h4xgroover",
#     password="9P*H2*Xv8wZU#%U",
#     database="freedb_academix",

#     port=3306

# )

# def get_con():
#     try:
#         conn = mysql.connector.connect(
#             host="sql.freedb.tech",
#             user="freedb_h4xgroover",
#             password="9P*H2*Xv8wZU#%U",
#             database="freedb_academix",
#             port=3306
#         )
       
#         print("Connexion réussie à la base de données")
#         return conn
   
#     except mysql.connector.Error as err:
#         print(f"Erreur de connexion à la base de données : {err}")
#         return None
    
# import random 

# import faker



# def inser(n=800):
#     db =get_con()
#     if db is None:
#         print("Impossible de se connecter à la base de données. Insertion annulée.")
#         return
    
#     cursor = db.cursor()
#     fake = faker.Faker()
#     for _ in range(n):
#         id = random.randint(1, 1000)
#         nom = fake.name()[0:20]  # Limiter la longueur du nom à 20 caractères
#         # inserer maintenta
#         query ="insert into Test (id,nom) values (%s,%s)"
#         cursor.execute(query, (id, nom))
#     db.commit()
#     cursor.close()
#     db.close()

# if __name__ == "__main__":
#     inser()
