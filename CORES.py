# 一些乱七八糟的函数与库


from itertools import combinations
from itertools import permutations
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


def assign(i, S, I, O):
    '''
    输入 assignment S 和个体，返回在该分配下，他所分配的物品
    如果一个人分配到了多个物品，返回效用最高的那个
    返回零代表该分配下他什么都没得到
    '''
    if not i in I:
        print('player is out of range')
        return None
    A = []
    for a in O:
        if S[i-1][a-1]:
            A.append(a)
    if not len(A):
        return 0
    elif len(A)==1:
        return A[0]
    else:
        t = A[0]
        for a in A:
            if P_c(i, a, t):
                t = a
        return t


def R_c(i, a, b, P):
    '''
    判断对i来说，是否偏好a
    '''
    if a>0:
        ua = P[i-1][a-1]
    else:
        ua = 0
    if b>0:
        ub = P[i-1][b-1]
    else:
        ub = 0
        
    if ua>=ub:
        return True
    else:
        return False


def P_c(i, a, b, P):
    '''
    判断对i来说，是否严格偏好a
    '''
    if a>0:
        ua = P[i-1][a-1]
    else:
        ua = 0
    if b>0:
        ub = P[i-1][b-1]
    else:
        ub = 0
        
    if ua>ub:
        return True
    else:
        return False

    
def private_own(coalition, Omega, I, O):
    '''
    输入所有权结构/分配
    返回物品集（在该所有权结构/分配下被该集团完全所有的物品）
    '''
    A = []
    for a in O:
        k = 1
        for i in I:
            if Omega[i-1][a-1] and not (i in coalition):
                k = 0
                break
        if k:
            A.append(a)
    return A


def transpose(A):
    '''
    transpose a matrix
    '''
    n = len(A)
    m = len(A[0])
    ans = empty(m, n)
    for i in range(m):
        for j in range(n):
            ans[i][j] = A[j][i]
    return ans


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



def inverse(mu, object_set, I):
    '''
    返回物品集涉及的所有人（集合）
    '''
    peop = []
    for a in object_set:
        for i in I:
            if mu[i-1][a-1]:
                peop.append(i)
    return peop


def ext_private_own(coalition, mu, C, I, O):
    
    coal = []
    coal.append(set(coalition))
    coal_j = coal[0]
    coal_k = coal[0]|set(inverse(mu, private_own(coal[0], C,I,O),I))

    while coal_j!=coal_k:
        coal.append(coal_k)
        coal_j = coal_k
        coal_k = coal[-1]|set(inverse(mu, private_own(coal[-1], C,I,O),I))
    
    return list(coal[-1])


def check_example(mu, C, P):
    
    print('\nCheck:')
    
    if if_in_strong_core(mu, C, P):
        print('s', end=' ')
    if if_in_weak_core(mu, C, P):
        print('w', end=' ')
    if if_in_effective_core(mu, C, P):
        print('e', end=' ')
    if if_in_direct_exclusion_core(mu, C, P):
        print('dex', end=' ')
    if if_in_exclusion_core(mu, C, P):
        print('idex', end=' ')
    
    return None


def weakly_block(coalition, M, S, C, P, I, O):
    '''
    check is assignment Mu is weakly blocked by coalition via Sigma
    '''
    k1 = 1
    k2 = 0
    for i in coalition:
        if not R_c(i, assign(i, S, I, O), assign(i, M, I, O), P):
            k1 = 0
    for i in coalition:
        if P_c(i, assign(i, S, I, O), assign(i, M, I, O), P):
            k2 = 1
    k3 = 0
    if set(private_own(coalition, S, I, O))<=set(private_own(coalition, C, I, O)):
        k3 = 1
    
    if k1 and k2 and k3:
        return True
    else:
        return False
    
    
def if_in_strong_core(mu, C, P, detail = False):
    
    
    n_player = len(C)
    I = []
    for i in range(n_player):
        I.append(i+1)
    n_object = len(C[0])
    O = []
    for a in range(n_object):
        O.append(a+1)
    
    
    # check if the strong core is empty
    # 对coalition进行组合
    COALITION = []

    for popu in range(1, n_player):
        for coalition in combinations(I, popu+1):
            COALITION.append(list(coalition))
            
    ans = True
    
    T_list = []
    I_plus = [0]+I
    for i in I_plus:
        T = []
        for j in I:
            if j==i:
                T.append(1)
            else:
                T.append(0)
        T_list.append(T)
    for TT in permutations(T_list, len(O)):
        T = transpose(list(TT))
        for coalition in COALITION:
            if weakly_block(coalition, mu, T, C, P, I, O):
                if detail:
                    print('Coalition: '+str(coalition)+'\n')
                    output(T)
                ans = False
    return ans


def strongly_block(coalition, M, S, C, P, I, O):
    '''
    check is assignment Mu is strongly blocked by coalition via Sigma
    '''
    k1 = 1
    for i in coalition:
        if not P_c(i, assign(i, S, I, O), assign(i, M, I, O), P):
            k1 = 0
    k3 = 0
    if set(private_own(coalition, S, I, O))<=set(private_own(coalition, C, I, O)):
        k3 = 1
    
    if k1 and k3:
        return True
    else:
        return False  
    
    
def if_in_weak_core(mu, C, P, detail = False):
    
    
    n_player = len(C)
    I = []
    for i in range(n_player):
        I.append(i+1)
    n_object = len(C[0])
    O = []
    for a in range(n_object):
        O.append(a+1)
    
    # check if the strong core is empty
    # 对coalition进行组合
    COALITION = []

    for popu in range(1, n_player):
        for coalition in combinations(I, popu+1):
            COALITION.append(list(coalition))
            
    ans = True
    
    T_list = []
    I_plus = [0]+I
    for i in I_plus:
        T = []
        for j in I:
            if j==i:
                T.append(1)
            else:
                T.append(0)
        T_list.append(T)
    for TT in permutations(T_list, len(O)):
        T = transpose(list(TT))
        for coalition in COALITION:
            if strongly_block(coalition, mu, T, C, P, I, O):
                if detail:
                    print('Coalition: '+str(coalition)+'\n')
                    output(T)
                ans = False
    return ans


