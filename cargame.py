import pygame
import random
from time import sleep

WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600

BLACK = (0, 0, 0)
WHITE = (240, 240, 240)
GRAY = (150, 150, 150)
RED = (230, 0, 0)

class Car:
    #초기화 후, x, y의 좌표값, 차가 어디로 가는지에 대한 좌표값
    def __init__(self, x = 0, y = 0, dx = 0, dy = 0):
        self.image = ""
        self.x = x
        self.y = y
        self.dx = dx
        self.dy = dy

    def load_image(self):
        # self.image = pygame.image.load('RacingCar01.png')
        self.image = pygame.image.load('RacingCar02.png')
        #size[0] = width, size[1] = height
        self.width = self.image.get_rect().size[0]
        self.height = self.image.get_rect().size[1]

    def draw_image(self):
        #실질적 x, y좌표에 이미지 drop
        screen.blit(self.image, [self.x, self.y])

    def move_x(self):
        #실제 좌표에 움직이는 방향만큼 더해주기
        self.x += self.dx

    def move_y(self):
        # 실제 좌표에 움직이는 방향만큼 더해주기
        self.y += self.dy

    def check_out_of_screen(self):
        #스크린 넘어가지 않게 만든다.
        #윈도우 창의 오른쪽 끝 or 왼쪽 끝
        if self.x + self.width > WINDOW_WIDTH or self.x < 0:
            self.x -= self.dx

    def check_crush(self, car):
        #내 자동차와 타차가 부딫혔는가
        if(self.x + self.width > car.x) and (self.x < car.x+car.width) and\
                (self.y < car.y+car.height) and (self.y+self.height > car.y):
            return True
        else:
            return False

def draw_main_menu():
    draw_x = (WINDOW_WIDTH / 2) - 200
    draw_y = WINDOW_HEIGHT / 2
    image_intro = pygame.image.load('PyCar.png')
    screen.blit(image_intro, [draw_x, draw_y - 280])
    font_40 = pygame.font.SysFont("FixedSys", 40, True, False)
    font_30 = pygame.font.SysFont("FixedSys", 30, True, False)
    text_title = font_40.render('Racing Car Game', True, BLACK)
    screen.blit(text_title, [draw_x, draw_y])
    text_score = font_40.render("Score: "+str(score), True, WHITE)
    screen.blit(text_score, [draw_x, draw_y + 70])
    text_start = font_30.render("Press Spacebar to START", True, RED)
    screen.blit(text_start, [draw_x, draw_y + 140])
    text_start = font_30.render("Press left/right key to play", True, RED)
    screen.blit(text_start, [draw_x, draw_y + 180])
    pygame.display.flip()

def draw_score():
    font_30 = pygame.font.SysFont("FixedSys", 30, True, False)
    text_score = font_30.render("Score: " + str(score), True, BLACK)
    screen.blit(text_score, [15, 15])

if __name__ == '__main__':
    #파이게임 초기화
    pygame.init()
    #전체크기 정의
    screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    #캡션 이름
    pygame.display.set_caption('PLAYDATA')
    #게임에서는 시간이 필요함
    clock = pygame.time.Clock()

    pygame.mixer.music.load('race.wav')
    sound_crush = pygame.mixer.Sound('crash.wav')
    sound_engine = pygame.mixer.Sound('engine.wav')

    #유저는 화면 정 가운데에 위치.
    player = Car(WINDOW_WIDTH / 2, WINDOW_HEIGHT / 2, 0, 0)
    player.load_image()

    cars = []
    car_count = 3
    for i in range(car_count):
        #자동차가 나오는 곳을 랜덤하게 정함.
        x = random.randrange(0, WINDOW_WIDTH - 55)
        y = random.randrange(-150, -50)
        #속도를 5~10 사이로 정의함.
        car = Car(x, y, 0, random.randint(5, 10))
        car.load_image()
        cars.append(car)

    lanes = []
    #차선 그리기,
    lane_width = 10
    lane_height = 80
    lane_margin = 20
    lane_count = 20
    lane_x = (WINDOW_WIDTH - lane_width) / 2
    lane_y = -10
    for i in range(lane_count):
        lanes.append([lane_x, lane_y])
        lane_y += lane_height + lane_margin

    score = 0
    crash = True
    game_on = True
    while game_on:
        #이벤트 처리.
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_on = False

            if crash:
                #충돌하면 게임이 다시 시작될 수 있는 요소를 줄 것임
                if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                    crash = False
                    for i in range(car_count):
                        cars[i].x = random.randrange(0, WINDOW_WIDTH - cars[i].width)
                        cars[i].y = random.randrange(-150, -50)


                    player.load_image()
                    player.x = WINDOW_WIDTH / 2
                    player.dx = 0
                    score = 0
                    pygame.mouse.set_visible(False)
                    sound_engine.play()
                    sleep(1)
                    pygame.mixer.music.play(-1)

            if not crash:
                #키가 눌렸을때
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RIGHT:
                        player.dx = 4
                    elif event.key == pygame.K_LEFT:
                        player.dx = -4

                #키에 안 눌릴때
                if event.type == pygame.KEYUP:
                    if event.key == pygame.K_RIGHT:
                        player.dx = 0
                    elif event.key == pygame.K_LEFT:
                        player.dx = 0

        screen.fill(GRAY)

        if not crash:
            for i in range(lane_count):
                #차선을 계속 그린다.
                pygame.draw.rect(screen, WHITE, [lanes[i][0], lanes[i][1], lane_width, lane_height])
                lanes[i][1] += 10
                if lanes[i][1] > WINDOW_HEIGHT:
                    #전체 게임 화면을 차선이 넘어갔을 때
                    lanes[i][1] = -40 - lane_height

            player.draw_image()
            player.move_x()
            player.check_out_of_screen()

            for i in range(car_count):
                cars[i].draw_image()
                #플레이어는 좌우로, 상대방들은 위에서 아래로 움직인다.
                cars[i].y += cars[i].dy
                if cars[i].y > WINDOW_HEIGHT:
                    score += 10
                    cars[i].x = random.randint(0, WINDOW_WIDTH - cars[i].width)
                    cars[i].y = random.randint(-150, -50)
                    cars[i].dy = random.randint(5, 10)
                    cars[i].load_image()

            for i in range(car_count):
                #플레이어가 타차랑 부딫히면 일어나게 되는 것들.
                if player.check_crush(cars[i]):
                    crash = True
                    #노래 멈추기, 잠깐 멈추고, 마우스 보이게 된다.
                    pygame.mixer.music.stop()
                    sound_crush.play()
                    sleep(1)
                    pygame.mouse.set_visible(True)
                    break
            #점수 표출
            draw_score()
            pygame.display.flip()

        else:
            draw_main_menu()

        clock.tick(60)
    pygame.quit()

