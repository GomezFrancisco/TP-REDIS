# import redis

# def connect_db():
#     conexion = redis.StrictRedis(port=6379, db=0, host="db-redis")
#     if(conexion.ping()):
#         print("conectado a redis")
#     else:
#         print("error de conexion con redis")
#     return conexion

# def get_list(nombre):
#     db = connect_db()
#     db.lpush(nombre, "luke, leia, han, chewbbaca")
#     lista = db.lrange(nombre,0,-1)
#     return lista

# connectiondb.py
import redis
import json
from utils import mandalorian_episodes

def connect_db():
    return redis.StrictRedis(port=6379, db=0, host="db-redis", decode_responses=True)

def init_episodes():
    db = connect_db()
    for ep in mandalorian_episodes:
        key = f"ep_s{ep['temporada']}_e{ep['capitulo']}"
        if not db.exists(key):  # Solo si aún no se cargó
            db.set(key, json.dumps(ep))

def listar_capitulos():
    db = connect_db()
    keys = sorted(db.keys("ep_s*_e*"))
    lista = []
    for key in keys:
        cap = json.loads(db.get(key))
        cap["id"] = key
        lista.append(cap)
    return lista

def reservar_capitulo(id_capitulo):
    db = connect_db()
    cap = json.loads(db.get(id_capitulo))
    if cap["estado"] == "disponible":
        cap["estado"] = "reservado"
        db.set(id_capitulo, json.dumps(cap), ex=240)  # 4 min reserva
        return True
    return False

def confirmar_pago(id_capitulo, precio):
    db = connect_db()
    cap = json.loads(db.get(id_capitulo))
    if cap["estado"] == "reservado":
        cap["estado"] = "alquilado"
        cap["precio"] = precio
        db.set(id_capitulo, json.dumps(cap), ex=86400)  # 24 hs
        return True
    return False
