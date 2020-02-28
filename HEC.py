import csv

def output(A):
    '''
    输出矩阵
    '''
    for i in range(len(A)):
        for j in range(len(A[i])):
            print(A[i][j], end = '    ')
        print('\n')
    for i in range((len(A[0])-1)*5+1):
        print('-', end = '')
    print('\n')
    return None

def inpt(file):
    '''
    file is the name of the inputed csv file
    '''
    C = []
    # 从文件中读取数据
    with open(file) as c_file:
        c_reader = csv.reader(c_file, delimiter = ' ')
        for row in c_reader:
            C.append(row)

    for i in range(len(C)):
        for j in range(len(C[i])):
            C[i][j] = int(C[i][j])
    
    return C

CC = inpt('0_C.txt')
PP = inpt('0_P.txt')
#print('所有矩阵：\n')
#output(CC)
#print('偏好矩阵：\n')
#output(PP)

II, OO = [], []
for i in range(len(CC)):
    II.append(i+1)
for a in range(len(CC[0])):
    OO.append(a+1)
    
    
def empty(n, m):
    '''
    创建 n*m 的零矩阵
    '''
    A = []
    for i in range (n):
        A.append([])
        for j in range(m):
            A[i].append(0)
    return A


def multiply(A, B):
    '''
    计算矩阵乘法
    两个矩阵默认满足乘法的条件；该函数不处理错误
    '''
    n = len(A)
    k = len(B)
    m = len(B[0])
    ans = empty(n, m)
    
    for i in range(n):
        for j in range(m):
            for t in range(k):
                ans[i][j] += A[i][t]*B[t][j]     
    return ans


def favo(i, O):
    '''
    输入人，在物品集中找到他最喜欢的物品；如果在物品集中没有这个人想要的物品，那么返回0
    '''
    u = 0
    ans = 0
    for a in O:
        if PP[i-1][a-1]>u:
            ans = a
            u = PP[i-1][a-1]
    return ans


def belong(a, I, C):
    '''
    输入物品，在参与者集合和当前所有权结构中找到该物品的所有者；如果所有者不存在则返回0
    '''
    ans = 0
    for i in I:
        if C[i-1][a-1]:
            ans = i
    return ans


def graph(I, O, C):
    '''
    根据TTC把当前的指向化成图
    '''
    n = len(C)
    G = empty(n, n)
    for i in I:
        if max(PP[i-1]) and favo(i, O):
            G[i-1][belong(favo(i, O), I, C)-1] = 1
    return G
    

def TTC(I, O, C):
    '''
    当前图下是否存在圈；如果不存在返回空列表；如果存在返回圈中人；列表长度可以作为check的布尔变量
    '''
    G = graph(I, O, C)
    circle = [[],[]]
    A = G
    for degree in range(len(G)):
        for j in range(len(G)):
            if (A[j][j]==1) and not (j+1 in circle[0]):
                circle[0].append(j+1)
                circle[1].append(favo(j+1, O))
        A = multiply(A, G)
    return circle


def allocate(I, O, C):
    # 得到随机分配后的所有矩阵
    A = empty(len(C), len(C[0]))
    for a in O:
        k = 1
        for i in I:
            if (C[i-1][a-1]):
                if k:
                    k = 0
                    A[i-1][a-1] = 1
                else:
                    A[i-1][a-1] = 0
    return A

def cre_like(A):
    m = len(A)
    n = len(A[0])
    B = empty(m, n)
    for i in range(m):
        for j in range(n):
            B[i][j] = A[i][j]
    return B


t = 0
I, O, C = [[]], [[]], [[]]
I[0], O[0], C[0] = II, OO, CC
all_out = []

#print(I[0])
#print(O[0])
print('第0期\n')
output(C[0])


#for t in range(1, 4):

while len(all_out)<len(C[0]):
    
    t += 1
    
    # 得到本轮TTC圈中人和物
    out = TTC(I[t-1], O[t-1], allocate(I[t-1], O[t-1], C[t-1]))
    all_out += out[0]
    print('第%s期出圈人\n'%t)
    output(out)

    I.append([])
    O.append([])
    for i in I[t-1]:
        if not (i in out[0]):
            I[t].append(i)
    for a in O[t-1]:
        if not (a in out[1]):
            O[t].append(a)


    # 新的所有权结构
    C.append(cre_like(C[t-1]))
    player_pool = []
    for i in I[t-1]:
        if i in out[0]:
            # the object pointed by the agent exclusively assigned to the player
            a = out[1][out[0].index(i)]
            for aa in O[0]:
                if aa == a:
                    C[t][i-1][aa-1] = 1
                else:
                    C[t][i-1][aa-1] = 0
            for ii in I[0]:
                if ii != i:
                    C[t][ii-1][a-1] = 0

        else:
            # decide if the player need compensation
            k = 0
            for a in O[t-1]:
                if C[t-1][i-1][a-1] and (a in out[1]):
                    k = 1
            if k:
                player_pool.append(i)

    for a in O[t]:
        k = 0
        for i in I[t-1]:
            if C[t-1][i-1][a-1] and (i in out[0]):
                k = 1
        if k:
            if len(player_pool):
                C[t][player_pool[0]-1][a-1] = 1
            else:
                for i in I[t]:
                    C[t][i-1][a] = 1
    print('第%s期所有权结构\n'%t)
    output(C[t])