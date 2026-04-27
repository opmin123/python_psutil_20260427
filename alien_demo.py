"""
外星人颜色(if-elif-else demo)
2026-4-22
"""
alien_color = ["green","yellow","red"]
for color in alien_color:
    if color == "green":
        print("获得5个点积分")


"""
判断处于哪个阶段(if-elif-else demo)

"""
age = 35
if age < 2:
    print("婴儿阶段")
elif age >=2 and age < 4:
    print("学步阶段")
elif age >=4 and age < 13:
    print("儿童阶段")
elif age >= 13 and age < 20:
    print("青年")
elif age >= 20 and age < 65:
    print("成年人")
elif age >= 65:
    print("老年人")


"""

字典案例demo 2026-4-23
"""
alien_0 = {"color": "red","points": 5}
alien_1 = {"color": "green","points": 10}
alien_2 = {"color": "yellow","points": 15}
aline_list = [alien_0,alien_1,alien_2]
for aline in aline_list:
    print(aline)



"""
字典 批量打印外星人数量案例 2026-4-23
"""

alines = []
for aline_number in range(30):
    new_aline = {"color": "red", "points": 5, "speed": "slow"}
    alines.append(new_aline)
print(len(alines))
for aline_p in alines[:5]:
    print(aline_p)
print("...")


"""
输入函数input() 函数 2026-4-23
"""

message = input("请输入:...")
print(message)