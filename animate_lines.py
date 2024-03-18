async def deleted_lines_animation(lines) -> None:
    if lines:
        for x in range(9, -1, -1):
            for y in lines:
                print(x)
                main_container.controls[y*10+x].border = ft.border.all(2, MUTE_COLOR)
                main_container.controls[y*10+x].content.controls[0].bgcolor = MUTE_COLOR
                page.update()
                await asyncio.sleep(0.05)