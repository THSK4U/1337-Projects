# to install poetry "curl -sSL https://install.python-poetry.org | python3 -"
from importlib import import_module, metadata
import sys


def check_dependencies():
    missing: list = []
    required: dict = {
        "pandas": "Data manipulation",
        "requests": "Network access",
        "matplotlib": "Visualization",
        "numpy": "Numerical computing",
    }
    for pkg, value in required.items():
        try:
            import_module(pkg)
            version = metadata.version(pkg)
            print(f"[OK] {pkg} ({version}) - {value} ready")
        except ModuleNotFoundError:
            print(f"[MISSING] {pkg}")
            missing.append(pkg)
    return missing


def main():
    try:
        print("LOADING STATUS: Loading programs...")

        print("\nChecking dependencies:")
        check_missing = check_dependencies()
        if check_missing:
            print(f"""\nMissing {check_missing} dependencies!
    Please run: python3 -m pip install -r requirements.txt
    Or: python3 -m pip install poetry && poetry install""")
            sys.exit(1)

        import pandas
        import requests
        from matplotlib import pyplot
        import numpy

        print("\nAnalyzing Matrix data...")
        print("Processing 1000 data points...")

        response = requests.get("https://httpbin.org/get")
        status_code = response.status_code

        data = numpy.random.rand(1000)
        data_frame = pandas.DataFrame({"values": data})

        pyplot.plot(data_frame["values"])
        pyplot.title(f"Matrix Analysis (HTTP status: {status_code})")

        output_image = "matrix_analysis.png"
        pyplot.savefig(output_image)
        print("Generating visualization...")

        print("\nAnalysis complete!")
        print(f"Results saved to: {output_image}")

    except ModuleNotFoundError as e:
        print(e)


main()
