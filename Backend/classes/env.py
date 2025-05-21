def entry(data: dict = None, read_mode: bool = True):
    with open(file=".env", mode="r" if read_mode else "w", encoding="utf-8") as env:
        if read_mode:
            data = {}
            for line in env.readlines():
                key, value = line.split("=")
                data[key.strip()] = value.strip()
            return data
        else:
            output = ""
            for [key, value] in data.items():
                output += f"{key}={value}\n"
            env.write(output.strip())
