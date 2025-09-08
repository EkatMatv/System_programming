import threading

reminders = [
    ("Сообщение 1", 1),
    ("Сообщение 2", 2),
    ("Сообщение 3", 3),
]

timers = []
for message, delay in reminders:
    timer = threading.Timer(delay, print, args=[message])
    timers.append(timer)
    timer.start()
    print(f"Таймер установлен: '{message}' через {delay} сек")

for timer in timers:
    timer.join()

print("Все напоминания выполнены!")