from config import settings


def _format_top_failed(pairs):
    if not pairs:
        return "(sin datos aun)"
    return ", ".join(f"{char.upper()} x{count}" for char, count in pairs)


def draw(screen, font_title, font_hud, statistics, player, key_stats):
    width, height = screen.get_size()
    data = statistics.data

    title_surf = font_title.render("MIS ESTADISTICAS", True, settings.COLORS["accent"])
    screen.blit(title_surf, title_surf.get_rect(center=(width // 2, 80)))

    lines = [
        f"XP total: {player.data['total_xp']}",
        f"Niveles completados: {data['levels_completed']}",
        f"Estrellas obtenidas: {data['stars_earned']}",
        f"WPM promedio: {statistics.average_wpm:.1f}",
        f"WPM maximo: {data['best_wpm']:.1f}",
        f"Precision promedio: {statistics.average_precision:.1f}%",
        f"Total de caracteres escritos: {data['total_characters_typed']}",
        f"Total de palabras (aprox.): {int(statistics.total_words_typed)}",
        f"Total de errores: {data['total_errors']}",
        f"Tiempo jugado: {int(data['total_time_played_seconds'])}s",
        f"Mejor combo: x{data['best_combo']}",
        f"Letras mas falladas: {_format_top_failed(key_stats.most_failed_letters(3))}",
        f"Numeros mas fallados: {_format_top_failed(key_stats.most_failed_numbers(3))}",
        f"Simbolos mas fallados: {_format_top_failed(key_stats.most_failed_symbols(3))}",
    ]

    y = 150
    for line in lines:
        surf = font_hud.render(line, True, settings.COLORS["text"])
        screen.blit(surf, surf.get_rect(center=(width // 2, y)))
        y += surf.get_height() + 6

    hint_surf = font_hud.render("ESC para volver al menu", True, settings.COLORS["text_pending"])
    screen.blit(hint_surf, hint_surf.get_rect(center=(width // 2, height - 60)))
