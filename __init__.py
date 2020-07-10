import math
import os
import random
import arcade

covids = 100
escala = 0.5
espacciofuera = 300
ancho = 800
largo = 600
titulo = "Cuarentena si puedes"
limiteizq = -espacciofuera
limitede = ancho + espacciofuera
limiteabajo = -espacciofuera
limitearriba = ancho + espacciofuera

#Creamos clase para definir el giro de Miguel
class spritegiro(arcade.Sprite):
    def update(self):
        super().update()
        self.angle = math.degrees(math.atan2(self.change_y, self.change_x))



#Clase para Miguel
class elmaster(arcade.Sprite):
                                            #def __init__ es una función especial llamada "constructor"
                                            #self "mi" nos referimos al campo de dirección (no se puede poner en una def distinta)
                                            #método= función dentro de una clase, definimos los atributos primero con el init y luego los métodos


    def __init__(self, archivo, escala):
        super().__init__(archivo, escala)
       #Método que establece las variables/variable del personaje
        self.thrust = 0
        self.speed = 0
        self.max_speed = 4
        self.drag = 0.05
        self.respawning = 0
        self.respawn()

    #método para el respawn
    def respawn(self):
        #posición del respawn
        self.respawning = 1
        self.center_x = ancho / 2
        self.center_y = largo / 2
        self.angle = 0

    #método para el movimiento del personaje
    def update(self):
        if self.respawning:
            self.respawning += 1
            self.alpha = self.respawning
            if self.respawning > 250:
                self.respawning = 0
                self.alpha = 255
        if self.speed > 0:
            self.speed -= self.drag
            if self.speed < 0:
                self.speed = 0

        if self.speed < 0:
            self.speed += self.drag
            if self.speed > 0:
                self.speed = 0

        self.speed += self.thrust
        if self.speed > self.max_speed:
            self.speed = self.max_speed
        if self.speed < -self.max_speed:
            self.speed = -self.max_speed

        self.change_x = -math.sin(math.radians(self.angle)) * self.speed
        self.change_y = math.cos(math.radians(self.angle)) * self.speed

        self.center_x += self.change_x
        self.center_y += self.change_y
        if self.right < 0:
            self.left = ancho

        if self.left > ancho:
            self.right = 0

        if self.bottom < 0:
            self.top = largo

        if self.top > largo:
            self.bottom = 0

        super().update()



#definimos los covids
class covidsprite(arcade.Sprite):
    def __init__(self, archivocovid, escala):
        super().__init__(archivocovid, scale=escala)
        self.size = 0

    def update(self):
        super().update()
        if self.center_x < limiteizq:
            self.center_x = limitede
        if self.center_x > limitede:
            self.center_x = limiteizq
        if self.center_y > limitearriba:
            self.center_y = limiteabajo
        if self.center_y < limiteabajo:
            self.center_y = limitearriba

