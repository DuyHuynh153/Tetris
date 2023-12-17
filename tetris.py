
import pygame
import random

 
# creating the data structure for pieces
# setting up global vars
# functions
# - create_grid
# - draw_grid
# - draw_window
# - rotating shape in main
# - setting up the main
 
"""
10 x 20 square grid
shapes: S, Z, I, O, J, L, T
represented in order by 0 - 6
"""
 
pygame.font.init() # khởi tạo module phông chữ

# GLOBALS VARS
s_width = 800
s_height = 700
play_width = 300  # meaning 300 // 10 = 30 width per block
play_height = 600  # meaning 600 // 20 = 20 height per block
block_size = 30
 
top_left_x = (s_width - play_width) // 2
top_left_y = s_height - play_height
 
 
# SHAPE FORMATS
 
S = [['.....',
      '.....',
      '..00.',
      '.00..',
      '.....'],

     ['.....',
      '..0..',
      '..00.',
      '...0.',
      '.....']]
 
Z = [['.....',
      '.....',
      '.00..',
      '..00.',
      '.....'],
     ['.....',
      '..0..',
      '.00..',
      '.0...',
      '.....']]
 
I = [['..0..',
      '..0..',
      '..0..',
      '..0..',
      '.....'],
     ['.....',
      '0000.',
      '.....',
      '.....',
      '.....']]
 
O = [['.....',
      '.....',
      '.00..',
      '.00..',
      '.....']]
 
J = [['.....',
      '.0...',
      '.000.',
      '.....',
      '.....'],
     ['.....',
      '..00.',
      '..0..',
      '..0..',
      '.....'],
     ['.....',
      '.....',
      '.000.',
      '...0.',
      '.....'],
     ['.....',
      '..0..',
      '..0..',
      '.00..',
      '.....']]
 
L = [['.....',
      '...0.',
      '.000.',
      '.....',
      '.....'],
     ['.....',
      '..0..',
      '..0..',
      '..00.',
      '.....'],
     ['.....',
      '.....',
      '.000.',
      '.0...',
      '.....'],
     ['.....',
      '.00..',
      '..0..',
      '..0..',
      '.....']]
 
T = [['.....',
      '..0..',
      '.000.',
      '.....',
      '.....'],
     ['.....',
      '..0..',
      '..00.',
      '..0..',
      '.....'],
     ['.....',
      '.....',
      '.000.',
      '..0..',
      '.....'],
     ['.....',
      '..0..',
      '.00..',
      '..0..',
      '.....']]
 
shapes = [S, Z, I, O, J, L, T]
shape_colors = [(0, 255, 0), (255, 0, 0), 
                (0, 255, 255), (255, 255, 0), 
                (255, 165, 0), (0, 0, 255), 
                (128, 0, 128)]
# index 0 - 6 represent shape
 
 
class Piece(object):
    def __init__(self,x,y,shape):
        self.x = x
        self.y = y
        self.shape = shape
        self.color = shape_colors[shapes.index(shape)] # chọn màu trong list shape_color với index = shape nhập vào
        self.rotation = 0

 #kiểm tra trong lưới có vị trí khoá thì đổi màu trong lưới grid
def create_grid(locked_positions):
    grid = [[(0,0,0) for _ in range(10)] for _ in range(20) ] # tạo lưới gồm 20 hàng, mỗi hàng có 10 cột(lưới rỗng)
    for i in range(len(grid)): # len of grid is 20 
        for j in range(len(grid[i])): #len = 10
            if (j,i) in locked_positions: # j ,i đại diện cho x,y | vd: ((0,0):(255,255,255))
                c = locked_positions[(j,i)]
                grid [i][j] = c
    return grid


def convert_shape_format(shape):
    positions = []
    #trả về 1 sublist trong của 1 shape có dược
    format = shape.shape[shape.rotation % len(shape.shape)  ]
    
# chuyển sang vị trí các block vẽ
    for i,line in enumerate(format):
        row = list(line) # row: '..0..'
        for j,column in enumerate(row):
            if column =='0':
                positions.append((shape.x + j , shape.y + i))
    # sửa lại vị trí các block 
    for i, pos in enumerate(positions):
        
        positions[i] = (pos[0]-2,pos[1]-4) 
    return positions
 
