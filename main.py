# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.


def print_hi(name):
    # Use a breakpoint in the code line below to debug your script.
    print(f'Hi, {name}')  # Press Ctrl+F8 to toggle the breakpoint.
    print("Hello Python      ")
    print(name.title())
    print(name.lower())
    print(name.upper())


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    print_hi('PyCharm')
    char_demo_list = ["a","b","c","d","e","f","g"]
    del char_demo_list[0]
    print(char_demo_list)

    char_demo_list.pop()
    print(char_demo_list)
    print(len(char_demo_list))
    print(char_demo_list)
    number_list = list(range(1,9,3))
    print(number_list)

    square_num_list = [value**2 for value in range(1,11)]
    print(square_num_list)

    print("==============列表解析法 打印1-20数字=============")
    num_list = [value for value in range(1,21)]
    print(str(num_list)+"\n")

    print("===================== 列表切片用法==================")
    demo_list1 = ["a","b","c","d"]
    demo_list2 = demo_list1
    demo_list_new = demo_list1[:]
    print("demo_new 列表输出")
    print(demo_list_new)
    demo_list1.append("e")
    print(demo_list1)
    print(demo_list2)
    print(demo_list_new)
# See PyCharm help at https://www.jetbrains.com/help/pycharm/
