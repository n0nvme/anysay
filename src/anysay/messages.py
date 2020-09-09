from sty import bg, fg, rs

from colored import attr as attr_c
from colored import bg as bg_c
from colored import fg as fg_c


def convert_truecolor_char(rgba0, rgba1):
    top = rgba0[:3]
    bottom = rgba1[:3]
    if len(rgba0) > 3 and len(rgba1) > 3:
        if rgba0[3] == rgba1[3]:
            if rgba0[0] == 0:
                top = bg.rs
                char = " "
            else:
                char = "█"

        elif rgba0[3] == 0:
            top = bg.rs
            char = "▄"
        else:
            bottom = top
            top = bg.rs
            char = "▀"

    # logger.debug(f"top color: {rgba0} botom color: {rgba1}")
    result = bg(*top) + fg(*bottom) + char + rs.all
    return result


def bordered_message(mes: str, border_color, char_color) -> str:
    midle_char = convert_truecolor_char(border_color, border_color)
    top_angle_char = convert_truecolor_char((0, 0, 0, 0), border_color)
    top_line = convert_truecolor_char(border_color, (0, 0, 0, 0))
    bottom_angle_char = top_line
    bottom_line = top_angle_char

    messages_lines = mes.split(r"\n")
    max_line_len = max([len(line) for line in messages_lines])

    border_message = (
        f"\n\n  {top_angle_char}{top_line * (max_line_len + 3)}{top_angle_char}\n"
    )

    for line in messages_lines:
        addition_spaces = " " * (max_line_len - len(line))
        border_message += f" {midle_char}  {line}{addition_spaces}   {midle_char}\n"

    border_message += (
        f"  {bottom_angle_char}{bottom_line * (max_line_len + 3)}{bottom_angle_char}\n"
    )

    return border_message


if __name__ == "__main__":
    print(
        bordered_message(
            r"i'm piklerick \n MORTYYYY !1!", (123, 123, 123, 1), (0, 0, 0, 0)
        )
    )
