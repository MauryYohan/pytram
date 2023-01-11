# -------------------------------------------------------------------------------------------------------------------- #
# ------------------------------------------------------- DATA ------------------------------------------------------- #
# -------------------------------------------------------------------------------------------------------------------- #
troncon_principal_tram_a = [
    "Le Haillan Rostand", "Les Pins", "Frères Robinson", "Hôtel de Ville Mérignac", "Pin Galant", "Mérignac Centre",
    "Lycées de Mérignac", "Quatre Chemins", "Pierre Mendès-France", "Alfred de Vigny", "Fontaine d'Arlac", "Peychotte",
    "François Mitterrand", "Saint-Augustin", "Hôpital Pellegrin", "Stade Chaban-Delmas", "Gaviniès", "Hôtel de Police",
    "Saint-Bruno - Hôtel de Région", "Mériadeck", "Palais de Justice", "Hôtel de Ville", "Sainte-Catherine",
    "Place du Palais", "Porte de Bourgogne", "Stalingrad", "Jardin botanique", "Thiers - Benauge", "Galin", "Jean Jaurès",
    "Cenon Gare", "Carnot - Mairie de Cenon", "Buttinière"
]
troncon_principal_tram_b = [
    "Berges de la Garonne", "Claveau", "Brandenburg", "New-York", "Rue Achard", "Bassins à Flot", "Les Hangars",
    "Cours du Médoc", "Chartrons", "CAPC (Musée d'Art Contemporain)", "Quinconces", "Grand Théâtre", "Gambetta",
    "Hôtel de Ville", "Musée d'Aquitaine", "Victoire", "Saint-Nicolas", "Bergonié", "Barrière Saint-Genès", "Roustaing",
    "Forum", "Peixotto", "Béthanie", "Arts et Métiers", "François Bordes", "Doyen Brus", "Montaigne-Montesquieu",
    "UNITEC", "Saige", "Bougnard"
]
troncon_principal_tram_c = [
    "Parc des Expositions", "Palais des Congrès", "Quarante Journaux", "Berges du lac", "Les Aubiers",
    "Place Ravezies-Le Bouscat", "Grand Parc", "Émile Counord", "Camille Godard", "Place Paul Doumer", "Jardin Public",
    "Quinconces", "Place de la Bourse", "Porte de Bourgogne", "Saint-Michel", "Sainte-Croix", "Tauzia", "Gare Saint-Jean",
    "Belcier", "Carle Vernet", "Bègles Terres Neuves", "La Belle Rose", "Stade Musard", "Calais – Centujean",
    "Gare de Bègles", "Parc de Mussonville", "Lycée Vaclav Havel"
]
troncon_principal_tram_d = [
    "Quinconces", "Charles Gruet", "Marie Brizard", "Barrière du Médoc", "Courbet", "Calypso", "Mairie du Bouscat",
    "Les Ecus", "Sainte-Germaine", "Hippodrome", "Le Sulky", "Toulouse Lautrec", "Picot", "Eysines Centre",
    "Les Sources", "Cantinolle"
]

lines = {
    'A': troncon_principal_tram_a,
    'B': troncon_principal_tram_b,
    'C': troncon_principal_tram_c,
    'D': troncon_principal_tram_d
}

# -------------------------------------------------------------------------------------------------------------------- #
# ----------------------------------------------------- FUNCTION ----------------------------------------------------- #
# -------------------------------------------------------------------------------------------------------------------- #
def find_stop(stop_name):
    """ Jalon 1 : Retrouver la ou les lignes de tram qui possède le nom de l'arrêt saisi par l'utilisateur \n
    :param stop_name: Le nom de l'arrêt
    :return: Retourne la liste des lignes auxquels cet arrêt corresponds
    """
    return [tram_line for tram_line, line_stop in lines.items() if stop_name in line_stop]

def find_terminal(_lines):
    """ Jalon 2 : recherche les arrêts particuliers (terminus) \n
    :param _lines: Dictionnaire contenant l'ensemble des lignes du réseau de tram \n
    :return: La liste des terminus de chaque ligne
    """
    _terminus = []
    for line in _lines.values():
        _terminus.append(line[0])
        _terminus.append(line[-1])
    return _terminus

def find_transfer_stops(_lines):
    """ Jalon 3 : recherche les arrêts particuliers (correspondance)
    :param _lines: Dictionnaire contenant l'ensemble des lignes du réseau de tram \n
    :return: La liste des correspondances du réseau
    """
    seen = set()
    duplicate = set()
    for line in _lines.values():
        for stop in line:
            seen.add(stop) if stop not in seen else duplicate.add(stop)
    return list(duplicate)

def check_same_line(_departure, _arrival):
    """ Jalon 4 : Recherche si le départ et l'arrivée sont sur la même ligne, sans bifurcation \n
    :param _departure: Arret de départ
    :param _arrival: Arret d'arrivée
    :return: A, B, C ou D selon la ligne commune
    """
    if _departure in troncon_principal_tram_a and _arrival in troncon_principal_tram_a:
        return "A"
    elif _departure in troncon_principal_tram_b and _arrival in troncon_principal_tram_b:
        return "B"
    elif _departure in troncon_principal_tram_c and _arrival in troncon_principal_tram_c:
        return "C"
    elif _departure in troncon_principal_tram_d and _arrival in troncon_principal_tram_d:
        return "D"
    else:
        return None

