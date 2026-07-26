def combine_two_text_files(file_a, file_b, file_write):
    with (
        open(file_write, "w", encoding="UTF-8") as f_out,
        open(file_a, encoding="UTF-8") as fa,
        open(file_b, encoding="UTF-8") as fb,
    ):
        f_out.write(fa.read())
        f_out.write(fb.read())


combine_two_text_files(
    input("Enter file a's name:\n"),
    input("Enter file b's name:\n"),
    input("Enter the output file's name:\n"),
)
