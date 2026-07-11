import subprocess
import os
import datetime
# Define the test suite
test_categories = {
    "1. Vector & Vector Operations (Constants & Algebraic)": [
        'python3 main.py vector-operation "[2,3,4]" "[4,5,6]" "add"',
        'python3 main.py vector-operation "[x,y,z]" "[1,1,1]" "subtract"',
        'python3 main.py vector-operation "[x,y,z]" "[1,2,3]" "dot"',
        'python3 main.py vector-operation "[1,0,0]" "[0,1,0]" "cross"',
        'python3 main.py vector-operation "[x,y,z]" "[x,y,z]" "cross"',
    ],
    "2. Vector & Scalar Operations (Scaling)": [
        'python3 main.py vector-operation "[3,-2,1]" "x*y*z" "multiply"',
        'python3 main.py vector-operation "[2,4,6]" "2" "divide"',
        'python3 main.py vector-operation "[x**2, y**2, z**2]" "1/x" "multiply"',
    ],
    "3. Pure Scalar Operations": [
        'python3 main.py vector-operation "x**2" "2*x" "add"',
        'python3 main.py vector-operation "x+1" "x-1" "multiply"',
    ],
    "4. The Safety Catch Tests (Expecting Errors)": [
        'python3 main.py vector-operation "[2,3,4]" "5" "add"',
        'python3 main.py vector-operation "x" "[1,2,3]" "subtract"',
        'python3 main.py vector-operation "[x,y,z]" "x" "dot"',
        'python3 main.py vector-operation "5" "[1,2,3]" "cross"',
    ],
}

output_file = "test_results.md"


def run_tests():
    print(f"Running {sum(len(cmds) for cmds in test_categories.values())} tests...")

    with open(output_file, "w", encoding="utf-8") as f:
        f.write(f"Test Run Timestamp: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
        f.write("# Calc 3 CLI - Vector Operation Test Results\n\n")
        f.write(
            "> Automated test run to verify mathematical accuracy and safety catches.\n\n"
        )

        for category, commands in test_categories.items():
            f.write(f"## {category}\n\n")

            for cmd in commands:
                f.write(f"**Command executed:**\n`{cmd}`\n\n")

                # Execute the terminal command
                # capture_output grabs stdout and stderr
                # text=True ensures we get string output instead of raw bytes
                result = subprocess.run(cmd, shell=True, capture_output=True, text=True)

                # Combine standard output and standard error just in case Typer routes errors to stderr
                output = result.stdout.strip()
                error_output = result.stderr.strip()

                final_output = output if output else error_output

                # If the script fails completely (like a syntax error before Typer catches it)
                if not final_output:
                    final_output = "No output or fatal crash."

                f.write("**Output:**\n")
                f.write("```text\n")
                f.write(final_output + "\n")
                f.write("```\n\n")
                f.write("---\n\n")

    print(f"✅ Testing complete! Results saved to {os.path.abspath(output_file)}")


if __name__ == "__main__":
    run_tests()
