def updateEnv(key, value, env_file=".env"):
    with open(env_file, "r") as file:
        lines = file.readlines()

    updated = False
    with open(env_file, "w") as file:
        for line in lines:
            if line.startswith(f"{key}="):
                file.write(f"{key}='{value}'\n")
                updated = True
            else:
                file.write(line)

        if not updated:
            file.write(f"{key}={value}\n")