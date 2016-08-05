import random
import pprint
from copy import deepcopy
from PIL import Image,ImageDraw,ImageFont

_word="helloworld"
_width=_height=30

def grid_to_img(grid,fname):
    image = Image.new("RGBA", (len(grid)*100,len(grid)*100), (255,255,255))
    draw = ImageDraw.Draw(image)
    font = ImageFont.truetype("fonts/Helvetica.ttf", 100)
    for i in range(len(grid)):
        for j in range(len(grid[i])):
            draw.text((i*100+15, j*100-7), grid[j][i], (0,0,0), font=font)
    img_resized = image.resize((1000,1000), Image.ANTIALIAS)
    img_resized.save("images/"+fname+".png","png")

def initial_grid(word, width,height):
    grid=[]
    for _ in range(width):
        row = []
        for _ in range(height):
            row.append(random.choice(word))
        grid.append(row)
    return grid

def shuffle_word(word):
    shuff = ""
    lw = list(word)
    for _ in lw:
        shuff += random.choice(lw)
    return shuff

def shuffle_word_in_row(grid,rownum,word):
    new_row = ("".join(grid[rownum])).replace(word, shuffle_word(word))
    grid[rownum]=list(new_row)

def shuffle_word_in_col(grid,colnum,word):
    column=""
    for i in range(len(grid)):
        column+=grid[i][colnum]
    column = column.replace(word, shuffle_word(word))
    for i in range(len(grid)):
        grid[i][colnum]=column[i]

def insert_word_in_row(grid,rownum,word):
    print len(grid),rownum
    new_row = grid[rownum]
    begin = random.randint(0,len(grid[0])-len(word))
    new_row[begin:begin + len(word)]=list(word)
    grid[rownum]=new_row

def insert_word_in_col(grid,colnum,word):
    begin = random.randint(0,len(grid)-len(word))
    c = 0
    for i in range(begin,begin + len(word)):
        grid[i][colnum] = word[c]
        c+=1

def remove_all_words(grid,word):
    if len(set(word)) < 2:
        return grid
    current_is_row = True
    while True:
        wc = word_count(grid, word)
        if wc[0]==0:
            break
        if current_is_row and len(wc[1])!=0:
            temp_grid = deepcopy(grid)
            shuffle_word_in_row(temp_grid, random.choice(wc[1]), word)
            if word_count(temp_grid, word)[0] <= wc[0]:
                grid = temp_grid
        elif len(wc[2])!=0:
            temp_grid = deepcopy(grid)
            shuffle_word_in_col(temp_grid, random.choice(wc[2]), word)
            if word_count(temp_grid, word)[0] <= wc[0]:
                grid = temp_grid
        current_is_row = not current_is_row
    return grid

def insert_one_word(grid,word):
    random.choice([insert_word_in_col,insert_word_in_row])(grid, random.randint\
        (0,len(grid)), word)

def word_count(grid,word):
    count = 0
    found_rows = []
    found_cols = []
    # rows check
    for i in range(len(grid)):
        if "".join(grid[i]).find(word)!=-1:
            count+=("".join(grid[i]).count(word))
            found_rows.append(i)
    # cols 
    for i in range(len(grid[0])):
        column=""
        for j in range(len(grid)):
            column+=grid[j][i]
        if "".join(column).find(word)!=-1:
            count+="".join(column).count(word)
            found_cols.append(i)
    return (count,found_rows,found_cols)

def print_grid(grid):
    for i in xrange(len(grid)):
        for j in xrange(len(grid[i])):
            print grid[i][j],
        print ""

def random_word():
    f=open("wordlist/words.txt","r").readlines()
    return random.choice(f).strip()

def get_puzzl():
    _word = random_word().upper()
    _width=_height= random.randint(len(_word)+2,27)
    grid = initial_grid(_word,_width,_height)
    grid = remove_all_words(grid, _word)
    insert_one_word(grid, _word)
    grid_to_img(grid,"grid")
    return {
        'puzzl':'word_grid',
        'tweet_text':'find #%s'%_word.lower(),
        'tweet_image':'images/grid.png'
    }

# if __name__ == '__main__':
#     _word = random_word().upper()
#     _width=_height= random.randint(20,30)
#     print _word,_width
#     grid = initial_grid(_word,_width,_height)
#     s = word_count(grid, _word)
#     grid = remove_all_words(grid, _word)
#     insert_one_word(grid, _word)
#     print_grid(grid)
#     grid_to_img(grid,"grid")