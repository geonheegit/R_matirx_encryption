import numpy as np

def convert_string_to_numbers(input_string):
    input_string = input_string.lower()  # 모든 문자를 소문자로 변환

    alphabet = 'abcdefghijklmnopqrstuvwxyz'
    result = []

    for char in input_string:
        if char.isalpha():  # 알파벳인 경우에만 변환
            index = alphabet.index(char)
            result.append(index)
        elif char == " ":
            result.append(27) # 27은 띄어쓰기를 의미함.

    return result

def get_alphabet_by_index(number, mode):
    alphabet = 'abcdefghijklmnopqrstuvwxyz'
    result_list = []
    if mode == "FD": # Forced Decryption
        index = (number) % 26  # 알파벳 인덱스 계산
        result_list.append(alphabet[index])

    elif mode == "RD": # Real Decryption
        if 0 <= number <= 25:
            result_list.append(alphabet[number])
        elif number == 27:
            result_list.append(" ")
        elif number == 30:
            result_list.append("")

    return result_list[0]

def decrypt(encrypted_list, password_np_array): # 왼쪽 위부터 글 읽는 방식으로
    normal_alphabets_in_nums = []
    normal_alphabets_list = []
    decrypted_arrays = []

    for each_22_np_array in encrypted_list:
        each_decrypted_array = each_22_np_array @ np.linalg.inv(password_np_array) # 역행렬 곱하기
        decrypted_arrays.append(each_decrypted_array)

    for i in decrypted_arrays:
        for j in i:
            for k in j:
                normal_alphabets_in_nums.append(int(round(k)))

    for i in normal_alphabets_in_nums:
        normal_alphabets_list.append(get_alphabet_by_index(i, "RD"))

    original_str = ''.join(normal_alphabets_list)
    return original_str

def forced_decryption(encrypted_matrices_list):
    normal_alphabets_in_nums = []
    encrypted_alphabets_list = []

    for i in encrypted_matrices_list:
        for j in i:
            for k in j:
                normal_alphabets_in_nums.append(int(round(k)))
    # print(normal_alphabets_in_nums)
    for i in normal_alphabets_in_nums:
        encrypted_alphabets_list.append(get_alphabet_by_index(i, "FD"))

    str = ''.join(encrypted_alphabets_list)
    return str

def adjust_list(lst): # 숫자 30은 빈공간을 의미
    dummy_list = [30, 30]

    last_list = lst[-1]  # 마지막 리스트
    while len(last_list) < 2:
        last_list.append(30)

    if len(lst) % 2 != 0:
        lst.append(dummy_list)

    return lst

def encrypt_or_decrypt(input, password, mode):
    converted_numbers = convert_string_to_numbers(input)

    foursliced_numbers = []
    for i in range(0, len(converted_numbers), 2):
        group = converted_numbers[i:i + 2]
        foursliced_numbers.append(group)

    # print(foursliced_numbers)
    filled_fs_numbers = adjust_list(foursliced_numbers)
    # print(f"빈 공간 채워진 리스트: {filled_fs_numbers}")

    foursliced_numbers_22_adjusted = []
    for i in range(0, len(filled_fs_numbers), 2):
        group = filled_fs_numbers[i:i + 2]
        foursliced_numbers_22_adjusted.append(group)
    # print(f"빈 공간 채워진 2x2 리스트: {foursliced_numbers_22_adjusted}")

    foursliced_numbers_22_adjusted_np = []
    for i in foursliced_numbers_22_adjusted:
        arrayed_list = np.array(i)
        foursliced_numbers_22_adjusted_np.append(arrayed_list)

    # =============================
    password_numbers = []
    for i in range(0, len(password)):
        each_num = password[i]
        password_numbers.append(int(each_num))

    # 비밀번호 리스트를 2x2 넘파이 배열로
    password_numbers_np = np.array(password_numbers)
    password_numbers_np = password_numbers_np.reshape((2, 2))
    # print(password_numbers_np)

    # 2x2씩 쪼개인 문자열 행렬과 비밀번호 행렬의 행렬곱 연산
    encrypted_matrices = []
    for i in foursliced_numbers_22_adjusted_np:
        result_matrix = i @ password_numbers_np  # 행렬곱 연산
        encrypted_matrices.append(result_matrix)
    # ==============================
    if mode == 1:
        print(f"입력한 문장: {user_input}")
        print(f"비밀번호: {user_password}")
        print(f"암호화된 문장: {forced_decryption(encrypted_matrices)}")

        np.save("data\encrypted_sentence_mat.npy", encrypted_matrices)
        # print(f"복호화된 문장: {decrypt(encrypted_matrices, password_numbers_np)}")

    elif mode == 2:
        encrypted_matrices = np.load("data/encrypted_sentence_mat.npy")
        print(f"복호화된 문장: {decrypt(encrypted_matrices, password_numbers_np)}")

mode = int(input("숫자를 입력하세요.\n①: 암호화, ②: 복호화\n▶ "))

user_input = input("문자열을 입력하세요: ")
user_password = input("4자리 숫자 비밀번호를 입력하세요: ")

if mode == 1:
    encrypt_or_decrypt(user_input, user_password, 1)

elif mode == 2:
    try:
        encrypt_or_decrypt(user_input, user_password, 2)
    except:
        print("오류 발생. 비밀번호가 틀립니다.")