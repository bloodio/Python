num = int(input())
score = []
for i in range (0, num):
    score.append(int(input()))

sum = 0
for i in range (0, num):
    sum = sum + score[i]
avg = sum / num
print(avg)
