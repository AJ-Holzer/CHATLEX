import time

from argon2 import PasswordHasher

from env.config import config


# trunk-ignore(bandit/B107)
def calibrate_argon2_time_cost(
    target_duration: float = config.ARGON2_TARGET_PASSWORD_DURATION,
    memory_cost: int = config.ARGON2_MEMORY_COST,
    parallelism: int = config.ARGON2_PARALLELISM,
    hash_len: int = config.ARGON2_HASH_LEN,
    max_time_cost: int = config.ARGON2_MAX_TIME_COST_CALIBRATION,
    password_sample: str = "benchmark_password",
) -> int:
    """
    Calibrates the Argon2 time_cost parameter to achieve a target password hashing duration.
    This function iteratively increases the Argon2 time_cost parameter until the time taken to hash
    a sample password meets or exceeds the specified target duration. It returns the smallest
    time_cost value that satisfies the duration constraint, or the maximum allowed time_cost if
    the target duration is not reached.

    Args:
        target_duration (float): Desired minimum duration (in seconds) for hashing the password.
        memory_cost (int): Amount of memory (in kibibytes) to use for hashing.
        parallelism (int): Number of parallel threads to use for hashing.
        hash_len (int): Length of the resulting hash.
        max_time_cost (int): Maximum time_cost value to test during calibration.
        password_sample (str): Sample password to use for benchmarking.

    Returns:
        int: The calibrated time_cost value that achieves at least the target_duration, or
             max_time_cost if the target duration is not reached.
    """
    for time_cost in range(1, max_time_cost + 1):
        print(f"[Calibration] Testing time cost {time_cost}...")

        # Initialize password hasher
        ph = PasswordHasher(
            time_cost=time_cost,
            memory_cost=memory_cost,
            parallelism=parallelism,
            hash_len=hash_len,
        )

        # Test hash duration
        start = time.perf_counter()
        ph.hash(password_sample)
        duration = time.perf_counter() - start

        # Return if hash duration exceeded time limit
        if duration >= target_duration:
            print(f"[Calibration] Chose time_cost={time_cost} (~{duration:.2f}s)")
            return time_cost

    # Return max time cost if hashing did not exceed time limit
    print(
        f"[Calibration] Max time_cost={max_time_cost} reached; duration < {target_duration}s"
    )
    return max_time_cost