#clase para hacer la ventana
class juego(arcade.Window):

    vida: object

    def __init__(self):

    #super() llama a la clase "constructora padre"   (HERENCIA)
        super().__init__(ancho, largo, titulo)

        #agregamos variables/datos

        self.player_sprite_list = arcade.SpriteList()
        file_path = os.path.dirname(os.path.abspath(__file__))
        file_path1 = os.path.dirname(os.path.abspath("resources"))
        os.chdir(file_path)
        os.chdir(file_path1)
        self.frame_count = 0

        self.fin = False


        # listas de sprites
        self.listajugador = arcade.SpriteList()
        self.listacovid = arcade.SpriteList()
        self.listabalas = arcade.SpriteList()
        self.listavidas = arcade.SpriteList()

        # jugador
        self.puntos = 0
        self.jugador = None
        self.vidas = 3

        # Sonidos
        self.sonidodisparo = arcade.load_sound(":resources:sounds/laser2.wav")
        self.sonidoachunte = arcade.load_sound(":resources:sounds/hurt3.wav")
        self.sonidoachunte2 = arcade.load_sound(":resources:sounds/jump5.wav")
        self.sonidoachunte3 = arcade.load_sound(":resources:sounds/hurt5.wav")
        self.sonidoachunte4 = arcade.load_sound(":resources:sounds/jump4.wav")
        #self.musikita_sound = arcade.load_sound(":resources:music/1918.mp3")

    def start_new_game(self):
        self.frame_count = 0
        self.fin = False

        # listas de sprites
        self.listacovid = arcade.SpriteList()
        self.listabalas = arcade.SpriteList()
        self.list_vida = arcade.SpriteList()

        # Ponemos al personaje
        self.puntos = 0
        self.jugador = elmaster(":resources:images/animated_characters/male_adventurer/maleAdventurer_jump.png", escala)
        self.listajugador.append(self.jugador)
        self.vidas = 3
        cur_pos = 0
        #agregamos vidas
        for i in range(self.vidas):
            vida = arcade.Sprite(":resources:images/animated_characters/male_adventurer/maleAdventurer_jump.png",
                                      escala)
            vida.center_x = cur_pos + vida.width
            vida.center_y = vida.height + 500
            cur_pos += vida.width
            self.listavidas.append(vida)
        image_list = (":resources:images/enemies/slimePurple.png", ":resources:images/enemies/wormPink.png")

        #Elige qué tipo de covid respawnear (hay 2 modelos de covid)
        for i in range(covids):
            image_no = random.randrange(2)
            enemigosprite = covidsprite(image_list[image_no], escala)
            enemigosprite.guid = "covid"

            #lugar de aparición al azar
            enemigosprite.center_y = random.randrange(limiteabajo, limitearriba)
            enemigosprite.center_x = random.randrange(limiteizq, limitede)

            enemigosprite.change_x = random.random() * 2 - 1
            enemigosprite.change_y = random.random() * 2 - 1

            enemigosprite.change_angle = (random.random() - 0.5) * 2
            enemigosprite.size = 4
            self.listacovid.append(enemigosprite)

    def on_draw(self):
        #comenzamos a dibujar(método)
        arcade.start_render()
        #dibuja cada lista
        self.listacovid.draw()
        self.listavidas.draw()
        self.listabalas.draw()
        self.listajugador.draw()
        #puntos
        output = f"puntos: {self.puntos}"
        arcade.draw_text(output, 10, 70, arcade.color.WHITE, 13)
        #Cont. de covids eliminados
        output = f"cuenta covid: {len(self.listacovid)}"
        arcade.draw_text(output, 10, 50, arcade.color.WHITE, 13)

    #definimos al pulsar las teclas
    def on_key_press(self, symbol, modifiers):
        if symbol == arcade.key.M:
            playsound.playsound(self.musikita_sound)

        #agregamos el sprite disparo
        if not self.jugador.respawning and symbol == arcade.key.SPACE:
            balasprite = spritegiro(":resources:images/space_shooter/laserBlue01.png", escala)
            balasprite.guid = "Bullet"

            #velocidad de la bala
            balavel = 13
            balasprite.change_y = \
                math.cos(math.radians(self.jugador.angle)) * balavel
            balasprite.change_x = \
                -math.sin(math.radians(self.jugador.angle)) \
                * balavel

            balasprite.center_x = self.jugador.center_x
            balasprite.center_y = self.jugador.center_y
            balasprite.update()

            self.listabalas.append(balasprite)

            #sonido de disparo
            arcade.play_sound(self.sonidodisparo)

        if symbol == arcade.key.LEFT:
            self.jugador.change_angle = 3
        elif symbol == arcade.key.RIGHT:
            self.jugador.change_angle = -3
        elif symbol == arcade.key.UP:
            self.jugador.thrust = 0.2
        elif symbol == arcade.key.DOWN:
            self.jugador.thrust = -.2

    def on_key_release(self, symbol, modifiers):
        """     Cuando sueltas las teclas, lo agregamos con la retroalimentación de gonzalo y el profesor  """
        if symbol == arcade.key.LEFT:
            self.jugador.change_angle = 0
        elif symbol == arcade.key.RIGHT:
            self.jugador.change_angle = 0
        elif symbol == arcade.key.UP:
            self.jugador.thrust = 0
        elif symbol == arcade.key.DOWN:
            self.jugador.thrust = 0

#update= actualiza atributos
    def on_update(self, x):
        self.frame_count += 1

        if not self.fin:
            self.listacovid.update()
            self.listabalas.update()
            self.listajugador.update()

            for bala in self.listabalas:
                covids = arcade.check_for_collision_with_list(bala, self.listacovid)

                for covid in covids:
                    covid.remove_from_sprite_lists()
                    bala.remove_from_sprite_lists()
                    self.puntos += 1

                tamaño = max(bala.width, bala.height)
                if bala.center_x < 0 - tamaño:
                    bala.remove_from_sprite_lists()
                if bala.center_x > ancho + tamaño:
                    bala.remove_from_sprite_lists()
                if bala.center_y < 0 - tamaño:
                    bala.remove_from_sprite_lists()
                if bala.center_y > largo + tamaño:
                    bala.remove_from_sprite_lists()

            if not self.jugador.respawning:
                covids = arcade.check_for_collision_with_list(self.jugador, self.listacovid)
                if len(covids) > 0:
                    #respawn si te quedan vidas
                    if self.vidas > 0:
                        self.vidas -= 1
                        self.jugador.respawn()
                        self.listavidas.pop().remove_from_sprite_lists()
                        print("contagio")

                    else:

                        self.fin = True
                        print("Fin del juego")





def main():
    #Comenzamos el juego
    window = juego()
    window.start_new_game()
    arcade.run()


if __name__ == "__main__":
    main()