def define_transfer_stop(_departure, _arrival, _connection):
    """ Jalon 5 : Recherche un ou des arrêts de correspondance lorsque le départ et l'arrivée sont sur des lignes
    différentes \n
    :param _departure: Arrêt de départ
    :param _arrival: Arrêt d'arrivée
    :param _connection: Arrêt de correspondance
    :return: Retourne la correspondance
    """
    the_lines = find_stop(_departure) + find_stop(_arrival)
    for stop in _connection:
        if find_stop(stop) == the_lines:
            return stop
    return _connection[0]

def find_direction(_departure, _arrival):
    """ Jalon 6 : Trajet sur la même ligne, déterminer le sens depuis le départ. \n
    Jalon 7 : Trajet sur des lignes différentes, déterminer le sens depuis le départ, vers l'arrêt de correspondance. \n
    :param _departure: Arrêt de départ
    :param _arrival: Arrêt d'arrivée
    :return: Le sens de la direction (direct ou inverse)
    """
    intersection = list(filter(lambda x: x in matching_lines_departure, matching_lines_arrival))
    if intersection == ['A']:
        return "direct" if troncon_principal_tram_a.index(_departure) < troncon_principal_tram_a.index(_arrival) else "inverse"
    elif intersection == ['B']:
        return "direct" if troncon_principal_tram_b.index(_departure) < troncon_principal_tram_b.index(_arrival) else "inverse"
    elif intersection == ['C']:
        return "direct" if troncon_principal_tram_c.index(_departure) < troncon_principal_tram_c.index(_arrival) else "inverse"
    elif intersection == ['D']:
        return "direct" if troncon_principal_tram_d.index(_departure) < troncon_principal_tram_d.index(_arrival) else "inverse"
    else:
        return None

def count_stops(_departure, _arrival):
    """ Jalon 8 & 9 : Comptabiliser le nombre d'arrêts. \n
    :param _departure: Arrêt de départ
    :param _arrival: Arrêt d'arrivée (ou de correspondance pour le jalon 9)
    :return: Le nombre d'arrêt à faire dans le trajet
    """
    intersection = list(filter(lambda x: x in matching_lines_departure, matching_lines_arrival))
    line_list = []
    if intersection == ['A']:
        line_list = troncon_principal_tram_a
    elif intersection == ['B']:
        line_list = troncon_principal_tram_b
    elif intersection == ['C']:
        line_list = troncon_principal_tram_c
    elif intersection == ['D']:
        line_list = troncon_principal_tram_d
    try:
        start_index = line_list.index(_departure)
        end_index = line_list.index(_arrival)
        return abs(end_index - start_index)
    except ValueError:
        return 0


# -------------------------------------------------------------------------------------------------------------------- #
# ---------------------------------------------------- MAIN CODE ----------------------------------------------------- #
# -------------------------------------------------------------------------------------------------------------------- #
# [JALON 1] - Retrouver la ou les lignes de tram qui possède le nom de l'arrêt saisi par l'utilisateur
departure = input("Saisir votre arrêt de départ: ")
arrival = input("Saisir votre arrêt de destination: ")
matching_lines_departure = find_stop(departure)
matching_lines_arrival = find_stop(arrival)

# [JALON 2] - Recherche les arrêts particuliers (terminus)
terminus = find_terminal(lines)

# [JALON 3] - Recherche les arrêts particuliers (connection)
connection = find_transfer_stops(lines)

# [JALON 4] - Recherche si le départ et l'arrivée sont sur la même ligne, ligne sans bifurcation
same_line = check_same_line(departure, arrival)

# [JALON 5] - Recherche les arrêts de correspondance lorsque le départ et l'arrivée sont sur des lignes différentes
if same_line is None:
    transfert_stop = define_transfer_stop(departure, arrival, connection)
    print("Voici les arrêts de connection possible :", transfert_stop)
    # [JALON 10] - Compter le nombre de correspondances, useless parce que nous ne gérons le cas que d'une seule
    # correspondance (vu en cours)
    print(len(transfert_stop))
    # [JALON 7] - Determiner le sens depuis l'arrêt de départ vers l'arrêt de correspondance
    direction = find_direction(departure, transfert_stop)
    print(direction)
    # [JALON 9] - Compter le nombre d'arrêts sur le trajet (ligne différente)
    stop_first = count_stops(departure, transfert_stop)
    stop_second = count_stops(transfert_stop, arrival)
    print(stop_first + stop_second)
else:
    # [JALON 6] - Trajet sur la même ligne, déterminer le sens depuis le départ
    direction = find_direction(departure, arrival)
    print(direction)
    # [JALON 8] - Compter le nombre d'arrêts sur le trajet (meme ligne)
    stop_count = count_stops(departure, arrival)
    print(stop_count)
