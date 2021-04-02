import math
import numpy as np

# s1 =[(1,1),(2,1),(12,2),(2,3)]
# s2 =[(1,2),(2,3),(2,9),(8,36)]
# # a = get_similarity(s1,s2)

# print(s1[2][1])

# def calculate_euclid(point_a, point_b):
#     """
#     Args:
#         point_a: a data point of curve_a
#         point_b: a data point of curve_b
#     Return:
#         The Euclid distance between point_a and point_b
#     """

#     # return math.sqrt((point_a - point_b)**2)
#     return math.sqrt(int(point_a)**2 + int(point_b)**2 - 2*int(point_a)*int(point_b))

# def calculate_frechet_distance(dp,i,j ,curve_a, curve_b):
#     """
#     Args:
#         dp: The distance matrix
#         i: The index of curve_a
#         j: The index of curve_b
#         curve_a: The data sequence of curve_a
#         curve_b: The data sequence of curve_b
#     Return:
#         The frechet distance between curve_a[i] and curve_b[j]
#     """
#     if dp[i][j] > -1:
#         return dp[i][j]
#     elif i == 0 and j ==0:
#         dp[i][j] = calculate_euclid(curve_a[0], curve_b[0])
#     elif i > 0 and j == 0:
#         dp[i][j] = max(calculate_frechet_distance(dp, i-1, 0, curve_a, curve_b), calculate_euclid(curve_a[i], curve_b[0]))
#     elif i == 0 and j > 0:
#         dp[i][j] = max(calculate_frechet_distance(dp, 0, j-1, curve_a,curve_b), calculate_euclid(curve_a[0],curve_b[j]))
#     elif i > 0 and j > 0:
#         dp[i][j] = max(min(calculate_frechet_distance(dp, i-1, j, curve_a, curve_b), calculate_frechet_distance(dp, i-1, j-1, curve_a, curve_b), calculate_frechet_distance(dp, i, j-1, curve_a, curve_b)), calculate_euclid(curve_a[i], curve_b[j]))
#     else:
#         dp[i][j] = float("inf")
#     return dp[i][j]

# def get_similarity(curve_a,curve_b):
#     dp = [[-1 for _ in range(len(curve_b))] for _ in range(len(curve_a))]
#     similarity =  calculate_frechet_distance(dp,len(curve_a)-1,len(curve_b)-1, curve_a, curve_b)
#     return max(np.array(dp).reshape(-1,1))[0]

# a = get_similarity(s1,s2)


def euc_dist(pt1, pt2):
    return math.sqrt((pt2[0]-pt1[0])*(pt2[0]-pt1[0])+(pt2[1]-pt1[1])*(pt2[1]-pt1[1]))
 
# 这个就是计算Frechet Distance距离的具体过程,是用递归方式计算
def _c(ca,i,j,P,Q):
    if ca[i,j] > -1:
        return ca[i,j]
    elif i == 0 and j == 0:
        ca[i,j] = euc_dist(P[0],Q[0])
    elif i > 0 and j == 0:
        ca[i,j] = max(_c(ca,i-1,0,P,Q),euc_dist(P[i],Q[0]))
    elif i == 0 and j > 0:
        ca[i,j] = max(_c(ca,0,j-1,P,Q),euc_dist(P[0],Q[j]))
    elif i > 0 and j > 0:
        ca[i,j] = max(min(_c(ca,i-1,j,P,Q),_c(ca,i-1,j-1,P,Q),_c(ca,i,j-1,P,Q)),euc_dist(P[i],Q[j]))
    else:
        ca[i,j] = float("inf")
    return ca[i,j]
 
# 这个是给我们调用的方法
def frechet_distance(P,Q):
    ca = np.ones((len(P),len(Q)))
    ca = np.multiply(ca,-1)
    return _c(ca, len(P) - 1, len(Q) - 1, P, Q)  # ca是a*b的矩阵(3*4),2,3
 
curve_a = [(1,2),(2,4)]        # 这个是曲线1
curve_b = [(1,4),(2,8),(3,4)]  # 这个是曲线2
 
result = frechet_distance(curve_a,curve_b)
print(result)

