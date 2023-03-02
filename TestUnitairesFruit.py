import unittest
import json
from app import app
from pymongo import MongoClient

class TestFruitsAPI(unittest.TestCase):
    
    @classmethod
    def setUpClass(cls):
        # Connexion à la base de données de test
        cls.client = MongoClient('mongodb://localhost:27017/')
        cls.db = cls.client['test_database']
        # Initialisation de la collection de fruits avec 4 fruits
        cls.db.fruits.insert_many([
            {"nom": "Pomme", "couleur": "Rouge", "saveur": "Sucrée"},
            {"nom": "Orange", "couleur": "Orange", "saveur": "Acide"},
            {"nom": "Banane", "couleur": "Jaune", "saveur": "Sucrée"},
            {"nom": "Ananas", "couleur": "Jaune", "saveur": "Acide"}
        ])
        # Configuration de l'application Flask pour les tests
        app.config['TESTING'] = True
        app.config['MONGO_URI'] = 'mongodb://localhost:27017/test_database'
        cls.app = app.test_client()

    @classmethod
    def tearDownClass(cls):
        # Nous verifions la Suppression de la collection de fruits de test
        cls.db.fruits.drop()

    def test_list_fruits(self):
        # Nous verifions que la liste des fruits est retournée avec succès
        response = self.app.get('/fruits')
        self.assertEqual(response.status_code, 200, "La requête pour obtenir la liste des fruits a échoué")
        self.assertEqual(len(json.loads(response.data)), 4, "Le nombre de fruits retournés est incorrect")

    def test_get_fruit(self):
        # Nous verifions qu'un fruit spécifique est retourné avec succès
        response = self.app.get('/fruits/1')
        self.assertEqual(response.status_code, 200, "La requête pour obtenir un fruit spécifique a échoué")
        self.assertEqual(json.loads(response.data)['nom'], 'Orange', "Le fruit retourné est incorrect")

    def test_add_fruit(self):
        # Nous verifions aussi qu'un nouveau fruit est ajouté avec succès
        new_fruit = {"nom": "Fraise", "couleur": "Rouge", "saveur": "Sucrée"}
        response = self.app.post('/fruits', json=new_fruit)
        self.assertEqual(response.status_code, 201, "La requête pour ajouter un nouveau fruit a échoué")
        self.assertEqual(json.loads(response.data)['nom'], 'Fraise', "Le fruit ajouté est incorrect")

    def test_update_fruit(self):
        # Nous verifions ensuite qu'un fruit existant est mis à jour avec succès
        updated_fruit = {"nom": "Banane", "couleur": "Vert", "saveur": "Acide"}
        response = self.app.put('/fruits/2', json=updated_fruit)
        self.assertEqual(response.status_code, 200, "La requête pour mettre à jour un fruit a échoué")
        self.assertEqual(json.loads(response.data)['couleur'], 'Vert', "Le fruit mis à jour est incorrect")

    def test_delete_fruit(self):
        # Nous verifions enfin qu'un fruit existant est supprimé avec succès
        response = self.app.delete('/fruits/4')
        self.assertEqual(response.status_code, 204, "La requête pour supprimer un fruit a échoué")

if __name__ == '__main__':
    unittest.main()