def effectively_block(coalition, mu, sigma, C, P, I, O):
    '''
    coalition effectively blocks mu via sigma
    '''
    
    # 集团中所有人都不变差
    k1 = 1
    for i in coalition:
        if not R_c(i, assign(i, sigma, I, O), assign(i, mu, I, O), P):
            k1 = 0
    
    # 集团中有人严格变好
    k2 = 0
    for i in coalition:
        if P_c(i, assign(i, sigma, I, O), assign(i, mu, I, O), P):
            k2 = 1
    
    # 进行的是集团内部分配
    k3 = 0
    if set(private_own(coalition, sigma, I, O))<=set(private_own(coalition, C, I, O)):
        k3 = 1
        
    # 新要求
    k4 = 1
    # 这里要加入新的判定条件
    for popu in range(len(coalition)):
        for coal in combinations(coalition, popu+1):
            coal = list(coal)
            if set(private_own(coal, sigma, I, O))<=set(private_own(coal, C, I, O)):
                obj = set(private_own(coal, C, I, O))-set(private_own(coal, sigma, I, O))
                if len(obj):
                    for a in obj:
                        if a in private_own(coalition, sigma, I, O):
                            k4 = 0
    if coalition == I:
        k4 = 1
    
    if k1 and k2 and k3 and k4:
        return True
    else:
        return False
    
    
def if_in_effective_core(mu, C, P, detail = False):
    
    
    n_player = len(C)
    I = []
    for i in range(n_player):
        I.append(i+1)
    n_object = len(C[0])
    O = []
    for a in range(n_object):
        O.append(a+1)
    
    # check if the strong core is empty
    # 对coalition进行组合
    COALITION = []

    for popu in range(1, n_player):
        for coalition in combinations(I, popu+1):
            COALITION.append(list(coalition))
            
    ans = True
    
    T_list = []
    I_plus = [0]+I
    for i in I_plus:
        T = []
        for j in I:
            if j==i:
                T.append(1)
            else:
                T.append(0)
        T_list.append(T)
    for TT in permutations(T_list, len(O)):
        T = transpose(list(TT))
        for coalition in COALITION:
            if effectively_block(coalition, mu, T, C, P, I, O):
                if detail:
                    print('Coalition: '+str(coalition)+'\n')
                    output(T)
                ans = False
    return ans


def directly_exclusion_block(coalition, M, S,C,P,I,O):
    
    k1 = 1
    for i in coalition:
        if not P_c(i, assign(i, S,I,O), assign(i, M,I,O),P):
            k1 = 0
    k2 = 1
    for j in I:
        if P_c(i, assign(i, M,I,O), assign(i, S,I,O),P) and not (assign(i, M,I,O) in private_own(coalition, C,I,O)):
            k2 = 0
            
    if k1 and k2:
        return True
    else:      
        return False
    
def if_in_direct_exclusion_core(mu,C,P, detail = False):
    
    n_player = len(C)
    I = []
    for i in range(n_player):
        I.append(i+1)
    n_object = len(C[0])
    O = []
    for a in range(n_object):
        O.append(a+1)
    
    
    # check if the strong core is empty
    # 对coalition进行组合
    COALITION = []

    for popu in range(1, n_player):
        for coalition in combinations(I, popu+1):
            COALITION.append(list(coalition))
            
    ans = True
    
    T_list = []
    I_plus = [0]+I
    for i in I_plus:
        T = []
        for j in I:
            if j==i:
                T.append(1)
            else:
                T.append(0)
        T_list.append(T)
    for TT in permutations(T_list, len(O)):
        T = transpose(list(TT))
        for coalition in COALITION:
            if directly_exclusion_block(coalition, mu, T,C,P,I,O):
                if detail:
                    print('Coalition: '+str(coalition)+'\n')
                    output(T)
                ans = False
    return ans




def indirectly_exclusion_block(coalition, M, S,C,P,I,O):
    
    k1 = 1
    for i in coalition:
        if not P_c(i, assign(i, S,I,O), assign(i, M,I,O),P):
            k1 = 0
    k2 = 1
    for j in I:
        if P_c(i, assign(i, M,I,O), assign(i, S,I,O),P) and not (assign(i, M,I,O) in ext_private_own(coalition, M, C,I,O)):
            k2 = 0
            
    if k1 and k2:
        return True
    else:      
        return False
    
    
def if_in_exclusion_core(mu,C,P, detail = False):
    
    
    n_player = len(C)
    I = []
    for i in range(n_player):
        I.append(i+1)
    n_object = len(C[0])
    O = []
    for a in range(n_object):
        O.append(a+1)
    
    # check if the strong core is empty
    # 对coalition进行组合
    COALITION = []

    for popu in range(1, n_player):
        for coalition in combinations(I, popu+1):
            COALITION.append(list(coalition))
            
    ans = True
    
    T_list = []
    I_plus = [0]+I
    for i in I_plus:
        T = []
        for j in I:
            if j==i:
                T.append(1)
            else:
                T.append(0)
        T_list.append(T)
    for TT in permutations(T_list, len(O)):
        T = transpose(list(TT))
        for coalition in COALITION:
            if indirectly_exclusion_block(coalition, mu, T,C,P,I,O):
                if detail:
                    print('Coalition: '+str(coalition)+'\n')
                    output(T)
                ans = False
    return ans