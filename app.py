from flask import Flask, jsonify, request
from pymongo import MongoClient
from bson.objectid import ObjectId

# Initialisation de l'application Flask 
app = Flask(__name__)

# Fonction pour convertir ObjectId en str
def id_str(doc):
    doc['_id'] = str(doc['_id'])
    return doc

# Connexion à la base de données MongoDB
client = MongoClient('localhost', 27017)
db = client['fruit_db']
collection = db['fruits']


# Voici ma 1ere Fonction qui récupère tous les fruits de la collection
@app.route('/fruits', methods=['GET'])
def obtenir_fruits():
    fruits = []
    for fruit in collection.find():
        fruits.append({
            'id': str(fruit['_id']),
            'nom': fruit['nom'],
            'couleur': fruit['couleur'],
            'saveur': fruit['saveur']
        })
    return jsonify({'fruits': fruits})

# Voici ma 2eme Fonction qui récupère un fruit spécifique par son ID
@app.route('/fruits/<string:fruit_id>', methods=['GET'])
def obtenir_fruit(fruit_id):
    fruit = collection.find_one({'_id': ObjectId(fruit_id)})
    if fruit:
        return jsonify({
            'id': str(fruit['_id']),
            'nom': fruit['nom'],
            'couleur': fruit['couleur'],
            'saveur': fruit['saveur']
        })
    else:
        return jsonify({'message': 'Fruit non trouvé'})

# Voici ma 3 eme Fonction qui ajoute un nouveau fruit à la collection
@app.route('/fruits', methods=['POST'])
def ajouter_fruit():
    nom = request.json['nom']
    couleur = request.json['couleur']
    saveur = request.json['saveur']
    fruit_id = collection.insert_one({
        'nom': nom,
        'couleur': couleur,
        'saveur': saveur
    }).inserted_id
    return jsonify({'id': str(fruit_id), 'nom': nom, 'couleur': couleur, 'saveur': saveur})

# Voici ma 4eme Fonction qui met à jour un fruit existant dans la collection
@app.route('/fruits/<string:fruit_id>', methods=['PUT'])
def mettre_a_jour_fruit(fruit_id):
    fruit = collection.find_one_and_update(
        {'_id': ObjectId(fruit_id)},
        {'$set': {
            'nom': request.json['nom'],
            'couleur': request.json['couleur'],
            'saveur': request.json['saveur']
        }},
        return_document=True
    )
    if fruit:
        return jsonify({
            'id': str(fruit['_id']),
            'nom': fruit['nom'],
            'couleur': fruit['couleur'],
            'saveur': fruit['saveur']
        })
    else:
        return jsonify({'message': 'Le Fruit na pas été trouvé'})

# Voici ma derniere Fonction qui supprime un fruit de la collection
@app.route('/fruits/<string:fruit_id>', methods=['DELETE'])
def supprimer_fruit(fruit_id):
    result = collection.delete_one({'_id': ObjectId(fruit_id)})
    if result.deleted_count == 1:
        return jsonify({'message': 'Votre Fruit a été supprimé'})
    else:
        return jsonify({'message': 'Le Fruit na pas été trouvé'})

# Lancement de l'application Flask
if __name__ == '__main__':
    app.run(debug=True)
