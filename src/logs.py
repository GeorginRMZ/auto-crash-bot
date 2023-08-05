from datetime import datetime


async def write_log(log: str) -> bool:
    now = datetime.now()
    date = f"{now.year}-{now.month}-{now.day} {now.hour}:{now.minute}:{now.second}.{now.microsecond}"

    try:
        file = open("logs.txt", "a+")
        file.write(f"{date} {log}\n")
        file.close()
        print(f"{date} {log}")
        return True
    except Exception as error_name:
        print(f"An error {error_name} occurred while logging.")
        return False
