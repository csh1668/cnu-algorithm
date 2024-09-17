def naive(A, B):
    n = len(A)
    C = [[0 for _ in range(n)] for _ in range(n)]
    for i in range(n):
        for j in range(n):
            for k in range(n):
                C[i][j] += A[i][k] * B[k][j]
    return C

def strassen(A, B, threadhold=64):
    n = len(A)
    if n <= threadhold: return naive(A, B)
    def add(M1, M2, sz):
        return [[M1[i][j] + M2[i][j] for j in range(sz)] for i in range(sz)]
    def sub(M1, M2, sz):
        return [[M1[i][j] - M2[i][j] for j in range(sz)] for i in range(sz)]
    k = n // 2
    A11 = [[A[i][j] for j in range(k)] for i in range(k)]
    A12 = [[A[i][j] for j in range(k, n)] for i in range(k)]
    A21 = [[A[i][j] for j in range(k)] for i in range(k, n)]
    A22 = [[A[i][j] for j in range(k, n)] for i in range(k, n)]
    B11 = [[B[i][j] for j in range(k)] for i in range(k)]
    B12 = [[B[i][j] for j in range(k, n)] for i in range(k)]
    B21 = [[B[i][j] for j in range(k)] for i in range(k, n)]
    B22 = [[B[i][j] for j in range(k, n)] for i in range(k, n)]
    P1 = strassen(A11, sub(B12, B22, k))
    P2 = strassen(add(A11, A12, k), B22)
    P3 = strassen(add(A21, A22, k), B11)
    P4 = strassen(A22, sub(B21, B11, k))
    P5 = strassen(add(A11, A22, k), add(B11, B22, k))
    P6 = strassen(sub(A12, A22, k), add(B21, B22, k))
    P7 = strassen(sub(A11, A21, k), add(B11, B12, k))
    C11 = add(sub(add(P5, P4, k), P2, k), P6, k)
    C12 = add(P1, P2, k)
    C21 = add(P3, P4, k)
    C22 = sub(sub(add(P5, P1, k), P3, k), P7, k)
    C = [[0 for _ in range(n)] for _ in range(n)]
    for i in range(k):
        for j in range(k):
            C[i][j] = C11[i][j]
            C[i][j + k] = C12[i][j]
            C[i + k][j] = C21[i][j]
            C[i + k][j + k] = C22[i][j]
    return C