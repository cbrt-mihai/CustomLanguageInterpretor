
iota_counter = 0
def iota(reset = False):
    global iota_counter
    if reset:
        iota_counter = 0
    else:
        result = iota_counter
        iota_counter += 1
        return result

OP_SET = iota()
OP_VAR = iota()
OP_ADDVV = iota()
OP_ADDVI = iota()
OP_ADDII = iota()
OP_ADDIV = iota()
OP_ENV = iota()
COUNT_OPS = iota()

def set(varName, value):
    return (OP_SET, varName, value)

def var(varName):
    return (OP_VAR, varName)

def addvv(res, x, y):
    return (OP_ADDVV, res, x, y)

def addvi(res, x, a):
    return (OP_ADDVI, res, x, a)

def addii(res, a, b):
    return (OP_ADDII, res, a, b)

def addiv(res, x, b):
    return (OP_ADDIV, res, x, b)

def add(res, fst, lst):
    if isinstance(fst, int):
        if isinstance(lst, int):
            op = OP_ADDII
        else:
            op = OP_ADDIV
    else:
        if isinstance(lst, int):
            op = OP_ADDVI
        else:
            op = OP_ADDVV
    return (op, res, fst, lst)

def env():
    return (OP_ENV, )

def interpret(program):
    env = []
    for op in program:
        assert COUNT_OPS == 7, "Not all operators have been implemented"
        if op[0] == OP_SET:
            bec = False
            for i, elem in enumerate(env):
                if elem[0] == op[1]:
                    bec = True
                    env.pop(i)
                    break
            env.append( (op[1], op[2]) )

        elif op[0] == OP_VAR:
            bec = False
            for elem in env:
                if elem[0] == op[1]:
                    bec = True
                    print(elem[1])
                    break
            if bec == False:
                print("not found")

        elif op[0] == OP_ADDVV:
            bec1 = False
            bec2 = False
            for elem in env:
                if elem[0] == op[2]:
                    bec1 = True
                    a = elem[1]
                if elem[0] == op[3]:
                    bec2 = True
                    b = elem[1]
            if bec1 and bec2:
                res = a + b
                bec = False
                for i, elem in enumerate(env):
                    if elem[0] == op[1]:
                        bec = True
                        env.pop(i)
                        break
                env.append( (op[1], res) )
            else:
                print("cannot add")

        elif op[0] == OP_ADDVI:
            bec1 = False
            for elem in env:
                if elem[0] == op[2]:
                    bec1 = True
                    a = elem[1]
            if bec1:
                res = a + op[3]
                bec = False
                for i, elem in enumerate(env):
                    if elem[0] == op[1]:
                        bec = True
                        env.pop(i)
                        break
                env.append((op[1], res))
            else:
                print("cannot add")

        elif op[0] == OP_ADDII:
            res = op[2] + op[3]
            bec = False
            for i, elem in enumerate(env):
                if elem[0] == op[1]:
                    bec = True
                    env.pop(i)
                    break
            env.append( (op[1], res) )


        elif op[0] == OP_ADDIV:
            bec1 = False
            for elem in env:
                if elem[0] == op[3]:
                    bec1 = True
                    b = elem[1]

            if bec1:
                res = b + op[2]
                bec = False
                for i, elem in enumerate(env):
                    if elem[0] == op[1]:
                        bec = True
                        env.pop(i)
                        break
                env.append((op[1], res))
            else:
                print("cannot add")

        elif op[0] == OP_ENV:
            print(env)
        else:
            assert False, "unreachable"

def getCodeLines(path):
    newLines = []
    with open(path) as f:
        lines = f.readlines()
        for line in lines:
            line = line.split("\n")[0]
            newLines.append(line)

    return newLines

def parseLines(lines):
    program = []

    for line in lines:
        # print(line)

        findPlus = line.find("+")
        findEqual= line.find("=")
        if findPlus != -1:
            plusParts = line.split("+")
            equalParts = plusParts[0].split("=")
            res = equalParts[0].strip(" ")
            fst = equalParts[1].strip(" ")
            lst = plusParts[1].strip(" ")

            program.append( add(res, fst, lst) )
        elif findEqual != -1:
            equalParts = line.split("=")
            vari = equalParts[0].strip(" ")
            val = equalParts[1].strip(" ")

            if val.isdigit():
                val = int(val)
                program.append(set(vari, val))
            else:
                program.append(add(vari, val, 0))

        else:
            spaceParts = line.split(" ")
            cmd = spaceParts[0]
            vr = spaceParts[1]
            if cmd == "var":
                program.append(var(vr))


    return program

program = [
    set("a", 5),
    set("b", 10),
    addvv("sum", "a", "b"),
    var("sum"),
    addii("sum2", 34, 35),
    var("sum2"),
    set("x", 69),
    var("x"),
    set("x", 70),
    var("x"),
    addii("sum", 10, 20),
    var("sum"),
    addvi("sum3", "a", 20),
    env()
]

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    path = "code.txt"

    lines = getCodeLines(path)
    print(lines)
    program = parseLines(lines)
    print(program)
    interpret(program)