import subprocess

steps = [

    ("PDF EXTRACTION", "python3 test_extract.py"),

    ("MASTER CLEANING", "python3 clean_master.py"),

    ("SMART CLEANING", "python3 smart_cleaner.py"),

    ("ANALYTICS ENGINE", "python3 analytics_engine.py"),

]

for step_name, command in steps:

    print("\n" + "=" * 50)
    print(f"RUNNING: {step_name}")
    print("=" * 50)

    result = subprocess.run(
        command,
        shell=True
    )

    if result.returncode != 0:

        print(f"\nFAILED at: {step_name}")
        break

print("\nPIPELINE COMPLETED")