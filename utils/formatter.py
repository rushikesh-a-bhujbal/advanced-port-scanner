def format_results(results):
    print("\nPORT     STATE     SERVICE")

    for port, banner in sorted(results):
        service = banner if banner else "(no banner)"
        print(f"{port:<8} OPEN      {service}")

