"""
Ce module représente l'échiquier.

C'est lui qui va gérer les événements des joueurs et prendre en charge l'affichage du jeu sur l'écran. Pour ce faire,
nous avons besoin des packages pygame et chess. Pygame est le moteur de jeu qui réagit aux clicks des souris. chess lui
est le moteur de jeu d'échecs, celui qui valide si le mouvement proposé par le joueur est valide.

Ce module est composé de plusieurs éléments:
1. Une classe pour décrire une pièce du jeu particulière
2. Une classe pour décrire l'échiquier lui-même.
3. Une initiale pour chaque type de pièce, afin de représenter un mouvement.


Kings move one square in any direction, so long as that square is not attacked by an enemy piece. Additionally,
kings are able to make a special move,
know as castling.
Queens move diagonally, horizontally, or vertically any number of squares. They are unable to jump over pieces.
Rooks move horizontally or vertically any number of squares. They are unable to jump over pieces.
Rooks move when the king castles.
Bishops move diagonally any number of squares. They are unable to jump over pieces.
Knights move in an ‘L’ shape’: two squares in a horizontal or vertical direction,
then move one square horizontally or vertically. They are the only piece able to jump over other pieces.
Pawns move vertically forward one square, with the option to move two squares if they have not yet moved.
Pawns are the only piece to capture different to how they move. Pawns capture one square diagonally in a forward direction.
Pawns are unable to move backward on captures or moves. Upon reaching the other side of the board a pawn promotes
into any other piece, except for a king. Additionally, pawns can make a special move named En Passant.

"""
import chess
import pygame
import sys


# We code the dictionary which represents the chess pieces. The initials are used to describe the piece when it is
# movement. For example 'e5' represents the movement of a pawn towards the e5 square, while Nb3 represents the movement
# of a jumper to box b3.
piece_initiale = {
    'Roi': 'K',
    'Dame': 'D',
    'Fou': 'B',
    'Cavalier': 'N',
    'Tour': 'R',
    'Pion': ''
}


