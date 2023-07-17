lista = [[1, 2], [1]]
print(lista)

def adjust_list(lst):
    last_list = lst[-1]  # 마지막 리스트
    while len(last_list) < 4:
        last_list.append("d")

    return lst

print(adjust_list(lista))