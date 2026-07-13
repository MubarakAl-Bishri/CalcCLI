import subprocess
import os
import datetime

# Define the comprehensive test suite
# Correct Typer Order: python3 main.py vector-operation v1 operation v2 [--show-steps]
test_categories = {
    "1. Vector & Vector Operations (Standard)": [
        'python3 main.py vector-operation "[2,3,4]" add "[4,5,6]"',
        'python3 main.py vector-operation "[x,y,z]" subtract "[1,1,1]"',
        'python3 main.py vector-operation "[1,0,0]" cross "[0,1,0]"',
        'python3 main.py vector-operation "[x,y,z]" cross "[x,y,z]"',
    ],
    "2. Vector & Vector Operations (Step-by-Step)": [
        'python3 main.py vector-operation "[2,3,4]" add "[4,5,6]" --show-steps',
        'python3 main.py vector-operation "[x,y,z]" dot "[1,2,3]" --show-steps',
        'python3 main.py vector-operation "[1,0,0]" cross "[0,1,0]" --show-steps',
    ],
    "3. Advanced Vector Operations (Angle & Projection)": [
        'python3 main.py vector-operation "[1,0,0]" angle "[0,1,0]"',
        'python3 main.py vector-operation "[1,1,0]" angle "[1,0,0]" --show-steps',
        'python3 main.py vector-operation "[2,2,0]" projection "[1,0,0]"',
        'python3 main.py vector-operation "[x,y,z]" projection "[1,1,1]" --show-steps',
    ],
    "4. Single Vector Operations (Length & Unit)": [
        # Note: v2 is left empty for these commands!
        'python3 main.py vector-operation "[3,4,0]" length',
        'python3 main.py vector-operation "[x,y,z]" length --show-steps',
        'python3 main.py vector-operation "[3,4,0]" unit',
        'python3 main.py vector-operation "[x,y,z]" unit --show-steps',
    ],
    "5. Vector & Scalar Operations (Scaling)": [
        'python3 main.py vector-operation "[3,-2,1]" multiply "x*y*z"',
        'python3 main.py vector-operation "[2,4,6]" divide "2"',
        'python3 main.py vector-operation "[x**2, y**2, z**2]" multiply "1/x" --show-steps',
    ],
    "6. Pure Scalar Operations": [
        'python3 main.py vector-operation "x**2" add "2*x"',
        'python3 main.py vector-operation "x+1" multiply "x-1" --show-steps',
        'python3 main.py vector-operation "10" divide "2"',
    ],
    "7. Safety Catches & Mathematical Errors": [
        # Adding vector to scalar
        'python3 main.py vector-operation "[2,3,4]" add "5"',
        # Subtracting vector from scalar
        'python3 main.py vector-operation "x" subtract "[1,2,3]"',
        # Dot/Cross with scalars (should fail gracefully)
        'python3 main.py vector-operation "[x,y,z]" dot "x"',
        'python3 main.py vector-operation "5" cross "[1,2,3]"',
        # Length/Unit of a scalar
        'python3 main.py vector-operation "5" length',
        'python3 main.py vector-operation "x" unit',
        # Zero vector operations (should trigger ZeroDivisionError logic)
        'python3 main.py vector-operation "[0,0,0]" unit',
        'python3 main.py vector-operation "[1,2,3]" projection "[0,0,0]"',
    ],
}

output_file = "test_results.md"


def run_tests():
    total_tests = sum(len(cmds) for cmds in test_categories.values())
    print(f"Running {total_tests} tests across {len(test_categories)} categories...")

    with open(output_file, "w", encoding="utf-8") as f:
        f.write(f"Test Run Timestamp: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
        f.write("# Calc 3 CLI - Ultimate Vector Operation Test Results\n\n")
        f.write("> Automated test run to verify mathematical accuracy, step-by-step logic, single-argument handling, and safety catches.\n\n")

        for category, commands in test_categories.items():
            f.write(f"## {category}\n\n")

            for cmd in commands:
                f.write(f"**Command executed:**\n`{cmd}`\n\n")

                # Execute the terminal command
                result = subprocess.run(cmd, shell=True, capture_output=True, text=True)

                # Combine stdout and stderr to capture normal outputs and Typer crash traces
                output = result.stdout.strip()
                error_output = result.stderr.strip()

                final_output = output if output else error_output

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