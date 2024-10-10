class Setting():
    def GetConnectionString(self):
        with open("ConnectionString.txt") as f:
            return str(f.read())