def valid_space(shape, grid):
    #tạo ra 1 list chứa các vị trí được chấp nhận(chỉ những chỗ trống)
    accepted_pos = [[(j,i) for j in range(10) if grid[i][j] ==(0,0,0)]  for i in range(20)]
    accepted_pos = [j for sub in accepted_pos for j in sub]
    # kind of like : [[(0,1)],[2,3]] -> [(0,1),(2,3)]
    # hơi giống mảng 1 chiều

    formatted = convert_shape_format(shape) #trả về list các vị trí của block
    for pos in formatted:
        if pos not in accepted_pos:
            # để cho block không hiển thị trên lưới mà phải roi từ trên xuông
            if pos[1] > -1: 
                return  False
    return True



def check_lost(positions): # kiểm tra thua trò chơi
    for pos in positions:
        x,y = pos
        if y < 1: #nếu giá trị y = 0 thì chạm trên cùng -> lost
            return True
    return False

def get_shape():
    return Piece(5 , 0 ,random.choice(shapes)) # trả về 1 trong những phần tử của list shapes[S,z,i,...]
                                               # với x=5,y=0 là y không thay đổi, x= 5 là ở giữa khung trog chơi, vì khung chứa 10 block
 
 
def draw_text_middle(surface, text, size, color):
    font = pygame.font.SysFont('comicsans',size,bold=True)
    label = font.render(text,1,color)
    # vẽ ở giữa màn hinh
    surface.blit(label,(top_left_x + play_width/2 
                        - (label.get_width()/2)
                        ,top_left_y + play_height/2 
                        -(label.get_height()/2) ))
   
def draw_grid(surface,grid): # hàm vẽ lưới 
    # gán biến đỡ dài
    sx = top_left_x
    sy = top_left_y
    for i in range(len(grid)):
        pygame.draw.line(surface,(128,128,128),(sx , sy+i*block_size)
                         ,(sx+play_width , sy+i*block_size))
        for j in range (len(grid[i])):
            pygame.draw.line(surface,(128,128,128),(sx+j*block_size , sy)
                             ,(sx + j*block_size , sy + play_height))

def clear_rows(grid, locked):
    inc =0 #increment: biến đếm giá trị hàng được xoá để tính điểm
    
    for i in range(len(grid)-1,-1,-1): # chạy ngược lại từ 19 -> 0 , bước nhảy -1
        row = grid[i]
        #nếu hàng đó không chưa ô rỗng -> đầy hàng
        if (0,0,0) not in row : 
            inc += 1
            ind = i
            #chạy từng ô trong hàng đó để xoá hết 1 hàng
            for j in range(len(row)):
                try:
                    del locked[(j,i)]
                except:
                    continue
        '''
        [(0,1),(0,0)] -> [(0,0),(0,1)]
        '''
                    
    if inc > 0:
        for key in sorted(list(locked), key = lambda x: x[1] )[::-1]: #sắp xếp các giá trị y tăng dần vì bị xoá
            x,y = key
            if y < ind:
                newKey = (x,y+inc)
                locked[newKey] = locked.pop(key)        # ghi đè lại vị trí để có được màu của key cũ
    return inc # để tính điểm
 
def draw_next_shape(shape, surface):
    font = pygame.font.SysFont('comicsans',30)
    label = font.render('Next Shape',1,(255,255,255))

    # khởi tạo vị trí x,y vẽ "Next Shape"
    sx = top_left_x + play_width + 50
    sy = top_left_y + play_height/2 -100
    format = shape.shape[shape.rotation % len(shape.shape)]
    
    for i, line in enumerate(format):
        row = list(line)
        for j,column in enumerate(row):
            if column =='0':
                #vẽ các ô để tạo thành lưới với mỗi ô có size = 30
                pygame.draw.rect(surface,shape.color,(sx + j*block_size, 
                                                      sy +i*block_size,
                                                      block_size,
                                                      block_size),0) 
    #vẽ label
    surface.blit(label,(sx,sy-50))
    
