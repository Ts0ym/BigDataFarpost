def check_tic_tac_toe_winner(board):
    lines = []

    lines.extend(board)

    lines.extend([[board[r][c] for r in range(3)] for c in range(3)])

    lines.append([board[i][i] for i in range(3)])
    lines.append([board[i][2 - i] for i in range(3)])

    for line in lines:
        if line.count('x') == 3:
            return "x wins!"
        if line.count('o') == 3:
            return "o wins!"

    for row in board:
        if '-' in row:
            return "unfinished!"

    return "draw!"