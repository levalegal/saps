import sys
import os
os.chdir(os.path.dirname(os.path.abspath(__file__)))

# Добавляем текущую директорию в путь
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

try:
    from main import main
    main()
except Exception as e:
    import traceback
    print("=" * 80)
    print("CRITICAL ERROR:")
    print("=" * 80)
    print(str(e))
    print("\n" + "=" * 80)
    print("TRACEBACK:")
    print("=" * 80)
    traceback.print_exc()
    input("\nPress Enter to exit...")