def draw_window(surface,grid,score = 0):
    surface.fill((0,0,0)) # draw background with black
    
    pygame.font.init()
    # thiết lập font chữ , cỡ chữ
    font = pygame.font.SysFont('comicsans',42) 
    # setup tittle , số 1 là chế độ khử răng cưa
    label = font.render('TETRIS',1,(255,255,255)) 
    
    # công thức tìm vị trí chính giữa màn hình để ghi chữ tettris
    surface.blit(label,(top_left_x + play_width/2 - (label.get_width())/2 ,30 ) ) 
 
    font = pygame.font.SysFont('comicsans',30)
    label = font.render('Score: '+ str(score),1,(255,255,255))

    sx = top_left_x + play_width + 50
    sy = top_left_y + play_height/2 -100
    surface.blit(label,(sx+20,sy+160))
  
    
    
    for i in range(len(grid)):
        for j in range(len(grid[i])):
            # vẽ các hình với màu lấp đầy các hình
            pygame.draw.rect(surface,grid[i][j],(top_left_x + j*block_size, top_left_y + i*block_size,block_size,block_size),0)#số 0 là kích thước đường viền

    pygame.draw.rect(surface,(255,0,0),(top_left_x,top_left_y,play_width,play_height),4) # vẽ khung viền vuông với màu đỏ, số 4 là độ lớn của đường viền

    draw_grid(surface,grid) # gọi hàm vẽ lưới màn hình(không có hàm vẫn chạy nhưng không thấy lưới )
    

def main(win):
    locked_positions = {}
    grid = create_grid(locked_positions)

    change_piece = False
    run = True
    # mảnh hiện tại 
    current_piece = get_shape()
    clock = pygame.time.Clock()
    
    fall_time = 0
    level_time =0
    fall_speed = 0.35 # thời gian 1 khối dừng trước khi rơi xuống
    
    next_piece = get_shape()

    score = 0


    # chạy vòng lâp hiển thị màn hình
    while run:
        grid = create_grid(locked_positions)
        fall_time += clock.get_rawtime()
        level_time += clock.get_rawtime()
        clock.tick()
        
        if level_time/1000 > 5:
            level_time = 0
            if level_time > 0.12:
                level_time -= 0.005

       

        if fall_time/1000 > fall_speed:
         #   print ("fall_time is: " + str(fall_time))
            fall_time = 0
            current_piece.y += 1
            # nếu như ko ở trên cùng màn hình
            if not (valid_space(current_piece,grid)): 
                current_piece.y -= 1
                change_piece = True # khi block dịch xuống mà ko dịch trái hay phải mà no chạm 1 cái gì đó như
                                    # là đáy hoặc 1 block khác 

        for event in pygame.event.get():
            if event.type == pygame.QUIT: # nếu tick vào quit thì thoát trò chơi
                run = False
                
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    current_piece.x -=1
                    if not (valid_space(current_piece,grid)): 
                        current_piece.x +=1         # nếu chạm bên trái màn hình chơi thì ko bị out game
                if event.key == pygame.K_RIGHT: #ấn mũi tên phải thì dịch block sang phải 1 đơn vị
                    current_piece.x +=1
                    if not (valid_space(current_piece,grid)):
                        current_piece.x -=1         # tương tự if ở trên nhưng là bên phải
                if event.key == pygame.K_DOWN:
                    current_piece.y +=1
                    if not (valid_space(current_piece,grid)):
                        current_piece.y -=1
                if event.key == pygame.K_UP: # mũi tên lên trên thì chuyển đổi hình dạng, chuyển đổi sublist
                    current_piece.rotation +=1   # thay đổi sang sublist tiếp theo của từng shape
                    if not (valid_space(current_piece,grid)):
                        current_piece.rotation -=1

        shape_pos = convert_shape_format(current_piece) 
        for i in range(len(shape_pos)):          
            x,y = shape_pos[i]
            #bắt đầu ở vị trí 0
         # nếu ở dưới màn hình ( bên trong màn hình) thì tô màu block
            if y > -1:
                grid [y][x] = current_piece.color

        if change_piece:
            for pos in  shape_pos:
                p = (pos[0],pos[1])
                locked_positions[p] = current_piece.color

            current_piece = next_piece
            next_piece = get_shape()
            change_piece = False
            score += clear_rows(grid , locked_positions) * 10

        draw_window(win, grid, score)     
        draw_next_shape(next_piece,win)
        pygame.display.update()
        
# nếu check_lost = true thì chạy xong nó thoát luôn ! Tức là check_lost đang = true
        if check_lost(locked_positions):
            draw_text_middle(win,"YOU LOST !",80,(255,255,255))
            pygame.display.update()
            pygame.time.delay(2000)
            run = False
          
    


def main_menu(win):
    run = True
    while run:
        win.fill((0,0,0))
        draw_text_middle(win, "Press Any Key To Play",40,(255,255,255))
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.KEYDOWN:
                main(win)
    #kết thuc vòng lặp thì thoát game  
    pygame.display.quit()

win = pygame.display.set_mode((s_width, s_height))
pygame.display.set_caption('Xếp Gạch')


main_menu(win)  # start game


