def write_zigzag():
    zig_zag_size = 40
    line = "*" * 8
    num_lines = 1000

    with open("zigzag.txt", "w", encoding="utf-8") as f:
        for i in range(num_lines):
            indents = i % zig_zag_size
            if indents <= zig_zag_size // 2:
                print(indents * " ", line, sep="", file=f)
            elif indents > zig_zag_size // 2:
                print((zig_zag_size - indents) * " ", line, sep="", file=f)


write_zigzag()