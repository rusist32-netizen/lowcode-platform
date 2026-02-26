import sys
import traceback

try:
    from run_platform import main
    main()
except Exception as e:
    with open("crash_log.txt", "w", encoding="utf-8") as f:
        f.write("ОШИБКА:\n")
        f.write(str(e) + "\n\n")
        f.write("ПОДРОБНЫЙ TRACEBACK:\n")
        traceback.print_exc(file=f)
    
    print("=" * 60)
    print("ПРОГРАММА УПАЛА! Ошибка записана в crash_log.txt")
    print("=" * 60)
    
    # Показываем ошибку на экране
    input("Нажмите Enter чтобы увидеть ошибку...")
    traceback.print_exc()
    input("\nНажмите Enter для выхода...")