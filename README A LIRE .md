INFORMATION SUPPLEMENTAIRE

# TESTS-UNITAIRES-LINUS-QUENUM



Voici quelques commandes curl pour tester les opérations CRUD de l'API RESTful Flask pour les fruits :

Obtenir tous les fruits de la collection :
curl http://localhost:5000/fruits


Obtenir un fruit spécifique par son ID :
curl http://localhost:5000/fruits/<fruit_id>
où <fruit_id> est l'ID du fruit que je souhaite récupérer.


Ajouter un nouveau fruit à la collection :
curl -X POST -H "Content-Type: application/json" -d '{"nom":"Banane", "couleur":"Jaune", "saveur":"Sucrée"}' http://localhost:5000/fruits


Mettre à jour un fruit existant dans la collection :
curl -X PUT -H "Content-Type: application/json" -d '{"nom":"Banane", "couleur":"Vert", "saveur":"Acide"}' http://localhost:5000/fruits/<fruit_id>
où <fruit_id> est l'ID du fruit que je souhaite mettre à jour.


Supprimer un fruit de la collection :
curl -X DELETE http://localhost:5000/fruits/<fruit_id>


Testes Unitaires

je n'utilise pas la bibliothèque requests pour effectuer les requêtes HTTP. 
Au lieu de cela, j'utilise la méthode app.test_client() fournie par Flask, 
qui permet de simuler des requêtes HTTP dans le contexte de l'application Flask en cours d'exécution.

Cela est  pratique pour les tests unitaires car cela permet de tester l'API sans avoir besoin de démarrer un serveur HTTP séparé. 
Cela permet également de bénéficier des fonctionnalités intégrées de Flask, 
comme la gestion automatique des sessions et des cookies, pour simplifier les tests.