class Piece:
    """
    Représente une simple pièce d'échec.


    A part has a name and a color. It also has a box, and therefore has coordinates on the screen. It
    finally has an image, and a reference to the playing surface to display.
    """
    def __init__(self, nom, couleur, x, y, taille, image, ecran):
        self.nom = nom
        self.couleur = couleur
        self.x = x
        self.y = y
        self.ecran = ecran
        self.image = image

    def affiche(self):
        """

        This method forces the part to be displayed on the screen

        A rectangle of the playing surface is redefined for its display. To display the rectangle, we will have
        need to know the coordinates of its top left corner. These will be the coordinates possessed by the
        piece itself. The size of the rectangle will come from the dimension of the image itself.

             (x, y)
                  +------largeur --------+
                  |                      |
                  |                      |
              longueur                   |  <----- Zone a afficher sur l'ecran.
                  |                      |
                  |                      |
                  +----------------------+
        """
        r = self.image.get_rect()       # We get the size of the image to display
        r.topleft = self.x, self.y      # We pass the coordinates of the room as the top left corner of the rectangle
        self.ecran.blit(self.image, r)  # We display the image in the rectangle created inside the screen area

    def case(self):
        """
        Returns the corresponding box of the part displayed on the screen.
        """
        return chr(97 + (self.x // 85)) + str(((680 - self.y) // 85))

    def get_colour(self):
        return self.couleur

class Echiquier:
    """
    Represents a chess board.
    """
    def __init__(self, ecran, echiquier, image):
        self.make_move = False
        self.move_coord = ""
        self.last_move = ""
        self.moteur = chess.Board()  # Motor will validate if the movements are valid.
        self.ecran = ecran
        self.echiquier = echiquier
        self.pieces = [Piece("Roi",      "Noir",  85 * 4, 0,      85, self._image(image, (68, 70, 85, 85)),   ecran),
                       Piece("Dame",     "Noir",  85 * 3, 0,      85, self._image(image, (234, 70, 85, 85)),  ecran),
                       Piece("Tour",     "Noir",  85 * 0, 0,      85, self._image(image, (400, 70, 85, 85)),  ecran),
                       Piece("Tour",     "Noir",  85 * 7, 0,      85, self._image(image, (400, 70, 85, 85)),  ecran),
                       Piece("Fou",      "Noir",  85 * 2, 0,      85, self._image(image, (566, 70, 85, 85)),  ecran),
                       Piece("Fou",      "Noir",  85 * 5, 0,      85, self._image(image, (566, 70, 85, 85)),  ecran),
                       Piece("Cavalier", "Noir",  85 * 1, 0,      85, self._image(image, (736, 70, 85, 85)),  ecran),
                       Piece("Cavalier", "Noir",  85 * 6, 0,      85, self._image(image, (736, 70, 85, 85)),  ecran),
                       Piece("Pion",     "Noir",  85 * 0, 85,     85, self._image(image, (902, 70, 85, 85)),  ecran),
                       Piece("Pion",     "Noir",  85 * 1, 85,     85, self._image(image, (902, 70, 85, 85)),  ecran),
                       Piece("Pion",     "Noir",  85 * 2, 85,     85, self._image(image, (902, 70, 85, 85)),  ecran),
                       Piece("Pion",     "Noir",  85 * 3, 85,     85, self._image(image, (902, 70, 85, 85)),  ecran),
                       Piece("Pion",     "Noir",  85 * 4, 85,     85, self._image(image, (902, 70, 85, 85)),  ecran),
                       Piece("Pion",     "Noir",  85 * 5, 85,     85, self._image(image, (902, 70, 85, 85)),  ecran),
                       Piece("Pion",     "Noir",  85 * 6, 85,     85, self._image(image, (902, 70, 85, 85)),  ecran),
                       Piece("Pion",     "Noir",  85 * 7, 85,     85, self._image(image, (902, 70, 85, 85)),  ecran),
                       Piece("Roi",      "Blanc", 85 * 4, 85 * 7, 85, self._image(image, (68, 214, 85, 85)),  ecran),
                       Piece("Dame",     "Blanc", 85 * 3, 85 * 7, 85, self._image(image, (234, 214, 85, 85)), ecran),
                       Piece("Tour",     "Blanc", 85 * 0, 85 * 7, 85, self._image(image, (400, 214, 85, 85)), ecran),
                       Piece("Tour",     "Blanc", 85 * 7, 85 * 7, 85, self._image(image, (400, 214, 85, 85)), ecran),
                       Piece("Fou",      "Blanc", 85 * 2, 85 * 7, 85, self._image(image, (566, 214, 85, 85)), ecran),
                       Piece("Fou",      "Blanc", 85 * 5, 85 * 7, 85, self._image(image, (566, 214, 85, 85)), ecran),
                       Piece("Cavalier", "Blanc", 85 * 1, 85 * 7, 85, self._image(image, (736, 214, 85, 85)), ecran),
                       Piece("Cavalier", "Blanc", 85 * 6, 85 * 7, 85, self._image(image, (736, 214, 85, 85)), ecran),
                       Piece("Pion",     "Blanc", 85 * 0, 85 * 6, 85, self._image(image, (902, 214, 85, 85)), ecran),
                       Piece("Pion",     "Blanc", 85 * 1, 85 * 6, 85, self._image(image, (902, 214, 85, 85)), ecran),
                       Piece("Pion",     "Blanc", 85 * 2, 85 * 6, 85, self._image(image, (902, 214, 85, 85)), ecran),
                       Piece("Pion",     "Blanc", 85 * 3, 85 * 6, 85, self._image(image, (902, 214, 85, 85)), ecran),
                       Piece("Pion",     "Blanc", 85 * 4, 85 * 6, 85, self._image(image, (902, 214, 85, 85)), ecran),
                       Piece("Pion",     "Blanc", 85 * 5, 85 * 6, 85, self._image(image, (902, 214, 85, 85)), ecran),
                       Piece("Pion",     "Blanc", 85 * 6, 85 * 6, 85, self._image(image, (902, 214, 85, 85)), ecran),
                       Piece("Pion",     "Blanc", 85 * 7, 85 * 6, 85, self._image(image, (902, 214, 85, 85)), ecran)]

    def jouer(self,colour):
        """
        This is where the game loop is located, in which the image of the chess board is refreshed.
        """
        play = True
        while play:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit(0)

                elif event.type == pygame.MOUSEBUTTONDOWN:
                    # Mouse click or press
                    if event.button == 1:
                        x, y = event.pos
                        print(x, y)
                        print("self.moteur = ", self.moteur)
                        print("From position: ", chr(97 + (x // 85)) + str(((680 - y) // 85) + 1))
                        curr_pos = chr(97 + (x // 85)) + str(((680 - y) // 85) + 1)


                elif event.type == pygame.MOUSEBUTTONUP:
                    # Mouse release
                    if event.button == 1:
                        x, y = event.pos
                        print(x, y)
                        # Calculating the final position by dividing with 85 ( side length of square) and taking
                        # the closest integer just below the value by forcing the result to be of int()
                        x_new = int(x / 85) * 85
                        y_new = int(y / 85) * 85
                        # print("To position: ", chr(97 + (x // 85)) + str(((680 - y) // 85) + 1))
                        final_pos = chr(97 + (x // 85)) + str(((680 - y) // 85) + 1)
                        check_move = curr_pos + final_pos
                        # print("check move", check_move)
                        new_pos = 0
                        for p in self.pieces:
                            # Get the piece in the given position calculated as curr_pos
                            print("p.get_colour()",p.get_colour())
                            print("get_colour()",colour)

                            if p.case() == curr_pos and p.get_colour()==colour:
                                valid_moves = self.moteur.generate_legal_moves()
                                move_made = chess.Move.from_uci(check_move)
                                self.make_move = False
                                for k in valid_moves:
                                    print("k =", k)
                                    if k == move_made:
                                        self.make_move = True
                                if self.make_move:
                                    p.x = x_new
                                    p.y = y_new
                                    self.moteur.push(move_made)
                                    self.pieces[new_pos] = p
                                    self.last_move = check_move
                                    #If the x value is not 3 digits, make it 3 digit by putting a 0 before the value
                                    # First the x and y values are converted to strings
                                    x_new_str = str(x_new)
                                    y_new_str = str(y_new)
                                    #Puts 0 until the length is 3
                                    while len(x_new_str)<3:
                                        x_new_str = "0" + x_new_str
                                    while len(y_new_str) < 3:
                                         y_new_str = "0" + x_new_str
                                    #This is the string which is passed to the server
                                    self.move_coord = str(x_new_str) + str(y_new_str)

                                    play = False
                            new_pos += 1
            self.update_screen()

    def make_auto_move(self, data):
        print("data =",data)
        curr_pos = data[0:2]
        print("curr_pos new",curr_pos)
        check_move = data[0:4]
        x_new = int(data[4:7])
        y_new = int(data[7:10])
        new_pos = 0
        for p in self.pieces:
            # Get the piece in the given position calculated as curr_pos
            if p.case() == curr_pos:
                move_made = chess.Move.from_uci(check_move)
                p.x = x_new
                p.y = y_new
                self.moteur.push(move_made)
                self.pieces[new_pos] = p
                self.last_move = check_move
            new_pos += 1
        self.update_screen()

    def update_screen(self):
            self.ecran.fill((255, 255, 255))
            self.ecran.blit(self.echiquier, self.echiquier.get_rect())

            [p.affiche() for p in self.pieces]
            pygame.display.update()

    def _image(self, image, pos):
        """
        Generates the image piece from the general image of the chess game
        """
        r = pygame.Rect(pos)
        obj = pygame.Surface(r.size).convert()
        obj.blit(image, (0, 0), r)
        return obj


def nouvelle_partie(sid):
    """
    This is where we create a new game.

    The function returns a chessboard and its pieces arranged to start a game.
    """
    pygame.init()                                # Initialisation du moteur de jeu pygame
    ecran = pygame.display.set_mode((680, 680))  # On cree une fenetre de 680 pixel par 680 pixels
    pygame.display.set_caption("Echecs : " + sid)         # Le titre de la fenetre s'appelle Echecs

    echiquier = pygame.Surface((680, 680))       # On definit une surface a l'ecran pour representer l'echiquier
    echiquier.fill((175, 141, 120))              # Que l'on peint en marron (uni) voici le RGB(175, 141, 120)

    # The following lines allow you to paint the boxes of the chessboard in a slightly different brown
    # previously defined
    for x in range(0, 8, 2):
        for y in range(0, 8, 2):
            pygame.draw.rect(echiquier, (250, 240, 230), (x * 85, y * 85, 85, 85))

    for x in range(1, 9, 2):
        for y in range(1, 9, 2):
            pygame.draw.rect(echiquier, (250, 240, 230), (x * 85, y * 85, 85, 85))

    #Here, we finally create the chess game as well as the new pieces to display
    return Echiquier(ecran, echiquier, pygame.image.load("ressources/img.png").convert())


if __name__ == '__main__':
    partie = nouvelle_partie()
    partie.jouer()
