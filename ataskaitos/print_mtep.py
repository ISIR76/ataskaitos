"""Minimal utility to print MTEP evaluation results."""

from ataskaitos.agent_from_human import MTEPVertinimas


def print_mtep(result: MTEPVertinimas) -> None:
    """Print MTEP evaluation in clean format."""

    print("\n" + "=" * 80)
    if result.score:
        score_val = float(result.score)
        status = "✓ ATITINKA" if score_val >= 0.70 else "✗ NEATITINKA"
        print(f"MTEP VERTINIMAS | Score: {score_val:.2f} | {status}")
    else:
        print("MTEP VERTINIMAS")
    print("=" * 80)

    # Initial Analysis
    print("\nPRADINĖ ANALIZĖ:")
    print(f"  {result.initial_analysis}")

    print()

    # 5 Core Criteria
    print("5 PAGRINDINIAI KRITERIJAI:")
    core_scores = []
    for name, field in [
        ("Naujumas", result.naujumas),
        ("Kūrybiškumas", result.kurybiskumas),
        ("Neapibrėžtumas", result.neapibreztumas),
        ("Sistemingumas", result.sistemingumas),
        ("Perduodamumas", result.perduodamumas),
    ]:
        score_val = float(field.score)
        core_scores.append(score_val)
        icon = "✓" if score_val >= 0.70 else "✗"
        print(f"  [{icon} {score_val:.2f}] {name}: {field.reason}")

    avg_core = sum(core_scores) / len(core_scores)
    print(f"  → Vidutinis balas: {avg_core:.2f}")

    # Document Structure
    print("\nDOKUMENTO STRUKTŪRA:")
    for name, field in [
        ("Įvadas", result.ivadas),
        ("Problemos formulavimas", result.problemos_formulavimas),
        ("Uždavinio apibrėžimas", result.uzdavinio_apibrezimas),
        ("Veiklos aprašymas", result.veiklos_aprasymas),
        ("Rezultato pateikimas", result.rezultato_pateikimas),
        ("Problemos sprendimas", result.problemos_sprendimas),
        ("Loginė seka", result.logine_seka),
    ]:
        score_val = float(field.score)
        icon = "✓" if score_val >= 0.70 else "✗"
        print(f"  [{icon} {score_val:.2f}] {name}: {field.reason}")

    # Red Flags
    print("\nRAUDONOS VĖLIAVOS:")
    for name, field in [
        ("Praktikos žodžiai", result.praktikos_zodziai),
        ("Tik modeliavimas", result.tik_modeliavimas),
        ("Mokslinis naujumas", result.mokslinis_naujumas),
        ("Tinkama tema", result.tinkama_tema),
    ]:
        score_val = float(field.score)
        icon = "✓" if score_val >= 0.70 else "⚠"
        print(f"  [{icon} {score_val:.2f}] {name}: {field.reason}")

    # Result Type
    print("\nREZULTATO TIPAS:")
    result_types = [
        ("Fundamentiniai tyrimai", result.rezultato_tipas_fundamentiniai_tyrimai),
        ("Koncepcija", result.rezultato_tipas_koncepcija),
        ("Parametrai", result.rezultato_tipas_parametrai),
        ("Pirminis maketas", result.rezultato_tipas_pirminis_maketas),
        ("Realus maketas", result.rezultato_tipas_realus_maketas),
        ("Prototipas", result.rezultato_tipas_prototipas),
        ("Galutinis prototipas", result.rezultato_tipas_galutinis_prototipas),
        ("Bandomoji partija", result.rezultato_tipas_bandomoji_partija),
        ("Įvertinta partija", result.rezultato_tipas_ivertinta_partija),
    ]
    found_type = False
    for name, field in result_types:
        score_val = float(field.score)
        if score_val >= 0.70:
            print(f"  ✓ {name} [{score_val:.2f}]: {field.reason}")
            found_type = True
    if not found_type:
        print("  (Nenustatytas aiškus rezultato tipas)")

    # Assessment Overview
    print("\nBENDRAS ĮVERTINIMAS:")
    print(f"  {result.assessment_overview}")

    print("\n" + "=" * 80 + "\n")
